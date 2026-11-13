# Kurulum Rehberi

Bu dosya, projeyi kendi bilgisayarında çalıştırmak isteyenler için kısa bir kurulum notu. Adımlar Windows'a göre yazıldı.

## 1. PostgreSQL ve pgAdmin

1. postgresql.org adresinden Download > Windows > "Download the installer" yolunu izle ve en güncel kararlı sürümü indir (biz 18.7 kurduk).
2. Kurulumda şu bileşenler işaretli olsun: PostgreSQL Server, pgAdmin 4, Command Line Tools. Stack Builder'a gerek yok.
3. `postgres` kullanıcısı için bir şifre belirle ve bir yere not et. Unutursan kurulumu baştan yapmak gerekebilir.
4. Port 5432 olarak kalsın, dil ayarı da varsayılan kalsın.
5. Kurulumu bitir.

## 2. Veritabanını oluşturma

pgAdmin ile:

1. pgAdmin'i aç, soldan Servers > PostgreSQL'e tıkla ve kurulumda belirlediğin şifreyi gir.
2. Databases'e sağ tıkla, Create > Database'i seç.
3. Database alanına `hastane_randevu` yaz, Save'e bas.

SQL ile (Query Tool'da):

```sql
CREATE DATABASE hastane_randevu;
```

Query Tool için `postgres` veritabanına sağ tıklayıp Query Tool'u açman yeterli. Tablolar sonraki adımda oluşturulacak, şimdilik veritabanı boş kalacak.

## 3. Python ve psycopg2

Python yüklü mü diye komut istemine şunu yaz:

```
python --version
```

Hata alırsan python.org adresinden Python'u indir ve kur. Kurulumun ilk ekranındaki "Add Python to PATH" kutusunu işaretlemeyi unutma.

Sonra kütüphaneyi kur:

```
python -m pip install psycopg2-binary
```

Not: Windows'ta sadece `pip install` yazınca "pip bulunamadı" hatası alınabiliyor, o yüzden `python -m pip` şeklinde yazmak daha garanti.

## 4. Bağlantı testi

Aşağıdaki kodu `baglanti_testi.py` adıyla kendi bilgisayarında bir yere kaydet. Şifreni kendi yazıyorsun, bu dosyayı GitHub'a yüklemeyin.

```python
import psycopg2

baglanti = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="hastane_randevu",
    user="postgres",
    password="SIFREN",
)

imlec = baglanti.cursor()
imlec.execute("SELECT version();")
print(imlec.fetchone()[0])

imlec.close()
baglanti.close()
```

Çalıştır:

```
python baglanti_testi.py
```

Ekrana PostgreSQL sürümü yazıyorsa her şey tamam.

## Mac için küçük notlar

- Komutlar `python3` ve `pip3` olarak geçiyor.
- Mac'te pip sistem geneline kurulum yaptırmayabilir. Bu durumda `python3 -m venv venv` ile bir ortam oluşturup `venv/bin/pip install psycopg2-binary` komutunu kullan.
- pgAdmin 4, `/Library/PostgreSQL/18` klasörünün içinde.
