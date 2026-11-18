"""Veritabanı bağlantı dosyası.

Hazırlayan: Veronika

Bütün ekranlar veritabanına bu dosyadaki Veritabani sınıfı üzerinden bağlanır.
Böylece bağlantı kodu her ekranda tekrar yazılmaz ve hata mesajları her yerde aynı olur.

Ekranlarda kullanımı:

    from db import db

    hastalar = db.getir("SELECT hasta_id, ad, soyad FROM hasta WHERE tc_no = %s", (tc,))
    hasta    = db.getir_tek("SELECT * FROM hasta WHERE hasta_id = %s", (hasta_id,))
    adet     = db.calistir("UPDATE randevu SET durum = 'iptal' WHERE randevu_id = %s", (rid,))
    yeni_id  = db.ekle("INSERT INTO bolum (bolum_adi) VALUES (%s) RETURNING bolum_id", (ad,))

Değerler SQL'in içine yazılmaz, her zaman %s ile parametre olarak verilir (SQL injection'a karşı).
Hata olursa psycopg2.Error fırlatılır; ekranda yakalanıp db.hata_mesaji(hata) ile kullanıcıya gösterilir.
"""

import psycopg2

try:
    from config import DB_AYARLARI
except ImportError:
    DB_AYARLARI = None


# Kısıt adına göre kullanıcıya gösterilecek Türkçe mesajlar
KISIT_MESAJLARI = {
    # benzersizlik (UNIQUE / PRIMARY KEY)
    "uq_cift_randevu": "Bu doktorun bu tarih ve saatte başka bir randevusu var.",
    "hasta_tc_no_key": "Bu TC kimlik numarasıyla kayıtlı bir hasta zaten var.",
    "uq_bolum_adi": "Bu isimde bir bölüm zaten var.",
    "uq_ilac_adi": "Bu isimde bir ilaç zaten var.",
    "uq_muayene_randevu": "Bu randevu için zaten bir muayene kaydı var.",
    "uq_recete_muayene": "Bu muayene için zaten bir reçete yazılmış.",
    "pk_recete_ilac": "Bu ilaç bu reçeteye zaten eklenmiş.",
    "pk_muayene_teshis": "Bu teşhis bu muayeneye zaten eklenmiş.",
    "pk_teshis": "Bu teşhis kodu zaten kayıtlı.",
    # kontrol (CHECK)
    "hasta_tc_no_check": "TC kimlik numarası 11 rakamdan oluşmalı.",
    "hasta_dogum_tarihi_check": "Doğum tarihi ileri bir tarih olamaz.",
    "hasta_cinsiyet_check": "Cinsiyet E ya da K olmalı.",
    "randevu_durum_check": "Randevu durumu aktif, iptal ya da tamamlandi olmalı.",
    "ck_recete_ilac_kutu": "Kutu adedi en az 1 olmalı.",
}


class Veritabani:
    """PostgreSQL bağlantısını yöneten sınıf."""

    def __init__(self, ayarlar=None):
        self.ayarlar = ayarlar or DB_AYARLARI
        self.baglanti = None

    def baglan(self):
        """Bağlantı yoksa ya da kopmuşsa yeniden bağlanır."""
        if self.baglanti is None or self.baglanti.closed:
            if not self.ayarlar:
                raise RuntimeError("app/config.py bulunamadı. config.example.py dosyasını "
                                   "config.py adıyla kopyalayıp şifreni yaz.")
            self.baglanti = psycopg2.connect(**self.ayarlar)
        return self.baglanti

    def _yurut(self, sql, parametreler, sonuc):
        """Sorguyu çalıştırır. Başarılıysa kaydeder (commit), hata olursa geri alır (rollback)."""
        baglanti = self.baglan()
        try:
            with baglanti.cursor() as imlec:
                imlec.execute(sql, parametreler)
                if sonuc == "hepsi":
                    veri = imlec.fetchall()
                elif sonuc == "tek":
                    veri = imlec.fetchone()
                elif sonuc == "id":
                    veri = imlec.fetchone()[0]
                else:
                    veri = imlec.rowcount
            baglanti.commit()
            return veri
        except psycopg2.Error:
            if not baglanti.closed:
                baglanti.rollback()
            raise

    def getir(self, sql, parametreler=None):
        """SELECT sorgusunun bütün satırlarını liste olarak döndürür."""
        return self._yurut(sql, parametreler, "hepsi")

    def getir_tek(self, sql, parametreler=None):
        """SELECT sorgusunun ilk satırını döndürür, sonuç yoksa None."""
        return self._yurut(sql, parametreler, "tek")

    def calistir(self, sql, parametreler=None):
        """INSERT / UPDATE / DELETE çalıştırır, etkilenen satır sayısını döndürür."""
        return self._yurut(sql, parametreler, "adet")

    def ekle(self, sql, parametreler=None):
        """'... RETURNING <id>' ile biten bir INSERT çalıştırır, yeni kaydın id'sini döndürür."""
        return self._yurut(sql, parametreler, "id")

    def kapat(self):
        if self.baglanti is not None and not self.baglanti.closed:
            self.baglanti.close()

    @staticmethod
    def hata_mesaji(hata):
        """psycopg2 hatasını kullanıcının anlayacağı Türkçe bir mesaja çevirir."""
        if isinstance(hata, RuntimeError):
            return str(hata)
        kod = getattr(hata, "pgcode", None)
        diag = getattr(hata, "diag", None)
        kisit = diag.constraint_name if diag is not None else None

        if kisit in KISIT_MESAJLARI:
            return KISIT_MESAJLARI[kisit]
        if kod is None:
            return ("Veritabanına bağlanılamadı. PostgreSQL'in çalıştığını ve "
                    "config.py'deki bilgileri kontrol edin.")
        if kod == "23505":
            return "Bu kayıt zaten var."
        if kod == "23001":
            return "Bu kayda bağlı başka kayıtlar olduğu için silinemez."
        if kod == "23503":
            detay = diag.message_detail if diag is not None else ""
            if detay and "still referenced" in detay:
                return "Bu kayda bağlı başka kayıtlar olduğu için silinemez."
            return "Seçilen kayıt bulunamadı."
        if kod == "23502":
            return "Zorunlu bir alan boş bırakıldı."
        if kod == "23514":
            return "Girilen değer kurallara uymuyor."
        if kod in ("22007", "22008"):
            return "Tarih ya da saat biçimi hatalı."
        if kod == "22P02":
            return "Sayı girilmesi gereken bir yere farklı bir değer girildi."
        if kod == "22001":
            return "Girilen metin çok uzun."
        return "Beklenmeyen bir veritabanı hatası oluştu."


# Bütün ekranların kullandığı ortak nesne
db = Veritabani()


if __name__ == "__main__":
    # Bağlantı testi: python db.py
    try:
        print(db.getir_tek("SELECT version()")[0])
        for tablo in ("bolum", "doktor", "hasta", "randevu", "muayene", "teshis",
                      "muayene_teshis", "ilac", "recete", "recete_ilac"):
            adet = db.getir_tek(f"SELECT COUNT(*) FROM {tablo}")[0]
            print(f"{tablo:15} {adet} kayıt")
        print("Bağlantı başarılı.")
    except (psycopg2.Error, RuntimeError) as hata:
        print("Hata:", Veritabani.hata_mesaji(hata))
    finally:
        db.kapat()
