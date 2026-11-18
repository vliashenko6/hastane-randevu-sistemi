"""Bölüm ve doktor listeleme ekranı (FG-10, FG-11).

Hazırlayan: Sude

Solda hastanedeki bölümler, sağda seçilen bölümde çalışan doktorlar listelenir.
"""

import tkinter as tk
from tkinter import ttk, messagebox

import psycopg2

from db import db


class BolumDoktorEkrani(tk.Toplevel):

    def __init__(self, ana_pencere):
        super().__init__(ana_pencere)
        self.ana_pencere = ana_pencere
        self.title("Bölümler ve Doktorlar")
        self.geometry("760x400")

        # Sol taraf: bölümler
        sol = ttk.LabelFrame(self, text="Bölümler")
        sol.pack(side="left", fill="y", padx=10, pady=10)

        self.bolum_tablosu = ttk.Treeview(sol, columns=("ad", "doktor"), show="headings", height=14)
        self.bolum_tablosu.heading("ad", text="Bölüm")
        self.bolum_tablosu.heading("doktor", text="Doktor sayısı")
        self.bolum_tablosu.column("ad", width=170)
        self.bolum_tablosu.column("doktor", width=90, anchor="center")
        self.bolum_tablosu.pack(fill="y", expand=True, padx=5, pady=5)
        # Bir bölüm seçilince o bölümün doktorları gelsin
        self.bolum_tablosu.bind("<<TreeviewSelect>>", lambda olay: self.doktorlari_listele())

        # Sağ taraf: doktorlar
        sag = ttk.LabelFrame(self, text="Doktorlar")
        sag.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)

        self.doktor_tablosu = ttk.Treeview(sag, columns=("unvan", "ad", "telefon"),
                                           show="headings", height=14)
        self.doktor_tablosu.heading("unvan", text="Unvan")
        self.doktor_tablosu.heading("ad", text="Ad Soyad")
        self.doktor_tablosu.heading("telefon", text="Telefon")
        self.doktor_tablosu.column("unvan", width=90)
        self.doktor_tablosu.column("ad", width=170)
        self.doktor_tablosu.column("telefon", width=120)
        self.doktor_tablosu.pack(fill="both", expand=True, padx=5, pady=5)

        self.bolumleri_listele()

    def bolumleri_listele(self):
        """Bütün bölümleri, her bölümdeki doktor sayısıyla birlikte listeler."""
        try:
            bolumler = db.getir("""
                SELECT b.bolum_id, b.bolum_adi, COUNT(d.doktor_id)
                FROM bolum b
                LEFT JOIN doktor d ON d.bolum_id = b.bolum_id
                GROUP BY b.bolum_id, b.bolum_adi
                ORDER BY b.bolum_adi
            """)
        except (psycopg2.Error, RuntimeError) as hata:
            messagebox.showerror("Hata", db.hata_mesaji(hata), parent=self)
            return

        self.bolum_tablosu.delete(*self.bolum_tablosu.get_children())
        for bolum_id, bolum_adi, doktor_sayisi in bolumler:
            # iid olarak bolum_id veriyoruz, seçilince hangi bölüm olduğunu buradan anlıyoruz
            self.bolum_tablosu.insert("", "end", iid=str(bolum_id), values=(bolum_adi, doktor_sayisi))

        # İlk bölüm seçili gelsin
        if bolumler:
            ilk = str(bolumler[0][0])
            self.bolum_tablosu.selection_set(ilk)
            self.bolum_tablosu.focus(ilk)

    def doktorlari_listele(self):
        """Seçilen bölümde çalışan doktorları listeler."""
        secili = self.bolum_tablosu.selection()
        if not secili:
            return
        bolum_id = int(secili[0])

        try:
            doktorlar = db.getir("""
                SELECT unvan, ad || ' ' || soyad, telefon
                FROM doktor
                WHERE bolum_id = %s
                ORDER BY ad, soyad
            """, (bolum_id,))
        except (psycopg2.Error, RuntimeError) as hata:
            messagebox.showerror("Hata", db.hata_mesaji(hata), parent=self)
            return

        self.doktor_tablosu.delete(*self.doktor_tablosu.get_children())
        for unvan, ad_soyad, telefon in doktorlar:
            # Boş olabilen sütunlar ekranda "-" görünsün
            self.doktor_tablosu.insert("", "end", values=(unvan or "-", ad_soyad, telefon or "-"))


if __name__ == "__main__":
    # Ekranı tek başına denemek için: python bolum_doktor_ekrani.py
    kok = tk.Tk()
    kok.withdraw()
    ekran = BolumDoktorEkrani(kok)
    ekran.protocol("WM_DELETE_WINDOW", kok.destroy)
    kok.mainloop()
