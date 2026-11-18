-- İlaç, reçete ve recete_ilac örnek verileri
-- Hazırlayan: Veronika
-- Çalıştırma sırası: 8. dosya (önce sql/04_ilac_recete.sql ve sql/veri/03_muayene_teshis_veri.sql çalışmalı)
-- 13 reçete var. Muayene 7 ve 14'te (miyopi) gözlük yazıldığı için ilaç reçetesi yok,
-- yani her muayenede reçete yazılmak zorunda değil.

INSERT INTO ilac (ilac_id, ilac_adi, etken_madde, ilac_formu) VALUES
    (1,  'Parol 500 mg',             'Parasetamol',                          'tablet'),
    (2,  'Majezik 100 mg',           'Flurbiprofen',                         'tablet'),
    (3,  'Augmentin BID 1000 mg',    'Amoksisilin + Klavulanik asit',        'tablet'),
    (4,  'Coraspin 100 mg',          'Asetilsalisilik asit',                 'tablet'),
    (5,  'Beloc ZOK 50 mg',          'Metoprolol',                           'tablet'),
    (6,  'Norvasc 5 mg',             'Amlodipin',                            'tablet'),
    (7,  'Glifor 1000 mg',           'Metformin',                            'tablet'),
    (8,  'Nexium 40 mg',             'Esomeprazol',                          'tablet'),
    (9,  'Metpamid 10 mg',           'Metoklopramid',                        'tablet'),
    (10, 'Arveles 25 mg',            'Deksketoprofen',                       'tablet'),
    (11, 'Voltaren Emulgel',         'Diklofenak',                           'jel'),
    (12, 'Tobradex göz damlası',     'Tobramisin + Deksametazon',            'damla'),
    (13, 'Otosporin kulak damlası',  'Neomisin + Polimiksin + Hidrokortizon', 'damla'),
    (14, 'Iliadin burun spreyi',     'Oksimetazolin',                        'sprey'),
    (15, 'Tantum Verde gargara',     'Benzidamin',                           'gargara');

-- Reçete tarihi, bağlı olduğu muayenenin tarihiyle aynı alınır.
INSERT INTO recete (recete_id, muayene_id, recete_tarihi, aciklama)
SELECT v.recete_id, v.muayene_id, m.muayene_tarihi, v.aciklama
FROM (VALUES
    (1,  1,  'Efor testi sonucuna göre tedavi düzenlenecek.'),
    (2,  2,  NULL),
    (3,  3,  'Diyete dikkat etmesi söylendi.'),
    (4,  4,  NULL),
    (5,  5,  NULL),
    (6,  6,  'Jel ağrıyan bölgeye sürülecek.'),
    (7,  8,  NULL),
    (8,  9,  'Antibiyotik kutusu bitene kadar kullanılacak.'),
    (9,  10, NULL),
    (10, 11, NULL),
    (11, 12, 'Baharatlı yemekten kaçınılacak.'),
    (12, 13, NULL),
    (13, 15, NULL)
) AS v(recete_id, muayene_id, aciklama)
JOIN muayene m ON m.muayene_id = v.muayene_id;

INSERT INTO recete_ilac (recete_id, ilac_id, doz, kullanim_sekli, kutu_adedi) VALUES
    (1,  4,  '1x1', 'Sabah, tok karnına',           1),
    (1,  5,  '1x1', 'Sabah',                        1),
    (2,  6,  '1x1', 'Sabah',                        2),
    (3,  7,  '2x1', 'Sabah ve akşam, yemekle',      2),
    (3,  6,  '1x1', 'Sabah',                        1),
    (4,  8,  '1x1', 'Sabah, aç karnına',            1),
    (4,  9,  '3x1', 'Yemeklerden önce',             1),
    (5,  10, '2x1', 'Tok karnına',                  1),
    (5,  11, '3x1', 'Ağrıyan bölgeye sürülecek',    1),
    (6,  2,  '2x1', 'Tok karnına',                  1),
    (6,  11, '3x1', 'Dize sürülecek',               1),
    (7,  12, '4x1', 'Her iki göze birer damla',     1),
    (7,  1,  '3x1', 'Ateş olursa',                  1),
    (8,  3,  '2x1', 'Sabah ve akşam, tok karnına',  1),
    (8,  1,  '3x1', 'Ateş ve ağrı olursa',          1),
    (8,  13, '3x1', 'Sol kulağa üçer damla',        1),
    (8,  15, '3x1', 'Gargara yapılacak',            1),
    (9,  3,  '2x1', 'Sabah ve akşam, tok karnına',  1),
    (9,  14, '2x1', 'Her burun deliğine bir sıkım', 1),
    (9,  1,  '3x1', 'Ateş olursa',                  1),
    (10, 4,  '1x1', 'Sabah, tok karnına',           1),
    (10, 5,  '1x1', 'Sabah',                        1),
    (10, 6,  '1x1', 'Sabah',                        1),
    (11, 8,  '1x1', 'Sabah, aç karnına',            1),
    (11, 9,  '3x1', 'Yemeklerden önce',             1),
    (12, 10, '2x1', 'Tok karnına',                  1),
    (13, 1,  '3x1', 'Ateş olursa',                  1),
    (13, 15, '3x1', 'Gargara yapılacak',            1);

-- Testler (başındaki -- silinip çalıştırılırsa hata vermesi beklenir):
-- Aynı ilaç aynı reçeteye ikinci kez eklenemez (pk_recete_ilac):
-- INSERT INTO recete_ilac (recete_id, ilac_id, doz) VALUES (1, 4, '1x1');
-- Aynı muayeneye ikinci reçete yazılamaz (uq_recete_muayene):
-- INSERT INTO recete (muayene_id) VALUES (1);
-- Kutu adedi en az 1 olmalı (ck_recete_ilac_kutu):
-- INSERT INTO recete_ilac (recete_id, ilac_id, doz, kutu_adedi) VALUES (2, 1, '1x1', 0);

-- Açıkça id yazdığımız için sayaçları en büyük id'ye getiriyoruz,
-- yoksa uygulamadan eklenen ilk kayıt id=1 almaya çalışır ve hata verir.
SELECT setval(pg_get_serial_sequence('ilac', 'ilac_id'), (SELECT MAX(ilac_id) FROM ilac));
SELECT setval(pg_get_serial_sequence('recete', 'recete_id'), (SELECT MAX(recete_id) FROM recete));
