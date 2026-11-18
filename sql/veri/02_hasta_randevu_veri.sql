-- Hasta ve randevu örnek verileri (15 hasta, 25 randevu)
-- Önce sql/veri/01_bolum_doktor_veri.sql çalışmalı (doktor_id 1-10 kullanılıyor).
-- id'ler SERIAL ile sırayla verilir (1, 2, 3...).

-- 15 hasta (TC numaraları uydurmadır)
INSERT INTO hasta (tc_no, ad, soyad, dogum_tarihi, cinsiyet, telefon, adres) VALUES
    ('10000000146', 'Ahmet',   'Yılmaz',   '1985-03-12', 'E', '05321110001', 'Kadıköy, İstanbul'),    -- 1
    ('10000000248', 'Ayşe',    'Kara',     '1990-07-25', 'K', '05321110002', 'Üsküdar, İstanbul'),    -- 2
    ('10000000350', 'Mehmet',  'Öztürk',   '1972-11-03', 'E', '05321110003', NULL),                   -- 3
    ('10000000452', 'Fatma',   'Aksoy',    '1965-01-30', 'K', '05321110004', 'Beşiktaş, İstanbul'),   -- 4
    ('10000000554', 'Mustafa', 'Doğan',    '1980-09-14', 'E', '05321110005', 'Ataşehir, İstanbul'),   -- 5
    ('10000000656', 'Emine',   'Çetin',    '1958-05-21', 'K', '05321110006', 'Maltepe, İstanbul'),    -- 6
    ('10000000758', 'Ali',     'Erdem',    '2001-12-08', 'E', '05321110007', NULL),                   -- 7
    ('10000000860', 'Zeynep',  'Güneş',    '1995-04-17', 'K', '05321110008', 'Şişli, İstanbul'),      -- 8
    ('10000000962', 'Hasan',   'Yıldırım', '2010-08-02', 'E', '05321110009', 'Pendik, İstanbul'),     -- 9
    ('10000001064', 'Elif',    'Kurt',     '1988-02-27', 'K', '05321110010', 'Bakırköy, İstanbul'),   -- 10
    ('10000001166', 'Hüseyin', 'Acar',     '1950-10-10', 'E', '05321110011', 'Kartal, İstanbul'),     -- 11
    ('10000001268', 'Merve',   'Tekin',    '1999-06-19', 'K', '05321110012', NULL),                   -- 12
    ('10000001360', 'İbrahim', 'Bulut',    '1975-03-05', 'E', '05321110013', 'Sarıyer, İstanbul'),    -- 13
    ('10000001462', 'Hatice',  'Şimşek',   '1968-12-24', 'K', '05321110014', 'Beykoz, İstanbul'),     -- 14
    ('10000001564', 'Emre',    'Aslan',    '2005-09-09', 'E', '05321110015', 'Ümraniye, İstanbul');   -- 15

-- 25 randevu
INSERT INTO randevu (hasta_id, doktor_id, randevu_tarihi, randevu_saati, durum) VALUES
    -- 1-15: tamamlanan randevular (3-14 Kasım 2026)
    (1,  1,  '2026-11-03', '09:00', 'tamamlandi'),  -- 1
    (2,  1,  '2026-11-03', '09:30', 'tamamlandi'),  -- 2
    (3,  3,  '2026-11-04', '10:00', 'tamamlandi'),  -- 3
    (4,  4,  '2026-11-04', '11:00', 'tamamlandi'),  -- 4
    (5,  5,  '2026-11-05', '14:00', 'tamamlandi'),  -- 5
    (6,  6,  '2026-11-05', '15:30', 'tamamlandi'),  -- 6
    (7,  7,  '2026-11-06', '09:00', 'tamamlandi'),  -- 7
    (8,  8,  '2026-11-06', '10:30', 'tamamlandi'),  -- 8
    (9,  9,  '2026-11-09', '13:00', 'tamamlandi'),  -- 9
    (10, 10, '2026-11-09', '11:30', 'tamamlandi'),  -- 10
    (11, 2,  '2026-11-10', '09:00', 'tamamlandi'),  -- 11
    (12, 3,  '2026-11-10', '10:00', 'tamamlandi'),  -- 12
    (13, 6,  '2026-11-11', '16:30', 'tamamlandi'),  -- 13
    (14, 8,  '2026-11-12', '14:30', 'tamamlandi'),  -- 14
    (15, 4,  '2026-11-13', '09:30', 'tamamlandi'),  -- 15
    -- 16-20: iptal edilen randevular
    (1,  2,  '2026-11-23', '09:00', 'iptal'),       -- 16
    (2,  5,  '2026-11-24', '10:00', 'iptal'),       -- 17
    (3,  7,  '2026-11-25', '11:00', 'iptal'),       -- 18
    (4,  1,  '2026-12-01', '09:00', 'iptal'),       -- 19 (21 ile aynı saat, iptal olduğu için çakışmaz)
    (5,  9,  '2026-11-30', '14:00', 'iptal'),       -- 20
    -- 21-25: aktif randevular (1-5 Aralık 2026)
    (6,  1,  '2026-12-01', '09:00', 'aktif'),       -- 21
    (7,  3,  '2026-12-02', '10:00', 'aktif'),       -- 22
    (8,  5,  '2026-12-03', '14:30', 'aktif'),       -- 23
    (9,  7,  '2026-12-04', '11:00', 'aktif'),       -- 24
    (10, 9,  '2026-12-05', '09:30', 'aktif');       -- 25

-- Test sorguları (başındaki -- işaretini kaldırıp tek tek çalıştır, ikisi de hata vermeli)

-- 1) Çift randevu: doktor 1'in 1 Aralık 09:00 saatinde zaten aktif randevusu var
-- INSERT INTO randevu (hasta_id, doktor_id, randevu_tarihi, randevu_saati)
-- VALUES (11, 1, '2026-12-01', '09:00');

-- 2) Aynı TC ile ikinci hasta: 10000000146 zaten kayıtlı
-- INSERT INTO hasta (tc_no, ad, soyad, dogum_tarihi, cinsiyet, telefon)
-- VALUES ('10000000146', 'Deneme', 'Kişi', '1990-01-01', 'E', '05320000000');
