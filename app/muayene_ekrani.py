"""Muayene ve teşhis giriş ekranı (FG-13, FG-14, FG-15).

Hazırlayan: Sude

Doktor panelinde seçilen randevu için açılır.
- Randevunun muayenesi yoksa: şikâyet, notlar ve en az bir teşhis girilip muayene kaydedilir.
  Muayene kaydedilince randevunun durumu veritabanındaki trigger ile 'tamamlandi' olur.
- Muayene zaten varsa: bilgileri gösterilir, yeni teşhis eklenebilir, reçete yazılabilir.
"""

import tkinter as tk
from tkinter import ttk, messagebox

import psycopg2

from db import db


class MuayeneEkrani(tk.Toplevel):

    def __init__(self, ana_pencere, randevu_id):
        super().__init__(ana_pencere)
        self.ana_pencere = ana_pencere
        self.randevu_id = randevu_id
        self.muayene_id = None           # muayene kaydedilince dolar
        self.bekleyen_teshisler = []     # kaydetmeden önce eklenen teşhisler: (kod, ad, aciklama)
        self.title("Muayene")
        self.geometry("770x560")
        self.transient(ana_pencere)

        # Randevu bilgisi (hasta, doktor, tarih)
        self.randevu_bilgisi = ttk.Label(self, text="", font=("Segoe UI", 10, "bold"))
        self.randevu_bilgisi.pack(anchor="w", padx=10, pady=(10, 5))

        # Şikâyet ve notlar
        form = ttk.LabelFrame(self, text="Muayene bilgileri")
        form.pack(fill="x", padx=10, pady=5)
        ttk.Label(form, text="Şikâyet *").grid(row=0, column=0, sticky="nw", padx=5, pady=5)
        self.sikayet_kutusu = tk.Text(form, height=3, width=60, font=("Segoe UI", 10))
        self.sikayet_kutusu.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(form, text="Notlar").grid(row=1, column=0, sticky="nw", padx=5, pady=5)
        self.notlar_kutusu = tk.Text(form, height=3, width=60, font=("Segoe UI", 10))
        self.notlar_kutusu.grid(row=1, column=1, padx=5, pady=5)

        # Teşhis ekleme
        teshis = ttk.LabelFrame(self, text="Teşhisler")
        teshis.pack(fill="both", expand=True, padx=10, pady=5)

        satir = ttk.Frame(teshis)
        satir.pack(fill="x", padx=5, pady=5)
        ttk.Label(satir, text="Teşhis:").pack(side="left")
        self.teshis_kutusu = ttk.Combobox(satir, state="readonly", width=38)
        self.teshis_kutusu.pack(side="left", padx=5)
        ttk.Label(satir, text="Açıklama:").pack(side="left")
        self.aciklama_kutusu = ttk.Entry(satir, width=18)
        self.aciklama_kutusu.pack(side="left", padx=5)
        ttk.Button(satir, text="Ekle", command=self.teshis_ekle).pack(side="left")

        self.teshis_tablosu = ttk.Treeview(teshis, columns=("kod", "ad", "aciklama"),
                                           show="headings", height=6)
        self.teshis_tablosu.heading("kod", text="Kod")
        self.teshis_tablosu.heading("ad", text="Teşhis")
        self.teshis_tablosu.heading("aciklama", text="Açıklama")
        self.teshis_tablosu.column("kod", width=70)
        self.teshis_tablosu.column("ad", width=260)
        self.teshis_tablosu.column("aciklama", width=220)
        self.teshis_tablosu.pack(fill="both", expand=True, padx=5, pady=5)

        # Alt düğmeler
        alt = ttk.Frame(self)
        alt.pack(fill="x", padx=10, pady=10)
        self.durum_yazisi = ttk.Label(alt, text="")
        self.durum_yazisi.pack(side="left")
        ttk.Button(alt, text="Kapat", command=self.destroy).pack(side="right")
        self.recete_dugmesi = ttk.Button(alt, text="Reçete yaz", command=self.recete_ac)
        self.recete_dugmesi.pack(side="right", padx=5)
        self.kaydet_dugmesi = ttk.Button(alt, text="Muayeneyi kaydet", command=self.muayene_kaydet)
        self.kaydet_dugmesi.pack(side="right")

        self.teshis_listesini_yukle()
        self.randevuyu_yukle()

    # ---------- yükleme ----------

    def teshis_listesini_yukle(self):
        """Teşhis kataloğunu (ICD-10 listesi) seçme kutusuna doldurur."""
        try:
            teshisler = db.getir("SELECT teshis_kodu, teshis_adi FROM teshis ORDER BY teshis_kodu")
        except (psycopg2.Error, RuntimeError) as hata:
            messagebox.showerror("Hata", db.hata_mesaji(hata), parent=self)
            teshisler = []
        # Kutuda "J06.9 - Akut üst solunum yolu enfeksiyonu" gibi görünür
        self.teshisler = {f"{kod} - {ad}": (kod, ad) for kod, ad in teshisler}
        self.teshis_kutusu["values"] = list(self.teshisler)

    def randevuyu_yukle(self):
        """Randevu bilgisini ve varsa daha önce girilmiş muayeneyi getirir."""
        try:
            randevu = db.getir_tek("""
                SELECT h.ad || ' ' || h.soyad,
                       COALESCE(d.unvan || ' ', '') || d.ad || ' ' || d.soyad,
                       to_char(r.randevu_tarihi, 'DD.MM.YYYY'), to_char(r.randevu_saati, 'HH24:MI'),
                       r.durum
                FROM randevu r
                JOIN hasta h ON h.hasta_id = r.hasta_id
                JOIN doktor d ON d.doktor_id = r.doktor_id
                WHERE r.randevu_id = %s
            """, (self.randevu_id,))
            muayene = db.getir_tek("""
                SELECT muayene_id, sikayet, notlar
                FROM muayene
                WHERE randevu_id = %s
            """, (self.randevu_id,))
        except (psycopg2.Error, RuntimeError) as hata:
            messagebox.showerror("Hata", db.hata_mesaji(hata), parent=self)
            return

        if randevu is None:
            messagebox.showerror("Hata", "Randevu bulunamadı.", parent=self)
            self.destroy()
            return

        hasta, doktor, tarih, saat, durum = randevu
        self.randevu_bilgisi.config(text=f"Hasta: {hasta}    Doktor: {doktor}    {tarih} {saat}")

        if muayene is None:
            if durum == "iptal":
                # İptal edilmiş randevuya muayene girilmez
                self.durum_yazisi.config(text="Bu randevu iptal edilmiş, muayene girilemez.")
                self.kaydet_dugmesi.state(["disabled"])
            else:
                self.durum_yazisi.config(text="Yeni muayene: en az bir teşhis ekleyip kaydedin.")
            self.recete_dugmesi.state(["disabled"])
        else:
            self.kayitli_muayeneyi_goster(*muayene)

    def kayitli_muayeneyi_goster(self, muayene_id, sikayet, notlar):
        """Kaydedilmiş muayenenin bilgilerini ve teşhislerini gösterir."""
        self.muayene_id = muayene_id
        for kutu, deger in ((self.sikayet_kutusu, sikayet), (self.notlar_kutusu, notlar or "")):
            kutu.config(state="normal")
            kutu.delete("1.0", "end")
            kutu.insert("1.0", deger)
            kutu.config(state="disabled")      # kayıtlı muayenenin şikâyeti değiştirilmez

        self.kaydet_dugmesi.state(["disabled"])
        self.recete_dugmesi.state(["!disabled"])
        self.durum_yazisi.config(text=f"Muayene no: {muayene_id} (kayıtlı)")
        self.teshisleri_listele()

    def teshisleri_listele(self):
        """Kayıtlı muayenenin teşhislerini muayene_teshis tablosundan getirir."""
        try:
            teshisler = db.getir("""
                SELECT t.teshis_kodu, t.teshis_adi, mt.aciklama
                FROM muayene_teshis mt
                JOIN teshis t ON t.teshis_kodu = mt.teshis_kodu
                WHERE mt.muayene_id = %s
                ORDER BY t.teshis_kodu
            """, (self.muayene_id,))
        except (psycopg2.Error, RuntimeError) as hata:
            messagebox.showerror("Hata", db.hata_mesaji(hata), parent=self)
            return
        self.teshis_tablosu.delete(*self.teshis_tablosu.get_children())
        for kod, ad, aciklama in teshisler:
            self.teshis_tablosu.insert("", "end", values=(kod, ad, aciklama or ""))

    # ---------- işlemler ----------

    def teshis_ekle(self):
        """Seçilen teşhisi ekler.

        Muayene henüz kaydedilmediyse teşhis sadece listeye eklenir, muayeneyle birlikte kaydedilir.
        Muayene kayıtlıysa teşhis hemen muayene_teshis tablosuna yazılır.
        """
        secim = self.teshis_kutusu.get()
        if not secim:
            messagebox.showwarning("Uyarı", "Lütfen listeden bir teşhis seçin.", parent=self)
            return
        kod, ad = self.teshisler[secim]
        aciklama = self.aciklama_kutusu.get().strip() or None

        if self.muayene_id is None:
            # Aynı teşhis aynı muayeneye iki kez eklenemez (FG-15)
            if any(t[0] == kod for t in self.bekleyen_teshisler):
                messagebox.showwarning("Uyarı", "Bu teşhis zaten eklendi.", parent=self)
                return
            self.bekleyen_teshisler.append((kod, ad, aciklama))
            self.teshis_tablosu.insert("", "end", values=(kod, ad, aciklama or ""))
        else:
            try:
                db.calistir("""
                    INSERT INTO muayene_teshis (muayene_id, teshis_kodu, aciklama)
                    VALUES (%s, %s, %s)
                """, (self.muayene_id, kod, aciklama))
            except (psycopg2.Error, RuntimeError) as hata:
                # Aynı teşhis tekrar eklenirse birincil anahtar hatası gelir,
                # db.hata_mesaji bunu "Bu teşhis bu muayeneye zaten eklenmiş." diye çevirir.
                messagebox.showerror("Hata", db.hata_mesaji(hata), parent=self)
                return
            self.teshisleri_listele()

        self.teshis_kutusu.set("")
        self.aciklama_kutusu.delete(0, "end")

    def muayene_kaydet(self):
        """Muayeneyi ve listeye eklenen teşhisleri kaydeder."""
        sikayet = self.sikayet_kutusu.get("1.0", "end").strip()
        notlar = self.notlar_kutusu.get("1.0", "end").strip() or None

        # Zorunlu alan kontrolü (FG-27)
        if not sikayet:
            messagebox.showwarning("Uyarı", "Şikâyet alanı boş bırakılamaz.", parent=self)
            return
        if not self.bekleyen_teshisler:
            messagebox.showwarning("Uyarı", "Muayeneye en az bir teşhis eklemelisiniz.", parent=self)
            return

        try:
            # Tarih yazmıyoruz, veritabanı varsayılan olarak bugünün tarihini koyar.
            # Bu INSERT'ten sonra trigger randevunun durumunu 'tamamlandi' yapar (FG-14).
            muayene_id = db.ekle("""
                INSERT INTO muayene (randevu_id, sikayet, notlar)
                VALUES (%s, %s, %s)
                RETURNING muayene_id
            """, (self.randevu_id, sikayet, notlar))
            for kod, ad, aciklama in self.bekleyen_teshisler:
                db.calistir("""
                    INSERT INTO muayene_teshis (muayene_id, teshis_kodu, aciklama)
                    VALUES (%s, %s, %s)
                """, (muayene_id, kod, aciklama))
        except (psycopg2.Error, RuntimeError) as hata:
            # Bu randevunun zaten muayenesi varsa UNIQUE hatası gelir (FG-13)
            messagebox.showerror("Hata", db.hata_mesaji(hata), parent=self)
            return

        self.bekleyen_teshisler = []
        messagebox.showinfo("Bilgi", "Muayene kaydedildi.", parent=self)
        self.kayitli_muayeneyi_goster(muayene_id, sikayet, notlar)

    def recete_ac(self):
        """Muayene için reçete ekranını açar (reçete ekranı Veronika'nın modülünde)."""
        if self.muayene_id is None:
            messagebox.showwarning("Uyarı", "Reçete yazmak için önce muayeneyi kaydedin.", parent=self)
            return
        try:
            from recete_ekrani import ReceteEkrani
        except ImportError:
            messagebox.showinfo("Bilgi", "Reçete ekranı henüz eklenmedi.", parent=self)
            return
        ReceteEkrani(self, self.muayene_id)


if __name__ == "__main__":
    # Ekranı tek başına denemek için: python muayene_ekrani.py <randevu_id>
    import sys
    kok = tk.Tk()
    kok.withdraw()
    ekran = MuayeneEkrani(kok, int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    ekran.protocol("WM_DELETE_WINDOW", kok.destroy)
    kok.mainloop()
