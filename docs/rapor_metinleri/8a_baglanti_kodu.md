# 8a- Uygulama ve Veritabanı Arasındaki Bağlantı Kodu Örneği

Hazırlayan: Veronika

Uygulama Python ile yazıldı ve PostgreSQL veritabanına **psycopg2** kütüphanesiyle bağlanıyor. Bağlantıyla ilgili bütün kodu tek bir dosyada, `app/db.py` içindeki `Veritabani` sınıfında topladık. Böylece ekranların hiçbiri doğrudan bağlantı kurmuyor; hepsi aynı `db` nesnesini kullanıyor. Bağlantı ayarları değişirse sadece bir yeri düzeltmek yetiyor ve hata mesajları her ekranda aynı oluyor.

## Bağlantı ayarları

Bağlantı bilgileri `app/config.py` dosyasında duruyor. Bu dosya şifre içerdiği için GitHub'a yüklenmiyor (`.gitignore`). Repoda sadece örneği (`config.example.py`) var; her ekip üyesi kendi şifresiyle kendi `config.py` dosyasını oluşturuyor.

```python
DB_AYARLARI = {
    "host": "localhost",      # veritabanı bu bilgisayarda
    "port": 5432,             # PostgreSQL'in varsayılan portu
    "dbname": "hastane_randevu",
    "user": "postgres",
    "password": "...",
}
```

## Bağlantı sınıfı (app/db.py, kısaltılmış)

```python
import psycopg2
from config import DB_AYARLARI


class Veritabani:
    def __init__(self, ayarlar=None):
        self.ayarlar = ayarlar or DB_AYARLARI
        self.baglanti = None

    def baglan(self):
        # bağlantı yoksa ya da kopmuşsa yeniden bağlan
        if self.baglanti is None or self.baglanti.closed:
            self.baglanti = psycopg2.connect(**self.ayarlar)
        return self.baglanti

    def _yurut(self, sql, parametreler, sonuc):
        baglanti = self.baglan()
        try:
            with baglanti.cursor() as imlec:
                imlec.execute(sql, parametreler)      # sorguyu gönder
                if sonuc == "hepsi":
                    veri = imlec.fetchall()            # bütün satırlar
                elif sonuc == "tek":
                    veri = imlec.fetchone()            # tek satır
                elif sonuc == "id":
                    veri = imlec.fetchone()[0]         # RETURNING ile gelen yeni id
                else:
                    veri = imlec.rowcount              # etkilenen satır sayısı
            baglanti.commit()                          # başarılıysa kaydet
            return veri
        except psycopg2.Error:
            baglanti.rollback()                        # hata varsa geri al
            raise

    def getir(self, sql, parametreler=None):
        return self._yurut(sql, parametreler, "hepsi")

    def getir_tek(self, sql, parametreler=None):
        return self._yurut(sql, parametreler, "tek")

    def calistir(self, sql, parametreler=None):
        return self._yurut(sql, parametreler, "adet")

    def ekle(self, sql, parametreler=None):
        return self._yurut(sql, parametreler, "id")


db = Veritabani()    # bütün ekranların kullandığı ortak nesne
```

Kodun çalışma sırası:

1. `psycopg2.connect()` config.py'deki bilgilerle veritabanına bağlanır.
2. `cursor()` ile bir imleç açılır, `execute()` SQL sorgusunu veritabanına gönderir.
3. SELECT sorgularında sonuçlar `fetchall()` / `fetchone()` ile Python'a gelir.
4. İşlem başarılıysa `commit()` ile kaydedilir. Bir kural bozulursa (örneğin çift randevu) PostgreSQL hata verir, `rollback()` ile işlem geri alınır ve hata ekrana iletilir.

## Ekranda kullanım örneği (reçeteye ilaç ekleme)

```python
from db import db

try:
    db.calistir(
        "INSERT INTO recete_ilac (recete_id, ilac_id, doz, kullanim_sekli, kutu_adedi) "
        "VALUES (%s, %s, %s, %s, %s)",
        (recete_id, ilac_id, doz, kullanim_sekli, kutu))
except psycopg2.Error as hata:
    messagebox.showerror("İlaç", db.hata_mesaji(hata))
```

Değerler SQL metninin içine yazılmıyor, `%s` yer tutucularıyla ayrı olarak gönderiliyor. psycopg2 bu değerleri kendisi güvenli hâle getirdiği için kullanıcının girdiği bir yazı SQL komutu gibi çalıştırılamıyor (**SQL injection** saldırısına karşı koruma). Örneğin TC kutusuna `' OR '1'='1` yazıldığında bütün hastalar listelenmiyor, sonuç boş geliyor.

## Hata mesajları

PostgreSQL'in hata mesajları İngilizce ve teknik. `db.hata_mesaji(hata)` metodu hatanın kodunu ve hangi kısıtın bozulduğunu okuyup kullanıcıya Türkçe bir mesaj veriyor:

| Durum | Bozulan kural | Kullanıcının gördüğü mesaj |
|---|---|---|
| Aynı doktora aynı saatte ikinci randevu | uq_cift_randevu (benzersiz indeks) | Bu doktorun bu tarih ve saatte başka bir randevusu var. |
| Aynı TC ile ikinci hasta | hasta.tc_no UNIQUE | Bu TC kimlik numarasıyla kayıtlı bir hasta zaten var. |
| Aynı ilaç aynı reçeteye ikinci kez | pk_recete_ilac (bileşik anahtar) | Bu ilaç bu reçeteye zaten eklenmiş. |
| Reçetede kullanılmış ilacı silme | fk_recete_ilac_ilac (RESTRICT) | Bu kayda bağlı başka kayıtlar olduğu için silinemez. |
| Veritabanına ulaşılamıyor | bağlantı hatası | Veritabanına bağlanılamadı. PostgreSQL'in çalıştığını ve config.py'deki bilgileri kontrol edin. |

## Bağlantı testi

`app` klasöründe `python db.py` komutu çalıştırıldığında bağlantı test ediliyor: PostgreSQL sürümü ve her tablodaki kayıt sayısı ekrana yazılıyor.

```
PostgreSQL 18.6 on x86_64-windows, compiled by msvc-19.44.35229, 64-bit
bolum           5 kayıt
doktor          10 kayıt
hasta           15 kayıt
...
Bağlantı başarılı.
```
