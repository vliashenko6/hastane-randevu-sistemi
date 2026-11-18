"""Randevu ekranı (FG-05, FG-06, FG-07, FG-08, FG-09).

Hazırlayan: Eray

Önce hasta TC ile bulunur, sonra bölüm ve doktor seçilip tarih ve saat girilerek
randevu alınır. Hastanın bütün randevuları listelenir, aktif olanlar iptal edilebilir.
"""

import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

import psycopg2

from db import db


def tarih_yaz(tarih):
    return tarih.strftime("%d.%m.%Y") if tarih else ""


class RandevuEkrani(tk.Toplevel):
    def __init__(self, ana_pencere):
        super().__init__(ana_pencere)
        self.ana_pencere = ana_pencere
        self.hasta_id = None
        self.doktorlar = []
        self.title("Randevu İşlemleri")
        self.geometry("820x600")

        # --- hasta seçimi ---
        hasta = tk.LabelFrame(self, text="Hasta", padx=8, pady=6)
        hasta.pack(fill="x", padx=10, pady=(10, 5))
        tk.Label(hasta, text="TC Kimlik No:").pack(side="left")
        self.tc = tk.Entry(hasta, width=16)
        self.tc.pack(side="left", padx=5)
        self.tc.bind("<Return>", lambda olay: self._hasta_bul())
        tk.Button(hasta, text="Hastayı Bul", command=self._hasta_bul).pack(side="left")
        self.hasta_yazi = tk.Label(hasta, text="Hasta seçilmedi.")
        self.hasta_yazi.pack(side="left", padx=12)

        # --- yeni randevu ---
        yeni = tk.LabelFrame(self, text="Yeni Randevu", padx=8, pady=6)
        yeni.pack(fill="x", padx=10, pady=5)
        self.bolumler = db.getir("SELECT bolum_id, bolum_adi FROM bolum ORDER BY bolum_adi")
        tk.Label(yeni, text="Bölüm:").grid(row=0, column=0, sticky="e", pady=3)
        self.bolum_secim = ttk.Combobox(yeni, state="readonly", width=24,
                                        values=[b[1] for b in self.bolumler])
        self.bolum_secim.grid(row=0, column=1, padx=5)
        self.bolum_secim.bind("<<ComboboxSelected>>", self._doktorlari_yukle)
        tk.Label(yeni, text="Doktor:").grid(row=0, column=2, sticky="e")
        self.doktor_secim = ttk.Combobox(yeni, state="readonly", width=30)
        self.doktor_secim.grid(row=0, column=3, padx=5)
        tk.Label(yeni, text="Tarih (GG.AA.YYYY):").grid(row=1, column=0, sticky="e", pady=3)
        self.tarih = tk.Entry(yeni, width=14)
        self.tarih.grid(row=1, column=1, sticky="w", padx=5)
        tk.Label(yeni, text="Saat (SS:DD):").grid(row=1, column=2, sticky="e")
        self.saat = tk.Entry(yeni, width=8)
        self.saat.grid(row=1, column=3, sticky="w", padx=5)
        tk.Button(yeni, text="Randevu Al", width=14, command=self.randevu_al).grid(
            row=1, column=4, padx=10)

        # --- randevu listesi ---
        liste_alani = tk.LabelFrame(self, text="Hastanın Randevuları", padx=8, pady=6)
        liste_alani.pack(fill="both", expand=True, padx=10, pady=5)
        self.liste = ttk.Treeview(liste_alani, show="headings", height=10,
                                  columns=("tarih", "saat", "doktor", "bolum", "durum"))
        for sutun, baslik, genislik in (("tarih", "Tarih", 90), ("saat", "Saat", 60),
                                         ("doktor", "Doktor", 250), ("bolum", "Bölüm", 160),
                                         ("durum", "Durum", 90)):
            self.liste.heading(sutun, text=baslik)
            self.liste.column(sutun, width=genislik)
        self.liste.pack(fill="both", expand=True)

        alt = tk.Frame(self)
        alt.pack(fill="x", padx=10, pady=(0, 10))
        tk.Button(alt, text="Seçili Randevuyu İptal Et", command=self.randevu_iptal).pack(
            side="left")
        tk.Button(alt, text="Kapat", command=self.destroy).pack(side="right")

    # ---------- hasta ve doktor seçimi ----------
    def _hasta_bul(self):
        tc = self.tc.get().strip()
        try:
            hasta = db.getir_tek("SELECT hasta_id, ad, soyad FROM hasta WHERE tc_no = %s", (tc,))
        except psycopg2.Error as hata:
            messagebox.showerror("Randevu", db.hata_mesaji(hata), parent=self)
            return
        if hasta is None:
            self.hasta_id = None
            self.hasta_yazi.config(text="Hasta seçilmedi.")
            self.liste.delete(*self.liste.get_children())
            messagebox.showwarning("Randevu", "Bu TC ile kayıtlı hasta yok. "
                                   "Önce Hasta İşlemleri'nden kayıt yapın.", parent=self)
            return
        self.hasta_id = hasta[0]
        self.hasta_yazi.config(text=f"{hasta[1]} {hasta[2]}")
        self.randevulari_listele()

    def _doktorlari_yukle(self, olay=None):
        """Seçilen bölümün doktorlarını listeler (FG-05)."""
        bolum_id = self.bolumler[self.bolum_secim.current()][0]
        try:
            self.doktorlar = db.getir(
                "SELECT doktor_id, COALESCE(unvan || ' ', '') || ad || ' ' || soyad "
                "FROM doktor WHERE bolum_id = %s ORDER BY soyad, ad", (bolum_id,))
        except psycopg2.Error as hata:
            messagebox.showerror("Randevu", db.hata_mesaji(hata), parent=self)
            return
        self.doktor_secim.config(values=[d[1] for d in self.doktorlar])
        self.doktor_secim.set("")

    # ---------- kontroller ----------
    def gecmis_tarih_kontrol(self, tarih, saat):
        """Randevu zamanı geçmişteyse True döner (FG-07). Bu kural veritabanında yok."""
        return datetime.combine(tarih, saat) < datetime.now()

    def cakisma_kontrol(self, doktor_id, tarih, saat):
        """Doktorun aynı tarih ve saatte iptal edilmemiş randevusu varsa True döner (FG-06)."""
        satir = db.getir_tek(
            "SELECT 1 FROM randevu WHERE doktor_id = %s AND randevu_tarihi = %s "
            "AND randevu_saati = %s AND durum <> 'iptal'", (doktor_id, tarih, saat))
        return satir is not None

    # ---------- işlemler ----------
    def randevu_al(self):
        if self.hasta_id is None:
            messagebox.showwarning("Randevu", "Önce hastayı seçin (TC yazıp 'Hastayı Bul').",
                                   parent=self)
            return
        if self.doktor_secim.current() < 0:
            messagebox.showwarning("Randevu", "Bölüm ve doktor seçin.", parent=self)
            return
        try:
            tarih = datetime.strptime(self.tarih.get().strip(), "%d.%m.%Y").date()
            saat = datetime.strptime(self.saat.get().strip(), "%H:%M").time()
        except ValueError:
            messagebox.showwarning("Randevu", "Tarihi GG.AA.YYYY, saati SS:DD biçiminde yazın "
                                   "(örnek: 14.12.2026 ve 09:30).", parent=self)
            return
        doktor_id = self.doktorlar[self.doktor_secim.current()][0]

        if self.gecmis_tarih_kontrol(tarih, saat):
            messagebox.showwarning("Randevu", "Geçmiş bir tarihe randevu verilemez.", parent=self)
            return
        try:
            if self.cakisma_kontrol(doktor_id, tarih, saat):
                messagebox.showwarning("Randevu", "Bu doktorun bu tarih ve saatte başka bir "
                                       "randevusu var.", parent=self)
                return
            db.ekle("INSERT INTO randevu (hasta_id, doktor_id, randevu_tarihi, randevu_saati) "
                    "VALUES (%s, %s, %s, %s) RETURNING randevu_id",
                    (self.hasta_id, doktor_id, tarih, saat))
        except psycopg2.Error as hata:
            messagebox.showerror("Randevu", db.hata_mesaji(hata), parent=self)
            return
        messagebox.showinfo("Randevu", "Randevu oluşturuldu.", parent=self)
        self.tarih.delete(0, tk.END)
        self.saat.delete(0, tk.END)
        self.randevulari_listele()

    def randevu_iptal(self):
        """Randevuyu silmez, durumunu 'iptal' yapar (FG-08). Sadece aktif randevu iptal edilir."""
        secili = self.liste.selection()
        if not secili:
            messagebox.showwarning("Randevu", "Listeden bir randevu seçin.", parent=self)
            return
        if self.liste.item(secili[0])["values"][4] != "aktif":
            messagebox.showwarning("Randevu", "Sadece aktif randevular iptal edilebilir.",
                                   parent=self)
            return
        if not messagebox.askyesno("Randevu", "Seçili randevu iptal edilsin mi?", parent=self):
            return
        try:
            db.calistir("UPDATE randevu SET durum = 'iptal' "
                        "WHERE randevu_id = %s AND durum = 'aktif'", (int(secili[0]),))
        except psycopg2.Error as hata:
            messagebox.showerror("Randevu", db.hata_mesaji(hata), parent=self)
            return
        self.randevulari_listele()

    def randevulari_listele(self):
        """Seçili hastanın bütün randevularını listeler (FG-09)."""
        self.liste.delete(*self.liste.get_children())
        if self.hasta_id is None:
            return
        try:
            satirlar = db.getir(
                "SELECT r.randevu_id, r.randevu_tarihi, r.randevu_saati, "
                "COALESCE(d.unvan || ' ', '') || d.ad || ' ' || d.soyad, b.bolum_adi, r.durum "
                "FROM randevu r JOIN doktor d ON d.doktor_id = r.doktor_id "
                "JOIN bolum b ON b.bolum_id = d.bolum_id WHERE r.hasta_id = %s "
                "ORDER BY r.randevu_tarihi DESC, r.randevu_saati DESC", (self.hasta_id,))
        except psycopg2.Error as hata:
            messagebox.showerror("Randevu", db.hata_mesaji(hata), parent=self)
            return
        for rid, tarih, saat, doktor, bolum, durum in satirlar:
            self.liste.insert("", tk.END, iid=str(rid), values=(
                tarih_yaz(tarih), saat.strftime("%H:%M"), doktor, bolum, durum))
