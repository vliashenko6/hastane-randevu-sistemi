"""İstatistik ekranı (FG-23, FG-24, FG-25).

Hazırlayan: Veronika

Hastane yöneticisi için üç sekme:
en çok yazılan ilaçlar, bölümlere göre hasta sayısı ve doktor başına muayene sayısı.
"""

import tkinter as tk
from tkinter import messagebox, ttk

import psycopg2

from db import db

# (sekme adı, sütun başlıkları, sorgu)
ISTATISTIKLER = [
    ("En Çok Yazılan İlaçlar", ("İlaç", "Reçete sayısı", "Toplam kutu"),
     "SELECT i.ilac_adi, COUNT(ri.recete_id), COALESCE(SUM(ri.kutu_adedi), 0) "
     "FROM ilac i LEFT JOIN recete_ilac ri ON ri.ilac_id = i.ilac_id "
     "GROUP BY i.ilac_id, i.ilac_adi "
     "ORDER BY COUNT(ri.recete_id) DESC, i.ilac_adi"),
    ("Bölümlere Göre Hasta Sayısı", ("Bölüm", "Hasta sayısı"),
     "SELECT b.bolum_adi, COUNT(DISTINCT r.hasta_id) "
     "FROM bolum b "
     "LEFT JOIN doktor d ON d.bolum_id = b.bolum_id "
     "LEFT JOIN randevu r ON r.doktor_id = d.doktor_id AND r.durum <> 'iptal' "
     "GROUP BY b.bolum_id, b.bolum_adi "
     "ORDER BY COUNT(DISTINCT r.hasta_id) DESC, b.bolum_adi"),
    ("Doktor Başına Muayene", ("Doktor", "Bölüm", "Muayene sayısı"),
     "SELECT d.unvan || ' ' || d.ad || ' ' || d.soyad, b.bolum_adi, COUNT(m.muayene_id) "
     "FROM doktor d "
     "JOIN bolum b ON b.bolum_id = d.bolum_id "
     "LEFT JOIN randevu r ON r.doktor_id = d.doktor_id "
     "LEFT JOIN muayene m ON m.randevu_id = r.randevu_id "
     "GROUP BY d.doktor_id, d.unvan, d.ad, d.soyad, b.bolum_adi "
     "ORDER BY COUNT(m.muayene_id) DESC, d.ad"),
]


class IstatistikEkrani(tk.Toplevel):
    def __init__(self, ana_pencere):
        super().__init__(ana_pencere)
        self.ana_pencere = ana_pencere
        self.title("İstatistikler")
        self.geometry("620x420")

        sekmeler = ttk.Notebook(self)
        sekmeler.pack(fill="both", expand=True, padx=10, pady=10)
        self.tablolar = []
        for ad, basliklar, _ in ISTATISTIKLER:
            sayfa = tk.Frame(sekmeler)
            sekmeler.add(sayfa, text=ad)
            tablo = ttk.Treeview(sayfa, columns=basliklar, show="headings")
            for baslik in basliklar:
                tablo.heading(baslik, text=baslik)
                tablo.column(baslik, width=150 if baslik != basliklar[0] else 240)
            tablo.pack(fill="both", expand=True)
            self.tablolar.append(tablo)

        dugmeler = tk.Frame(self)
        dugmeler.pack(fill="x", padx=10, pady=(0, 10))
        tk.Button(dugmeler, text="Yenile", command=self.istatistikleri_getir).pack(side="left")
        tk.Button(dugmeler, text="Kapat", command=self.destroy).pack(side="right")

        self.istatistikleri_getir()

    def istatistikleri_getir(self):
        """Üç istatistiği veritabanından okuyup sekmelere yazar."""
        for tablo, (ad, _, sorgu) in zip(self.tablolar, ISTATISTIKLER):
            tablo.delete(*tablo.get_children())
            try:
                for satir in db.getir(sorgu):
                    tablo.insert("", tk.END, values=satir)
            except psycopg2.Error as hata:
                messagebox.showerror(ad, db.hata_mesaji(hata), parent=self)
                return
