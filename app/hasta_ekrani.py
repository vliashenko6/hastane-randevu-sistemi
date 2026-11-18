"""Hasta ekranı (FG-01, FG-02, FG-03, FG-04, FG-27).

Hazırlayan: Eray

Yeni hasta kaydedilir, TC ya da ad-soyad ile aranır. Listeden seçilen hastanın
sadece telefon ve adresi güncellenebilir.
"""

import tkinter as tk
from datetime import date, datetime
from tkinter import messagebox, ttk

import psycopg2

from db import db

SUTUNLAR = "hasta_id, tc_no, ad, soyad, dogum_tarihi, cinsiyet, telefon, adres"


def tarih_yaz(tarih):
    return tarih.strftime("%d.%m.%Y") if tarih else ""


class HastaEkrani(tk.Toplevel):
    def __init__(self, ana_pencere):
        super().__init__(ana_pencere)
        self.ana_pencere = ana_pencere
        self.secili_id = None
        self.title("Hasta İşlemleri")
        self.geometry("860x560")

        # --- hasta formu ---
        form = tk.LabelFrame(self, text="Hasta Bilgileri", padx=8, pady=6)
        form.pack(fill="x", padx=10, pady=(10, 5))
        self.tc = self._giris(form, "TC Kimlik No:", 0, 0)
        self.ad = self._giris(form, "Ad:", 0, 2)
        self.soyad = self._giris(form, "Soyad:", 1, 0)
        self.dogum = self._giris(form, "Doğum Tarihi (GG.AA.YYYY):", 1, 2)
        tk.Label(form, text="Cinsiyet:").grid(row=2, column=0, sticky="e", pady=3)
        self.cinsiyet = ttk.Combobox(form, values=["E", "K"], state="readonly", width=5)
        self.cinsiyet.grid(row=2, column=1, sticky="w", padx=5)
        self.telefon = self._giris(form, "Telefon:", 2, 2)
        self.adres = self._giris(form, "Adres:", 3, 0)
        self.adres.config(width=60)
        self.adres.grid(columnspan=3, sticky="w")
        self.sabit_alanlar = [self.tc, self.ad, self.soyad, self.dogum, self.cinsiyet]

        dugmeler = tk.Frame(self)
        dugmeler.pack(fill="x", padx=10, pady=5)
        tk.Button(dugmeler, text="Kaydet", width=12, command=self.hasta_kaydet).pack(side="left")
        tk.Button(dugmeler, text="Telefon/Adres Güncelle", command=self.hasta_guncelle).pack(
            side="left", padx=8)
        tk.Button(dugmeler, text="Formu Temizle", command=self._formu_temizle).pack(side="left")

        # --- arama ---
        arama = tk.LabelFrame(self, text="Ara (TC ya da ad soyad)", padx=8, pady=6)
        arama.pack(fill="x", padx=10, pady=5)
        self.arama = tk.Entry(arama, width=30)
        self.arama.pack(side="left")
        self.arama.bind("<Return>", lambda olay: self.hasta_ara())
        tk.Button(arama, text="Ara", width=8, command=self.hasta_ara).pack(side="left", padx=8)
        tk.Button(arama, text="Tümünü Göster", command=self.listeyi_yenile).pack(side="left")

        # --- hasta listesi ---
        self.liste = ttk.Treeview(
            self, show="headings", height=10,
            columns=("tc", "ad", "soyad", "dogum", "cinsiyet", "telefon", "adres"))
        for sutun, baslik, genislik in (("tc", "TC No", 100), ("ad", "Ad", 90),
                                         ("soyad", "Soyad", 100), ("dogum", "Doğum T.", 85),
                                         ("cinsiyet", "Cins.", 45), ("telefon", "Telefon", 110),
                                         ("adres", "Adres", 260)):
            self.liste.heading(sutun, text=baslik)
            self.liste.column(sutun, width=genislik)
        self.liste.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        self.liste.bind("<<TreeviewSelect>>", self._hasta_secildi)

        self.listeyi_yenile()

    def _giris(self, ust, yazi, satir, sutun):
        tk.Label(ust, text=yazi).grid(row=satir, column=sutun, sticky="e", pady=3)
        giris = tk.Entry(ust, width=22)
        giris.grid(row=satir, column=sutun + 1, sticky="w", padx=5)
        return giris

    # ---------- kontrol ----------
    def _formu_kontrol(self):
        """Kayıttan önce alanları kontrol eder (FG-27). Sorun varsa None döner."""
        tc = self.tc.get().strip()
        ad = self.ad.get().strip()
        soyad = self.soyad.get().strip()
        telefon = self.telefon.get().strip()
        cinsiyet = self.cinsiyet.get()
        if not (tc.isdigit() and len(tc) == 11):
            messagebox.showwarning("Hasta", "TC kimlik no 11 rakamdan oluşmalı.", parent=self)
            return None
        if not ad or not soyad or not telefon or not cinsiyet:
            messagebox.showwarning(
                "Hasta", "TC, ad, soyad, doğum tarihi, cinsiyet ve telefon boş bırakılamaz.",
                parent=self)
            return None
        try:
            dogum = datetime.strptime(self.dogum.get().strip(), "%d.%m.%Y").date()
        except ValueError:
            messagebox.showwarning("Hasta", "Doğum tarihini GG.AA.YYYY biçiminde yazın "
                                   "(örnek: 25.03.1990).", parent=self)
            return None
        if dogum > date.today():
            messagebox.showwarning("Hasta", "Doğum tarihi bugünden sonra olamaz.", parent=self)
            return None
        return tc, ad, soyad, dogum, cinsiyet, telefon, self.adres.get().strip() or None

    # ---------- işlemler ----------
    def hasta_kaydet(self):
        """Yeni hasta ekler (FG-01, FG-02)."""
        if self.secili_id is not None:
            messagebox.showinfo("Hasta", "Yeni hasta için önce 'Formu Temizle' düğmesine basın.",
                                parent=self)
            return
        bilgi = self._formu_kontrol()
        if bilgi is None:
            return
        try:
            yeni_id = db.ekle(
                "INSERT INTO hasta (tc_no, ad, soyad, dogum_tarihi, cinsiyet, telefon, adres) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING hasta_id", bilgi)
        except psycopg2.Error as hata:
            messagebox.showerror("Hasta", db.hata_mesaji(hata), parent=self)
            return
        messagebox.showinfo("Hasta", f"Hasta kaydedildi (no: {yeni_id}).", parent=self)
        self._formu_temizle()
        self.listeyi_yenile()

    def hasta_ara(self):
        """TC ya da ad-soyad ile arar (FG-03)."""
        aranan = self.arama.get().strip()
        if not aranan:
            self.listeyi_yenile()
            return
        try:
            satirlar = db.getir(
                f"SELECT {SUTUNLAR} FROM hasta WHERE tc_no = %s "
                "OR ad || ' ' || soyad ILIKE %s ORDER BY soyad, ad",
                (aranan, "%" + aranan + "%"))
        except psycopg2.Error as hata:
            messagebox.showerror("Hasta", db.hata_mesaji(hata), parent=self)
            return
        self._listeyi_doldur(satirlar)
        if not satirlar:
            messagebox.showinfo("Hasta", "Aranan hasta bulunamadı.", parent=self)

    def hasta_guncelle(self):
        """Seçili hastanın sadece telefon ve adresini günceller (FG-04)."""
        if self.secili_id is None:
            messagebox.showwarning("Hasta", "Önce listeden bir hasta seçin.", parent=self)
            return
        telefon = self.telefon.get().strip()
        if not telefon:
            messagebox.showwarning("Hasta", "Telefon boş bırakılamaz.", parent=self)
            return
        try:
            db.calistir("UPDATE hasta SET telefon = %s, adres = %s WHERE hasta_id = %s",
                        (telefon, self.adres.get().strip() or None, self.secili_id))
        except psycopg2.Error as hata:
            messagebox.showerror("Hasta", db.hata_mesaji(hata), parent=self)
            return
        messagebox.showinfo("Hasta", "Telefon ve adres güncellendi.", parent=self)
        self._formu_temizle()
        self.listeyi_yenile()

    def listeyi_yenile(self):
        """Bütün hastaları listeler."""
        try:
            satirlar = db.getir(f"SELECT {SUTUNLAR} FROM hasta ORDER BY soyad, ad")
        except psycopg2.Error as hata:
            messagebox.showerror("Hasta", db.hata_mesaji(hata), parent=self)
            return
        self._listeyi_doldur(satirlar)

    # ---------- yardımcılar ----------
    def _listeyi_doldur(self, satirlar):
        self.liste.delete(*self.liste.get_children())
        for h in satirlar:
            self.liste.insert("", tk.END, iid=str(h[0]), values=(
                h[1], h[2], h[3], tarih_yaz(h[4]), h[5], h[6], h[7] or ""))

    def _hasta_secildi(self, olay=None):
        secili = self.liste.selection()
        if not secili:
            return
        self._formu_temizle()
        deger = self.liste.item(secili[0])["values"]
        self.secili_id = int(secili[0])
        # TC başında sıfır olabilir, Treeview sayıya çevirdiği için veritabanından okunur
        hasta = db.getir_tek("SELECT tc_no, ad, soyad, dogum_tarihi, cinsiyet, telefon, adres "
                             "FROM hasta WHERE hasta_id = %s", (self.secili_id,))
        for alan, yazi in zip((self.tc, self.ad, self.soyad, self.dogum),
                              (hasta[0], hasta[1], hasta[2], tarih_yaz(hasta[3]))):
            alan.insert(0, yazi)
        self.cinsiyet.set(hasta[4])
        self.telefon.insert(0, hasta[5])
        self.adres.insert(0, hasta[6] or "")
        # güncellemede sadece telefon ve adres değişebilir
        for alan in self.sabit_alanlar[:4]:
            alan.config(state="disabled")
        self.cinsiyet.config(state="disabled")

    def _formu_temizle(self):
        self.secili_id = None
        for alan in (self.tc, self.ad, self.soyad, self.dogum):
            alan.config(state="normal")
            alan.delete(0, tk.END)
        self.cinsiyet.config(state="readonly")
        self.cinsiyet.set("")
        self.telefon.delete(0, tk.END)
        self.adres.delete(0, tk.END)
