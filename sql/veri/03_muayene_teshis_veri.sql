-- Teşhis kataloğu, muayene ve muayene_teshis örnek verileri
-- Hazırlayan: Sude
-- Çalıştırma sırası: 6. dosya (önce sql/03_muayene_teshis.sql ve sql/veri/02_hasta_randevu_veri.sql çalışmalı)
-- Muayene 1-15, tamamlanmış randevu 1-15 için.

INSERT INTO teshis (teshis_kodu, teshis_adi) VALUES
    ('J06.9', 'Akut üst solunum yolu enfeksiyonu'),
    ('J03.9', 'Akut tonsillit'),
    ('I10',   'Esansiyel (primer) hipertansiyon'),
    ('I20.9', 'Anjina pektoris'),
    ('R07.4', 'Göğüs ağrısı'),
    ('E11.9', 'Tip 2 diabetes mellitus'),
    ('K29.7', 'Gastrit'),
    ('M54.5', 'Bel ağrısı'),
    ('M17.9', 'Diz osteoartriti'),
    ('H52.1', 'Miyopi'),
    ('H10.9', 'Konjonktivit'),
    ('R00.2', 'Çarpıntı'),
    ('R11',   'Bulantı ve kusma'),
    ('J01.9', 'Akut sinüzit'),
    ('H66.9', 'Otitis media');

-- Muayene tarihi, bağlı olduğu randevunun tarihiyle aynı alınır.
INSERT INTO muayene (muayene_id, randevu_id, muayene_tarihi, sikayet, notlar)
SELECT v.muayene_id, v.randevu_id, r.randevu_tarihi, v.sikayet, v.notlar
FROM (VALUES
    (1,  1,  'Göğüs ağrısı ve çarpıntı',                'Efor testi istendi.'),
    (2,  2,  'Tansiyon yüksekliği ve baş ağrısı',       'İlaç tedavisi başlandı.'),
    (3,  3,  'Halsizlik ve sık idrara çıkma',           'Kan şekeri yüksek, diyet önerildi.'),
    (4,  4,  'Mide yanması ve bulantı',                 NULL),
    (5,  5,  'Bel ağrısı',                              'Fizik tedavi önerildi.'),
    (6,  6,  'Dizde ağrı, merdiven çıkarken zorlanma',  NULL),
    (7,  7,  'Uzağı net görememe',                      'Gözlük yazıldı.'),
    (8,  8,  'Gözde kızarıklık ve sulanma',             'Göz damlası yazıldı.'),
    (9,  9,  'Boğaz ağrısı ve ateş',                    'Dinlenme ve bol sıvı önerildi.'),
    (10, 10, 'Öksürük ve burun akıntısı',               NULL),
    (11, 11, 'Yürürken gelen göğüs ağrısı',             'EKG ve efor testi istendi.'),
    (12, 12, 'Mide ağrısı ve bulantı',                  'Baharatlı yemekten kaçınması söylendi.'),
    (13, 13, 'Bel ağrısı, öne eğilince artıyor',        'Egzersiz önerildi.'),
    (14, 14, 'Uzağı bulanık görme',                     'Gözlük numarası arttı.'),
    (15, 15, 'Ateş, öksürük ve halsizlik',              NULL)
) AS v(muayene_id, randevu_id, sikayet, notlar)
JOIN randevu r ON r.randevu_id = v.randevu_id;

INSERT INTO muayene_teshis (muayene_id, teshis_kodu, aciklama) VALUES
    (1,  'R07.4', 'Kalp kaynaklı olup olmadığı test ile bakılacak'),
    (1,  'R00.2', NULL),
    (1,  'I20.9', 'Ön tanı, efor testi sonucuna göre kesinleşecek'),
    (2,  'I10',   NULL),
    (2,  'R00.2', 'Tansiyon yükseldiğinde oluyor'),
    (3,  'E11.9', NULL),
    (3,  'I10',   'Şeker hastalığına eşlik ediyor'),
    (4,  'K29.7', NULL),
    (4,  'R11',   NULL),
    (5,  'M54.5', NULL),
    (6,  'M17.9', 'Sağ diz'),
    (6,  'M54.5', 'Hafif bel ağrısı da var'),
    (7,  'H52.1', NULL),
    (8,  'H10.9', NULL),
    (8,  'J06.9', 'Soğuk algınlığı ile birlikte başlamış'),
    (9,  'J03.9', NULL),
    (9,  'J06.9', NULL),
    (9,  'H66.9', 'Sol kulak'),
    (10, 'J06.9', NULL),
    (10, 'J01.9', NULL),
    (11, 'I20.9', 'Ön tanı, tetkik sonucuna göre kesinleşecek'),
    (11, 'I10',   NULL),
    (12, 'K29.7', NULL),
    (12, 'R11',   NULL),
    (13, 'M54.5', NULL),
    (14, 'H52.1', NULL),
    (15, 'J06.9', NULL);

-- Test: aynı teşhis aynı muayeneye ikinci kez eklenemez.
-- Çalıştırınca birincil anahtar (pk_muayene_teshis) hatası vermesi beklenir.
-- INSERT INTO muayene_teshis (muayene_id, teshis_kodu) VALUES (2, 'I10');

SELECT setval(pg_get_serial_sequence('muayene', 'muayene_id'), (SELECT MAX(muayene_id) FROM muayene));
