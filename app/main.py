"""Hastane Randevu Sistemi - ana menü.

Hazırlayan: Veronika

Uygulama bu dosyadan başlatılır:  python main.py
Ana menüdeki her düğme ayrı bir ekranı (tk.Toplevel penceresi) açar.
"""

import importlib
import tkinter as tk
from tkinter import messagebox

import psycopg2

from db import db

# Düğme yazısı, ekranın dosyası ve sınıfı
EKRANLAR = [
    ("Hasta İşlemleri", "hasta_ekrani", "HastaEkrani"),
    ("Randevu İşlemleri", "randevu_ekrani", "RandevuEkrani"),
    ("Bölümler ve Doktorlar", "bolum_doktor_ekrani", "BolumDoktorEkrani"),
    ("Doktor Paneli", "doktor_paneli", "DoktorPaneli"),
    ("Reçete", "recete_ekrani", "ReceteEkrani"),
    ("İstatistikler", "istatistik_ekrani", "IstatistikEkrani"),
]


class AnaMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Doğuş Özel Hastanesi - Randevu Sistemi")
        self.geometry("380x470")
        self.resizable(False, False)

        tk.Label(self, text="Doğuş Özel Hastanesi", font=("Arial", 18, "bold")).pack(pady=(25, 0))
        tk.Label(self, text="Hastane Randevu Sistemi", font=("Arial", 11)).pack(pady=(0, 20))

        komutlar = [self.hasta_ac, self.randevu_ac, self.bolum_doktor_ac,
                    self.doktor_paneli_ac, self.recete_ac, self.istatistik_ac]
        for (yazi, _, _), komut in zip(EKRANLAR, komutlar):
            tk.Button(self, text=yazi, width=26, height=1, font=("Arial", 11),
                      command=komut).pack(pady=4)
        tk.Button(self, text="Çıkış", width=26, font=("Arial", 11),
                  command=self.cikis).pack(pady=(16, 0))

        self.protocol("WM_DELETE_WINDOW", self.cikis)
        self.baglanti_kontrol()

    def baglanti_kontrol(self):
        """Açılışta veritabanına bağlanılabiliyor mu bakar (FG-26)."""
        try:
            db.getir_tek("SELECT 1")
        except (psycopg2.Error, RuntimeError) as hata:
            messagebox.showerror("Bağlantı hatası", db.hata_mesaji(hata))

    def _ekran_ac(self, sira, *argumanlar):
        """Ekranın dosyasını bulup penceresini açar. Dosya henüz yoksa uyarı verir."""
        yazi, dosya, sinif = EKRANLAR[sira]
        try:
            modul = importlib.import_module(dosya)
        except ImportError:
            messagebox.showinfo(yazi, "Bu ekran henüz hazır değil.")
            return None
        return getattr(modul, sinif)(self, *argumanlar)

    def hasta_ac(self):
        return self._ekran_ac(0)

    def randevu_ac(self):
        return self._ekran_ac(1)

    def bolum_doktor_ac(self):
        return self._ekran_ac(2)

    def doktor_paneli_ac(self):
        return self._ekran_ac(3)

    def recete_ac(self):
        return self._ekran_ac(4)

    def istatistik_ac(self):
        return self._ekran_ac(5)

    def cikis(self):
        db.kapat()
        self.destroy()


if __name__ == "__main__":
    AnaMenu().mainloop()
