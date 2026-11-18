"""Doktor paneli: doktorun seçilen gündeki randevuları (FG-12).

Hazırlayan: Sude

Doktor ve tarih seçilir, o günkü randevular saat sırasıyla listelenir.
İptal edilen randevular listede çıkmaz. Bir randevu seçilip "Muayene" düğmesine
basılınca (ya da satıra çift tıklanınca) muayene ekranı açılır.
"""

import datetime
import tkinter as tk
from tkinter import ttk, messagebox

import psycopg2

from db import db
from muayene_ekrani import MuayeneEkrani


def tarih_oku(yazi):
    """Tarihi GG.AA.YYYY (diğer ekranlardaki gibi) ya da YYYY-AA-GG biçiminde okur.
    Geçersizse None döner."""
    yazi = yazi.strip()
    for bicim in ("%d.%m.%Y", "%Y-%m-%d"):
        try:
            return datetime.datetime.strptime(yazi, bicim).date()
        except ValueError:
            pass
    return None


class DoktorPaneli(tk.Toplevel):

    def __init__(self, ana_pencere):
        super().__init__(ana_pencere)
        self.ana_pencere = ana_pencere
        self.title("Doktor Paneli")
        self.geometry("820x430")

        # Üst kısım: doktor ve tarih seçimi
        ust = ttk.Frame(self)
        ust.pack(fill="x", padx=10, pady=10)

        ttk.Label(ust, text="Doktor:").pack(side="left")
        self.doktor_kutusu = ttk.Combobox(ust, state="readonly", width=40)
        self.doktor_kutusu.pack(side="left", padx=(5, 15))

        ttk.Label(ust, text="Tarih (GG.AA.YYYY):").pack(side="left")
        self.tarih_kutusu = ttk.Entry(ust, width=12)
        self.tarih_kutusu.insert(0, datetime.date.today().strftime("%d.%m.%Y"))
        self.tarih_kutusu.pack(side="left", padx=5)

        ttk.Button(ust, text="Listele", command=self.gunluk_randevulari_getir).pack(side="left", padx=5)

        # Randevu listesi
        sutunlar = ("saat", "hasta", "tc", "durum", "muayene")
        self.tablo = ttk.Treeview(self, columns=sutunlar, show="headings", height=13)
        basliklar = {"saat": "Saat", "hasta": "Hasta", "tc": "TC Kimlik No",
                     "durum": "Durum", "muayene": "Muayene"}
        genislikler = {"saat": 70, "hasta": 200, "tc": 130, "durum": 110, "muayene": 110}
        for sutun in sutunlar:
            self.tablo.heading(sutun, text=basliklar[sutun])
            self.tablo.column(sutun, width=genislikler[sutun])
        self.tablo.pack(fill="both", expand=True, padx=10)
        self.tablo.bind("<Double-1>", lambda olay: self.muayene_ac())

        # Alt kısım
        alt = ttk.Frame(self)
        alt.pack(fill="x", padx=10, pady=10)
        self.bilgi = ttk.Label(alt, text="")
        self.bilgi.pack(side="left")
        ttk.Button(alt, text="Muayene", command=self.muayene_ac).pack(side="right")

        self.doktorlari_yukle()

    def doktorlari_yukle(self):
        """Doktor seçme kutusunu doldurur."""
        try:
            doktorlar = db.getir("""
                SELECT d.doktor_id, COALESCE(d.unvan || ' ', '') || d.ad || ' ' || d.soyad,
                       b.bolum_adi
                FROM doktor d
                JOIN bolum b ON b.bolum_id = d.bolum_id
                ORDER BY b.bolum_adi, d.ad
            """)
        except (psycopg2.Error, RuntimeError) as hata:
            messagebox.showerror("Hata", db.hata_mesaji(hata), parent=self)
            return

        # Kutuda yazı görünüyor, arkada hangi yazının hangi doktor_id olduğunu tutuyoruz
        self.doktor_idleri = {}
        for doktor_id, ad, bolum in doktorlar:
            self.doktor_idleri[f"{ad} ({bolum})"] = doktor_id
        self.doktor_kutusu["values"] = list(self.doktor_idleri)
        if doktorlar:
            self.doktor_kutusu.current(0)

    def gunluk_randevulari_getir(self):
        """Seçilen doktorun seçilen gündeki randevularını saat sırasıyla listeler."""
        doktor_id = self.doktor_idleri.get(self.doktor_kutusu.get())
        if doktor_id is None:
            messagebox.showwarning("Uyarı", "Lütfen bir doktor seçin.", parent=self)
            return

        # Tarihi kontrol et (FG-27: hatalı giriş kaydedilmesin, kullanıcı uyarılsın)
        tarih = tarih_oku(self.tarih_kutusu.get())
        if tarih is None:
            messagebox.showwarning("Uyarı", "Tarihi GG.AA.YYYY biçiminde yazın (örn. 01.12.2026).",
                                   parent=self)
            return

        try:
            randevular = db.getir("""
                SELECT r.randevu_id, to_char(r.randevu_saati, 'HH24:MI'),
                       h.ad || ' ' || h.soyad, h.tc_no, r.durum, m.muayene_id
                FROM randevu r
                JOIN hasta h ON h.hasta_id = r.hasta_id
                LEFT JOIN muayene m ON m.randevu_id = r.randevu_id
                WHERE r.doktor_id = %s
                  AND r.randevu_tarihi = %s
                  AND r.durum <> 'iptal'
                ORDER BY r.randevu_saati
            """, (doktor_id, tarih))
        except (psycopg2.Error, RuntimeError) as hata:
            messagebox.showerror("Hata", db.hata_mesaji(hata), parent=self)
            return

        self.tablo.delete(*self.tablo.get_children())
        for randevu_id, saat, hasta, tc, durum, muayene_id in randevular:
            muayene = "Yapıldı" if muayene_id else "-"
            self.tablo.insert("", "end", iid=str(randevu_id),
                              values=(saat, hasta, tc, durum, muayene))
        self.bilgi.config(text=f"{tarih.strftime('%d.%m.%Y')} için {len(randevular)} randevu")

    def muayene_ac(self):
        """Seçilen randevu için muayene ekranını açar."""
        secili = self.tablo.selection()
        if not secili:
            messagebox.showwarning("Uyarı", "Lütfen listeden bir randevu seçin.", parent=self)
            return
        ekran = MuayeneEkrani(self, int(secili[0]))
        # Muayene ekranı kapanınca liste yenilensin (durum 'tamamlandi' olmuş olabilir)
        self.wait_window(ekran)
        self.gunluk_randevulari_getir()


if __name__ == "__main__":
    # Ekranı tek başına denemek için: python doktor_paneli.py
    kok = tk.Tk()
    kok.withdraw()
    panel = DoktorPaneli(kok)
    panel.protocol("WM_DELETE_WINDOW", kok.destroy)
    kok.mainloop()
