-- Bölüm, doktor, muayene ve teşhis modülü sorguları
-- Hazırlayan: Sude
-- Önce tüm tablolar ve örnek veriler yüklenmiş olmalı (sql/00_kurulum.sql).

-- Sorgu 1: Bölüm bazında hasta sayısı
-- Her bölüme kaç farklı hastanın randevu aldığını gösterir (iptal edilenler sayılmaz).
-- Aynı hasta bir bölüme iki kez geldiyse bir kez sayılır (DISTINCT).
-- LEFT JOIN sayesinde hiç hastası olmayan bölüm de 0 ile listelenir.
SELECT b.bolum_adi,
       COUNT(DISTINCT r.hasta_id) AS hasta_sayisi
FROM bolum b
LEFT JOIN doktor d ON d.bolum_id = b.bolum_id
LEFT JOIN randevu r ON r.doktor_id = d.doktor_id AND r.durum <> 'iptal'
GROUP BY b.bolum_id, b.bolum_adi
ORDER BY hasta_sayisi DESC, b.bolum_adi;

-- Sorgu 2: Doktor başına muayene sayısı
-- Muayene, randevu üzerinden doktora bağlanır (muayene -> randevu -> doktor).
-- Hiç muayene yapmamış doktor da 0 ile görünür.
SELECT d.unvan || ' ' || d.ad || ' ' || d.soyad AS doktor,
       b.bolum_adi,
       COUNT(m.muayene_id) AS muayene_sayisi
FROM doktor d
JOIN bolum b ON b.bolum_id = d.bolum_id
LEFT JOIN randevu r ON r.doktor_id = d.doktor_id
LEFT JOIN muayene m ON m.randevu_id = r.randevu_id
GROUP BY d.doktor_id, d.unvan, d.ad, d.soyad, b.bolum_adi
ORDER BY muayene_sayisi DESC, doktor;

-- Sorgu 3: En sık konulan teşhisler
-- muayene_teshis ara tablosunda her teşhisin kaç muayenede geçtiğini sayar.
-- En çok konulan 5 teşhis gelir.
SELECT t.teshis_kodu,
       t.teshis_adi,
       COUNT(*) AS kac_kez
FROM muayene_teshis mt
JOIN teshis t ON t.teshis_kodu = mt.teshis_kodu
GROUP BY t.teshis_kodu, t.teshis_adi
ORDER BY kac_kez DESC, t.teshis_kodu
LIMIT 5;

-- Sorgu 4: LEFT JOIN örneği - aktif randevusu olmayan doktorlar
-- Önümüzdeki günlerde hiç aktif randevusu olmayan (boş) doktorları bulur.
-- LEFT JOIN eşleşmeyen doktorları da getirir, onların randevu sütunları NULL olur.
-- Koşul ON kısmında, çünkü WHERE'e yazılsaydı NULL satırlar elenirdi.
-- (Not: "Hiç randevusu olmayan doktor" diye sorulsaydı örnek verilerde sonuç boş çıkardı,
-- çünkü 10 doktorun hepsinin en az bir randevusu var.)
SELECT d.doktor_id,
       d.unvan || ' ' || d.ad || ' ' || d.soyad AS doktor,
       b.bolum_adi
FROM doktor d
JOIN bolum b ON b.bolum_id = d.bolum_id
LEFT JOIN randevu r ON r.doktor_id = d.doktor_id AND r.durum = 'aktif'
WHERE r.randevu_id IS NULL
ORDER BY d.doktor_id;

-- Sorgu 5: Hastanın geçmiş muayeneleri ve teşhisleri (FG-16)
-- Hasta 3'ün muayeneleri ve o muayenelerde konulan teşhisler.
-- Çoka çok ilişki muayene_teshis ara tablosu üzerinden okunur.
SELECT m.muayene_tarihi,
       d.ad || ' ' || d.soyad AS doktor,
       m.sikayet,
       t.teshis_kodu,
       t.teshis_adi
FROM muayene m
JOIN randevu r ON r.randevu_id = m.randevu_id
JOIN doktor d ON d.doktor_id = r.doktor_id
JOIN muayene_teshis mt ON mt.muayene_id = m.muayene_id
JOIN teshis t ON t.teshis_kodu = mt.teshis_kodu
WHERE r.hasta_id = 3
ORDER BY m.muayene_tarihi DESC, t.teshis_kodu;
