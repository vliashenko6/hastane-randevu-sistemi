"""Reçete ekranı (FG-17, FG-18, FG-19, FG-20, FG-21).

Hazırlayan: Veronika

Bir muayene seçilir. Muayenenin reçetesi yoksa açıklama yazılıp reçete oluşturulur,
sonra reçeteye ilaç, doz, kullanım şekli ve kutu adedi girilerek ilaçlar eklenir.
Muayene ekranından açılırsa muayene_id ile gelir ve muayene seçimi kilitlenir.
"""

import tkinter as tk
from tkinter import messagebox, ttk

import psycopg2

from db import db


def tarih_yaz(tarih):
    return tarih.strftime("%d.%m.%Y") if tarih else ""


class ReceteEkrani(tk.Toplevel):
    def __init__(self, ana_pencere, muayene_id=None):
        super().__init__(ana_pencere)
        self.ana_pencere = ana_pencere
        self.muayene_id = muayene_id
        self.recete_id = None
        self.hasta_id = None
        self.title("Reçete")
        self.geometry("760x560")

        # --- muayene seçimi ---
        ust = tk.LabelFrame(self, text="Muayene", padx=8, pady=6)
        ust.pack(fill="x", padx=10, pady=(10, 5))
        self.muayeneler = db.getir(
            "SELECT m.muayene_id, m.muayene_tarihi, h.ad || ' ' || h.soyad, "
            "       COALESCE(d.unvan || ' ', '') || d.ad || ' ' || d.soyad "
            "FROM muayene m "
            "JOIN randevu r ON r.randevu_id = m.randevu_id "
            "JOIN hasta h ON h.hasta_id = r.hasta_id "
            "JOIN doktor d ON d.doktor_id = r.doktor_id "
            "ORDER BY m.muayene_tarihi DESC, m.muayene_id DESC")
        self.muayene_secim = ttk.Combobox(ust, state="readonly", width=80, values=[
            f"{m[0]} - {tarih_yaz(m[1])} - {m[2]} - {m[3]}" for m in self.muayeneler])
        self.muayene_secim.pack(fill="x")
        self.muayene_secim.bind("<<ComboboxSelected>>", self.muayene_secildi)
        self.durum = tk.Label(ust, text="Bir muayene seçin.", anchor="w", fg="#444444")
        self.durum.pack(fill="x", pady=(6, 0))

        # --- reçete oluşturma ---
        orta = tk.LabelFrame(self, text="Reçete", padx=8, pady=6)
        orta.pack(fill="x", padx=10, pady=5)
        tk.Label(orta, text="Açıklama:").grid(row=0, column=0, sticky="w")
        self.aciklama = tk.Entry(orta, width=60)
        self.aciklama.grid(row=0, column=1, padx=5)
        self.olustur_dugme = tk.Button(orta, text="Reçete Oluştur",
                                       command=self.recete_olustur, state="disabled")
        self.olustur_dugme.grid(row=0, column=2)

        # --- ilaç ekleme ---
        ilac_alani = tk.LabelFrame(self, text="İlaç Ekle", padx=8, pady=6)
        ilac_alani.pack(fill="x", padx=10, pady=5)
        self.ilaclar = db.getir("SELECT ilac_id, ilac_adi FROM ilac ORDER BY ilac_adi")
        tk.Label(ilac_alani, text="İlaç:").grid(row=0, column=0, sticky="w")
        self.ilac_secim = ttk.Combobox(ilac_alani, state="readonly", width=30,
                                       values=[i[1] for i in self.ilaclar])
        self.ilac_secim.grid(row=0, column=1, padx=5, pady=2)
        tk.Label(ilac_alani, text="Doz:").grid(row=0, column=2, sticky="w")
        self.doz = tk.Entry(ilac_alani, width=8)
        self.doz.grid(row=0, column=3, padx=5)
        tk.Label(ilac_alani, text="Kutu:").grid(row=0, column=4, sticky="w")
        self.kutu = tk.Spinbox(ilac_alani, from_=1, to=10, width=4)
        self.kutu.grid(row=0, column=5, padx=5)
        tk.Label(ilac_alani, text="Kullanım şekli:").grid(row=1, column=0, sticky="w")
        self.kullanim = tk.Entry(ilac_alani, width=55)
        self.kullanim.grid(row=1, column=1, columnspan=5, sticky="w", padx=5, pady=2)
        self.ekle_dugme = tk.Button(ilac_alani, text="İlaç Ekle", command=self.ilac_ekle,
                                    state="disabled")
        self.ekle_dugme.grid(row=0, column=6, rowspan=2, padx=8)

        # --- reçetedeki ilaçlar ---
        alt = tk.LabelFrame(self, text="Reçetedeki İlaçlar", padx=8, pady=6)
        alt.pack(fill="both", expand=True, padx=10, pady=5)
        self.liste = ttk.Treeview(alt, columns=("ilac", "doz", "kullanim", "kutu"),
                                  show="headings", height=6)
        for sutun, baslik, genislik in (("ilac", "İlaç", 220), ("doz", "Doz", 70),
                                         ("kullanim", "Kullanım şekli", 290),
                                         ("kutu", "Kutu", 60)):
            self.liste.heading(sutun, text=baslik)
            self.liste.column(sutun, width=genislik)
        self.liste.pack(fill="both", expand=True)

        dugmeler = tk.Frame(self)
        dugmeler.pack(fill="x", padx=10, pady=(0, 10))
        self.cikar_dugme = tk.Button(dugmeler, text="Seçili İlacı Çıkar",
                                     command=self.ilac_cikar, state="disabled")
        self.cikar_dugme.pack(side="left")
        self.gecmis_dugme = tk.Button(dugmeler, text="Hastanın Geçmiş Reçeteleri",
                                      command=self.gecmis_receteler, state="disabled")
        self.gecmis_dugme.pack(side="left", padx=8)
        tk.Button(dugmeler, text="Kapat", command=self.destroy).pack(side="right")

        # muayene ekranından açıldıysa o muayeneyi seç ve kilitle
        if muayene_id is not None:
            for i, m in enumerate(self.muayeneler):
                if m[0] == muayene_id:
                    self.muayene_secim.current(i)
                    self.muayene_secim.config(state="disabled")
                    self.muayene_secildi()
                    break

    def muayene_secildi(self, olay=None):
        """Seçilen muayenenin reçetesi var mı bakar ve ekranı ona göre hazırlar."""
        self.muayene_id = self.muayeneler[self.muayene_secim.current()][0]
        self.hasta_id = db.getir_tek(
            "SELECT r.hasta_id FROM muayene m JOIN randevu r ON r.randevu_id = m.randevu_id "
            "WHERE m.muayene_id = %s", (self.muayene_id,))[0]
        recete = db.getir_tek(
            "SELECT recete_id, recete_tarihi, aciklama FROM recete WHERE muayene_id = %s",
            (self.muayene_id,))
        self.gecmis_dugme.config(state="normal")
        if recete:
            self.recete_id = recete[0]
            self.durum.config(text=f"Reçete no: {recete[0]}  ({tarih_yaz(recete[1])})")
            self.aciklama.delete(0, tk.END)
            self.aciklama.insert(0, recete[2] or "")
            self.olustur_dugme.config(state="disabled")
            self.ekle_dugme.config(state="normal")
            self.cikar_dugme.config(state="normal")
        else:
            self.recete_id = None
            self.durum.config(text="Bu muayene için henüz reçete yazılmamış.")
            self.aciklama.delete(0, tk.END)
            self.olustur_dugme.config(state="normal")
            self.ekle_dugme.config(state="disabled")
            self.cikar_dugme.config(state="disabled")
        self.ilaclari_listele()

    def recete_olustur(self):
        """Seçili muayene için reçete oluşturur (FG-17)."""
        if self.muayene_id is None:
            messagebox.showwarning("Reçete", "Önce bir muayene seçin.", parent=self)
            return
        aciklama = self.aciklama.get().strip() or None
        try:
            self.recete_id = db.ekle(
                "INSERT INTO recete (muayene_id, aciklama) VALUES (%s, %s) RETURNING recete_id",
                (self.muayene_id, aciklama))
        except psycopg2.Error as hata:
            messagebox.showerror("Reçete", db.hata_mesaji(hata), parent=self)
            return
        self.muayene_secildi()

    def ilac_ekle(self):
        """Reçeteye ilaç ekler (FG-18). Aynı ilaç ikinci kez eklenemez (FG-19)."""
        if self.recete_id is None:
            messagebox.showwarning("İlaç", "Önce reçete oluşturun.", parent=self)
            return
        if self.ilac_secim.current() < 0 or not self.doz.get().strip():
            messagebox.showwarning("İlaç", "İlaç ve doz boş bırakılamaz.", parent=self)
            return
        try:
            kutu = int(self.kutu.get())
        except ValueError:
            messagebox.showwarning("İlaç", "Kutu adedi bir sayı olmalı.", parent=self)
            return
        ilac_id = self.ilaclar[self.ilac_secim.current()][0]
        try:
            db.calistir(
                "INSERT INTO recete_ilac (recete_id, ilac_id, doz, kullanim_sekli, kutu_adedi) "
                "VALUES (%s, %s, %s, %s, %s)",
                (self.recete_id, ilac_id, self.doz.get().strip(),
                 self.kullanim.get().strip() or None, kutu))
        except psycopg2.Error as hata:
            messagebox.showerror("İlaç", db.hata_mesaji(hata), parent=self)
            return
        self.doz.delete(0, tk.END)
        self.kullanim.delete(0, tk.END)
        self.ilaclari_listele()

    def ilac_cikar(self):
        secili = self.liste.selection()
        if not secili:
            messagebox.showwarning("İlaç", "Listeden bir ilaç seçin.", parent=self)
            return
        try:
            db.calistir("DELETE FROM recete_ilac WHERE recete_id = %s AND ilac_id = %s",
                        (self.recete_id, int(secili[0])))
        except psycopg2.Error as hata:
            messagebox.showerror("İlaç", db.hata_mesaji(hata), parent=self)
        self.ilaclari_listele()

    def ilaclari_listele(self):
        """Reçetedeki ilaçları tabloya yazar (FG-20)."""
        self.liste.delete(*self.liste.get_children())
        if self.recete_id is None:
            return
        satirlar = db.getir(
            "SELECT i.ilac_id, i.ilac_adi, ri.doz, ri.kullanim_sekli, ri.kutu_adedi "
            "FROM recete_ilac ri JOIN ilac i ON i.ilac_id = ri.ilac_id "
            "WHERE ri.recete_id = %s ORDER BY i.ilac_adi", (self.recete_id,))
        for ilac_id, ad, doz, kullanim, kutu in satirlar:
            self.liste.insert("", tk.END, iid=str(ilac_id), values=(ad, doz, kullanim or "", kutu))

    def gecmis_receteler(self):
        """Hastaya daha önce yazılmış bütün reçeteleri gösterir (FG-21, recete_detay görünümü)."""
        satirlar = db.getir(
            "SELECT recete_id, recete_tarihi, doktor, ilac_adi, doz FROM recete_detay "
            "WHERE hasta_id = %s ORDER BY recete_tarihi DESC, recete_id, ilac_adi",
            (self.hasta_id,))
        pencere = tk.Toplevel(self)
        pencere.title("Hastanın Geçmiş Reçeteleri")
        pencere.geometry("640x300")
        tablo = ttk.Treeview(pencere, columns=("no", "tarih", "doktor", "ilac", "doz"),
                             show="headings")
        for sutun, baslik, genislik in (("no", "Reçete", 60), ("tarih", "Tarih", 90),
                                         ("doktor", "Doktor", 190), ("ilac", "İlaç", 200),
                                         ("doz", "Doz", 60)):
            tablo.heading(sutun, text=baslik)
            tablo.column(sutun, width=genislik)
        for no, tarih, doktor, ilac, doz in satirlar:
            tablo.insert("", tk.END, values=(no, tarih_yaz(tarih), doktor, ilac, doz))
        tablo.pack(fill="both", expand=True, padx=10, pady=10)
        if not satirlar:
            tk.Label(pencere, text="Bu hastaya daha önce reçete yazılmamış.").pack(pady=(0, 10))
