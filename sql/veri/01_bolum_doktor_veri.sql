-- Bölüm ve doktor örnek verileri (5 bölüm, 10 doktor)
-- Hazırlayan: Sude
-- Çalıştırma sırası: 2. dosya (önce sql/01_bolum_doktor.sql çalışmalı)
-- id'ler açıkça yazılıyor, en sonda setval ile sayaçlar ayarlanıyor.

INSERT INTO bolum (bolum_id, bolum_adi) VALUES
    (1, 'Kardiyoloji'),
    (2, 'Dahiliye'),
    (3, 'Ortopedi'),
    (4, 'Göz Hastalıkları'),
    (5, 'Kulak Burun Boğaz');

INSERT INTO doktor (doktor_id, bolum_id, ad, soyad, unvan, telefon) VALUES
    (1, 1, 'Hakan', 'Aydın',  'Prof. Dr.', '02160000101'),
    (2, 1, 'Elif',  'Yıldız', 'Doç. Dr.',  '02160000102'),
    (3, 2, 'Murat', 'Kaya',   'Uzm. Dr.',  '02160000103'),
    (4, 2, 'Selin', 'Demir',  'Uzm. Dr.',  NULL),
    (5, 3, 'Cem',   'Şahin',  'Prof. Dr.', '02160000105'),
    (6, 3, 'Zeynep','Arslan', 'Uzm. Dr.',  NULL),
    (7, 4, 'Burak', 'Çelik',  'Uzm. Dr.',  '02160000107'),
    (8, 4, 'Aylin', 'Koç',    'Doç. Dr.',  '02160000108'),
    (9, 5, 'Oğuz',  'Polat',  'Uzm. Dr.',  '02160000109'),
    (10, 5, 'Deniz', 'Yalçın', 'Op. Dr.',   '02160000110');

SELECT setval(pg_get_serial_sequence('bolum', 'bolum_id'), (SELECT MAX(bolum_id) FROM bolum));
SELECT setval(pg_get_serial_sequence('doktor', 'doktor_id'), (SELECT MAX(doktor_id) FROM doktor));
