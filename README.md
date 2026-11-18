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

- `sql/` → tablo oluşturma, veri ekleme ve sorgu dosyaları
- `app/` → Python uygulaması
- `docs/` → diyagramlar, proje planı ve notlar
- `rapor/` → proje raporu

## Ekip

- Veronika – reçete ve ilaç kısmı, veritabanı bağlantısı, ana menü
- Eray – hasta ve randevu kısmı
- Sude – doktor, bölüm ve muayene kısmı

İş dağılımı: [docs/Hastane_Randevu_Proje_Plani.pdf](docs/Hastane_Randevu_Proje_Plani.pdf)
