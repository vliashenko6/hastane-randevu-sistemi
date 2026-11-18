-- İlaç ve reçete modülü sorguları
-- Hazırlayan: Veronika
-- Önce tüm tablolar ve örnek veriler yüklenmiş olmalı (sql/00_kurulum.sql).

-- Sorgu 1: En çok yazılan ilaçlar (GROUP BY + ORDER BY)
-- Her ilacın kaç farklı reçetede yazıldığını ve toplam kaç kutu verildiğini gösterir.
-- LEFT JOIN sayesinde hiç yazılmamış ilaç da 0 ile listelenir.
SELECT i.ilac_adi,
       COUNT(ri.recete_id)          AS recete_sayisi,
       COALESCE(SUM(ri.kutu_adedi), 0) AS toplam_kutu
FROM ilac i
LEFT JOIN recete_ilac ri ON ri.ilac_id = i.ilac_id
GROUP BY i.ilac_id, i.ilac_adi
ORDER BY recete_sayisi DESC, i.ilac_adi;

-- Sorgu 2: Bir reçetedeki ilaçlar (N-N ilişki üzerinden JOIN)
-- recete -> recete_ilac -> ilac zinciriyle 8 numaralı reçetenin ilaçlarını,
-- dozlarını ve kullanım şekillerini getirir.
SELECT r.recete_id,
       r.recete_tarihi,
       i.ilac_adi,
       ri.doz,
       ri.kullanim_sekli,
       ri.kutu_adedi
FROM recete r
JOIN recete_ilac ri ON ri.recete_id = r.recete_id
JOIN ilac i ON i.ilac_id = ri.ilac_id
WHERE r.recete_id = 8
ORDER BY i.ilac_adi;

-- Sorgu 3: Reçetenin hastası ve doktoru (zincir JOIN)
-- Reçetede hasta_id ve doktor_id tutmuyoruz. Bu bilgileri
-- recete -> muayene -> randevu -> hasta / doktor zinciri üzerinden buluyoruz.
SELECT r.recete_id,
       r.recete_tarihi,
       h.ad || ' ' || h.soyad                 AS hasta,
       d.unvan || ' ' || d.ad || ' ' || d.soyad AS doktor,
       b.bolum_adi
FROM recete r
JOIN muayene m ON m.muayene_id = r.muayene_id
JOIN randevu ra ON ra.randevu_id = m.randevu_id
JOIN hasta h ON h.hasta_id = ra.hasta_id
JOIN doktor d ON d.doktor_id = ra.doktor_id
JOIN bolum b ON b.bolum_id = d.bolum_id
ORDER BY r.recete_id;

-- Sorgu 4: HAVING örneği - en az 3 reçetede yazılan ilaçlar
-- WHERE gruplamadan önce satırları, HAVING ise gruplamadan sonra grupları süzer.
SELECT i.ilac_adi,
       COUNT(*) AS recete_sayisi
FROM recete_ilac ri
JOIN ilac i ON i.ilac_id = ri.ilac_id
GROUP BY i.ilac_id, i.ilac_adi
HAVING COUNT(*) >= 3
ORDER BY recete_sayisi DESC;

-- Sorgu 5: Alt sorgu (subquery) örneği - ortalamadan fazla ilaç içeren reçeteler
-- İçteki sorgu reçete başına ortalama ilaç sayısını hesaplar,
-- dıştaki sorgu bu ortalamadan fazla ilacı olan reçeteleri getirir.
SELECT ri.recete_id,
       COUNT(*) AS ilac_sayisi
FROM recete_ilac ri
GROUP BY ri.recete_id
HAVING COUNT(*) > (
    SELECT AVG(adet)
    FROM (SELECT COUNT(*) AS adet
          FROM recete_ilac
          GROUP BY recete_id) AS recete_basina
)
ORDER BY ilac_sayisi DESC, ri.recete_id;

-- Sorgu 6: VIEW örneği - 3 numaralı hastaya yazılmış tüm ilaçlar
-- recete_detay görünümü sql/04_ilac_recete.sql dosyasında tablolarla birlikte oluşturuluyor.
-- Görünüm reçete, muayene, randevu, hasta, doktor ve ilaç tablolarını birleştiren uzun JOIN'i
-- saklıyor. Burada onu tek bir tablo gibi kısa bir SELECT ile kullanıyoruz.
SELECT recete_id, recete_tarihi, doktor, ilac_adi, doz
FROM recete_detay
WHERE hasta_id = 3
ORDER BY recete_tarihi, ilac_adi;
