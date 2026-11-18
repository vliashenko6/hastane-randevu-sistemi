-- Hasta ve randevu tabloları
-- Çalıştırma sırası: 2. dosya (önce 01_bolum_doktor.sql çalışmalı, randevu doktor tablosuna bağlı).
-- Örnek veriler sql/veri/02_hasta_randevu_veri.sql dosyasında.

-- Hastaların kimlik ve iletişim bilgileri.
-- tc_no 11 rakam olmalı ve tekrar edemez, doğum tarihi gelecekte olamaz.
CREATE TABLE hasta (
    hasta_id      SERIAL PRIMARY KEY,
    tc_no         CHAR(11)     NOT NULL UNIQUE CHECK (tc_no ~ '^[0-9]{11}$'),
    ad            VARCHAR(50)  NOT NULL,
    soyad         VARCHAR(50)  NOT NULL,
    dogum_tarihi  DATE         NOT NULL CHECK (dogum_tarihi <= CURRENT_DATE),
    cinsiyet      CHAR(1)      NOT NULL CHECK (cinsiyet IN ('E', 'K')),
    telefon       VARCHAR(20)  NOT NULL,
    adres         VARCHAR(200)
);

-- Hasta ile doktor arasındaki randevular.
-- Randevusu olan hasta silinemez (RESTRICT).
-- İptal edilen randevu silinmez, durumu 'iptal' olur.
CREATE TABLE randevu (
    randevu_id      SERIAL PRIMARY KEY,
    hasta_id        INTEGER     NOT NULL REFERENCES hasta (hasta_id) ON DELETE RESTRICT,
    doktor_id       INTEGER     NOT NULL REFERENCES doktor (doktor_id),
    randevu_tarihi  DATE        NOT NULL,
    randevu_saati   TIME        NOT NULL,
    durum           VARCHAR(10) NOT NULL DEFAULT 'aktif'
                    CHECK (durum IN ('aktif', 'iptal', 'tamamlandi'))
);

-- Çift randevu engeli: iptal edilmemiş randevularda aynı doktor, tarih ve saat tekrar edemez.
-- Kısmi indeks olduğu için iptal edilen bir saate yeniden randevu verilebilir.
CREATE UNIQUE INDEX uq_cift_randevu
    ON randevu (doktor_id, randevu_tarihi, randevu_saati)
    WHERE durum <> 'iptal';

-- Not: "geçmiş tarihe randevu verilemez" kuralını veritabanına koymadık.
-- Örnek verilerde geçmiş tarihli tamamlanmış randevular var.
-- Bu kontrolü ileride Python uygulaması yapacak.
