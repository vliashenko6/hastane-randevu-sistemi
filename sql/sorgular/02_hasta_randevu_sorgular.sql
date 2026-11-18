-- Hasta ve randevu modülü sorguları
-- Önce tüm tablolar ve örnek veriler yüklenmiş olmalı.
-- Sorgulardaki doktor, hasta ve tarih değerlerini istediğin gibi değiştirebilirsin.

-- Sorgu 1: Doktorun günlük randevuları
-- Doktor 1'in 1 Aralık 2026 günü randevuları, saat sırasına göre (iptal edilenler gelmez).
SELECT r.randevu_saati,
       h.ad || ' ' || h.soyad AS hasta,
       h.telefon,
       r.durum
FROM randevu r
JOIN hasta h ON h.hasta_id = r.hasta_id
WHERE r.doktor_id = 1
  AND r.randevu_tarihi = '2026-12-01'
  AND r.durum <> 'iptal'
ORDER BY r.randevu_saati;

-- Sorgu 2: Hastanın randevu geçmişi
-- Hasta 1'in tüm randevuları (geçmiş ve gelecek), en yeniden eskiye doğru.
SELECT r.randevu_tarihi,
       r.randevu_saati,
       b.bolum_adi,
       d.unvan || ' ' || d.ad || ' ' || d.soyad AS doktor,
       r.durum
FROM randevu r
JOIN doktor d ON d.doktor_id = r.doktor_id
JOIN bolum b ON b.bolum_id = d.bolum_id
WHERE r.hasta_id = 1
ORDER BY r.randevu_tarihi DESC, r.randevu_saati DESC;

-- Sorgu 3: Tarih aralığına göre randevular
-- 3 Kasım ile 6 Kasım 2026 arasındaki (bu günler dahil) tüm randevular.
SELECT r.randevu_tarihi,
       r.randevu_saati,
       h.ad || ' ' || h.soyad AS hasta,
       d.ad || ' ' || d.soyad AS doktor,
       r.durum
FROM randevu r
JOIN hasta h ON h.hasta_id = r.hasta_id
JOIN doktor d ON d.doktor_id = r.doktor_id
WHERE r.randevu_tarihi BETWEEN '2026-11-03' AND '2026-11-06'
ORDER BY r.randevu_tarihi, r.randevu_saati;

-- Sorgu 4a: İptal edilen randevu sayısı (toplam)
SELECT COUNT(*) AS iptal_sayisi
FROM randevu
WHERE durum = 'iptal';

-- Sorgu 4b: İptal edilen randevu sayısı, doktora göre
-- En çok iptal olan doktor en üstte çıkar.
SELECT d.ad || ' ' || d.soyad AS doktor,
       COUNT(*) AS iptal_sayisi
FROM randevu r
JOIN doktor d ON d.doktor_id = r.doktor_id
WHERE r.durum = 'iptal'
GROUP BY d.doktor_id, d.ad, d.soyad
ORDER BY iptal_sayisi DESC, doktor;
