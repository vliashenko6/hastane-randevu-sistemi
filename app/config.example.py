# Veritabanı bağlantı ayarları (örnek dosya)
# Hazırlayan: Veronika
#
# Kullanım: Bu dosyanın bir kopyasını aynı klasörde "config.py" adıyla oluştur
# ve "password" kısmına kendi postgres şifreni yaz.
# config.py .gitignore'da olduğu için şifren GitHub'a yüklenmez.

DB_AYARLARI = {
    "host": "localhost",
    "port": 5432,
    "dbname": "hastane_randevu",
    "user": "postgres",
    "password": "SIFRENI_BURAYA_YAZ",
}
