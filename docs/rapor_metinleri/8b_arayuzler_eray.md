# Hasta ve Randevu Ekranları (Eray)

Hazırlayan: Eray

Ekran görüntüleri `docs/ekran_goruntuleri/` klasöründe.

Ekranlar Python'un Tkinter kütüphanesiyle yazıldı. Her ekran ana menüden açılan ayrı bir penceredir.

## Hasta Ekranı (eray_hasta_ekrani.png)

Danışma görevlisi bu ekranda hasta kaydı yapar, hasta arar ve hastanın iletişim bilgilerini günceller (FG-01 – FG-04).

- **Hasta Bilgileri:** TC kimlik no, ad, soyad, doğum tarihi, cinsiyet, telefon ve adres yazılıp Kaydet düğmesine basılır. Doğum tarihi GG.AA.YYYY biçiminde yazılır.
- **Kontroller (FG-27):** TC 11 rakam olmalı, zorunlu alanlar boş olmamalı, doğum tarihi geçerli olmalı ve bugünden sonra olmamalı. Kurallara uymayan değerde uyarı çıkar. Aynı TC ile ikinci kayıt yapılırsa veritabanının verdiği "Bu TC kimlik numarasıyla kayıtlı bir hasta zaten var." mesajı gösterilir.
- **Arama:** Kutuya TC ya da ad soyad yazılıp Ara'ya basılır. Sonuçlar aşağıdaki tabloda listelenir.
- **Güncelleme:** Tablodan bir hasta seçilince bilgileri forma gelir. Sadece telefon ve adres değiştirilebilir, diğer alanlar kilitlenir. Yeni hasta girmek için Formu Temizle'ye basılır.

## Randevu Ekranı (eray_randevu_ekrani.png)

Danışma görevlisi bu ekranda randevu verir, iptal eder ve hastanın randevu geçmişine bakar (FG-05 – FG-09).

- **Hasta:** Önce hastanın TC numarası yazılıp Hastayı Bul'a basılır. Hasta bulununca adı gösterilir ve randevuları tabloya gelir.
- **Yeni Randevu:** Bölüm seçilince sadece o bölümün doktorları listelenir. Sonra tarih (GG.AA.YYYY) ve saat (SS:DD) yazılıp Randevu Al'a basılır.
- **Kontroller:** Geçmiş bir tarihe randevu verilemez (FG-07). Doktorun aynı gün ve saatte iptal edilmemiş başka randevusu varsa uyarı çıkar (FG-06).
- **İptal:** Listeden aktif bir randevu seçilip Seçili Randevuyu İptal Et'e basılır. Randevu silinmez, durumu "iptal" olur (FG-08). Aktif olmayan randevu iptal edilemez.
- **Randevu geçmişi:** Tabloda hastanın bütün randevuları tarih, saat, doktor, bölüm ve durumla gösterilir (FG-09).
