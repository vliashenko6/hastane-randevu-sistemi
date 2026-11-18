-- Veritabanını baştan kuran ana dosya
-- Hazırlayan: Veronika
--
-- Tüm tabloları ve örnek verileri doğru sırayla oluşturur.
-- Sıra önemli: bir tablo, bağlı olduğu tablodan sonra oluşturulmalı.
--
-- Çalıştırma (psql ile, sql klasörünün bulunduğu yerden):
--   psql -U postgres -d hastane_randevu -f sql/00_kurulum.sql
--
-- pgAdmin ile çalıştırılacaksa: aşağıdaki "Eski tabloları sil" kısmını çalıştırın,
-- sonra dosyaları Query Tool'da tek tek bu sırayla açıp çalıştırın.

\set ON_ERROR_STOP on
-- Dosyalar UTF-8 kaydedildi; Türkçe karakterler bozulmasın diye (özellikle Windows'ta)
SET client_encoding TO 'UTF8';

-- Eski tabloları sil (dosya ikinci kez çalıştırılırsa baştan kurulsun diye)
DROP TABLE IF EXISTS recete_ilac, recete, ilac, muayene_teshis, teshis,
                     muayene, randevu, hasta, doktor, bolum CASCADE;
DROP FUNCTION IF EXISTS muayene_randevu_tamamla() CASCADE;

-- 1-2: bölüm ve doktor (Sude)
\ir 01_bolum_doktor.sql
\ir veri/01_bolum_doktor_veri.sql

-- 3-4: hasta ve randevu (Eray)
\ir 02_hasta_randevu.sql
\ir veri/02_hasta_randevu_veri.sql

-- 5-6: muayene, teşhis ve muayene_teshis (Sude)
\ir 03_muayene_teshis.sql
\ir veri/03_muayene_teshis_veri.sql

-- 7-8: ilaç, reçete ve recete_ilac (Veronika)
\ir 04_ilac_recete.sql
\ir veri/04_ilac_recete_veri.sql
