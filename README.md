# Hastane Randevu Sistemi

BİM 381 Veri Tabanı Sistemleri dersi için hazırladığımız grup projesi.

Projede hayali bir müşteri olarak Doğuş Özel Hastanesi'ni seçtik. Hastanede randevular telefonla alınıp kâğıda yazılıyor. Bu yüzden aynı doktora aynı saatte iki randevu verilebiliyor, hastanın önceki muayenelerine ulaşmak zor oluyor ve reçeteler takip edilemiyor. Biz de bu bilgileri tek bir veritabanında tutan basit bir randevu sistemi yapmaya karar verdik.

## Neler yapılabilecek?

- Hasta kaydı ve hasta arama
- Bölüm ve doktor seçip randevu alma, randevu iptali
- Doktorun o günkü randevularını görmesi
- Muayene ve teşhis kaydı
- Reçete yazma (bir reçetede birden fazla ilaç)
- Bazı istatistikler (en çok yazılan ilaç, bölümlere göre hasta sayısı vb.)

## Tablolar

hasta, randevu, bolum, doktor, muayene, teshis, muayene_teshis, ilac, recete, recete_ilac

İki tane çoka çok ilişki var: reçete ile ilaç arasındakini recete_ilac, muayene ile teşhis arasındakini muayene_teshis tablosuyla bağlıyoruz.

## Kullandıklarımız

PostgreSQL, Python (psycopg2), Tkinter

## Klasörler

- `sql/` → tablo oluşturma dosyaları (CREATE TABLE) ve hepsini kuran `00_kurulum.sql`
  - `sql/veri/` → örnek veriler (INSERT)
  - `sql/sorgular/` → bilgi alma sorguları (SELECT)
- `app/` → Python uygulaması
- `docs/` → gereksinimler, ER ve UML diyagramları, ilişkisel şema, proje planı
- `rapor/` → proje raporu

## Kurulum

1. PostgreSQL ve Python kurulumu için: [docs/kurulum.md](docs/kurulum.md)
2. `hastane_randevu` adında boş bir veritabanı oluştur.
3. Repo klasöründe şu komutla bütün tabloları ve örnek verileri kur:

```
psql -U postgres -d hastane_randevu -f sql/00_kurulum.sql
```

Dosya eski tabloları silip her şeyi baştan kurar, yani istendiği kadar tekrar çalıştırılabilir. pgAdmin kullanılacaksa dosyaları `00_kurulum.sql` içinde yazan sırayla Query Tool'da tek tek çalıştırmak gerekir.

## Ekip

- Veronika – reçete ve ilaç kısmı, veritabanı bağlantısı, ana menü
- Eray – hasta ve randevu kısmı
- Sude – bölüm, doktor, muayene ve teşhis kısmı

İş dağılımı: [docs/Hastane_Randevu_Proje_Plani.pdf](docs/Hastane_Randevu_Proje_Plani.pdf)
