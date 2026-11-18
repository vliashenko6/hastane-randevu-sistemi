# Canlı Demo Senaryosu: Hasta Kaydı ve Randevu

Hazırlayan: Eray
Sunumdaki yeri: 6. bölüm (ilk demo; Sude'nin doktor paneli demosundan önce)
Süre: yaklaşık 3 dakika

## Demodan önce

- Veritabanı sunumdan önce `sql/00_kurulum.sql` ile bir kez sıfırlanmış olmalı (bkz. Sude'nin senaryosu). Ben ayrıca sıfırlama yapmıyorum, sıfırlamayı benim demomdan önce yapıyoruz.
- Uygulama `app` klasöründe `python main.py` ile açık, ana menü geliyor.
- Demo **Prof. Dr. Hakan Aydın'ın 01.12.2026 09:00 randevusuna (randevu 21) dokunmuyor.** O randevu Sude ve Veronika'nın demosunda kullanılıyor. Ben Uzm. Dr. Murat Kaya (Dahiliye) ile çalışıyorum.
- Yeni hastanın TC'si veritabanında yok: 55512345678 (Kerem Aksoy). Sıfırlama sonrası kayıt yok, ilk kez eklenecek.
- Bugünün tarihi 18.11.2026 ya da sonrası olmalı. Geçmiş tarih örneği olarak 10.11.2026 kullanıyorum.

## Demo adımları

### 1. Hasta kaydı (1 dakika)

| Tıkla / yap | Söyle |
|---|---|
| Ana menüde **Hasta İşlemleri** | "Hasta kaydı bu ekrandan yapılıyor. Önce yanlış girişlerin nasıl engellendiğini gösteriyorum." |
| TC: **12345**, diğer alanları boş bırak, **Kaydet** | "TC 11 rakam olmak zorunda. Hem uygulama hem veritabanındaki CHECK kısıtı bunu kontrol ediyor." |
| TC: **55512345678**, Ad: **Kerem**, Soyad: **Aksoy**, Doğum: **14.03.1990**, Cinsiyet: **E**, Telefon boş, **Kaydet** | "Telefon zorunlu alan. Boşsa kayıt yapılmıyor." |
| Telefon: **05321234567**, Adres: **Kadıköy, İstanbul**, **Kaydet** | "Hasta kaydedildi, numarasını veritabanı SERIAL ile kendisi verdi." |
| **Formu Temizle**, TC: **10000000146** ile başka bir hasta kaydetmeyi dene (ad ve soyad yaz, diğerlerini doldur) | "Bu TC zaten kayıtlı. tc_no sütunu UNIQUE olduğu için veritabanı reddediyor, db.py bunu Türkçe mesaja çeviriyor." |
| Aramaya **Aksoy** yaz, **Ara** | "Arama TC ile de ad soyad ile de çalışıyor. Güncelleme sadece telefon ve adresi değiştirebiliyor; TC, ad ve doğum tarihi kilitli." |
| Pencereyi kapat | |

### 2. Randevu alma (1 dakika)

| Tıkla / yap | Söyle |
|---|---|
| Ana menüde **Randevu İşlemleri** | |
| TC: **55512345678**, **Hastayı Bul** | "Önce hasta bulunuyor, randevu hastaya bağlanıyor." |
| Bölüm: **Dahiliye**, Doktor: **Uzm. Dr. Murat Kaya**, Tarih: **10.11.2026**, Saat: **10:00**, **Randevu Al** | "Geçmiş tarihe randevu verilmiyor." |
| Tarih: **03.12.2026**, Saat: **10:30**, **Randevu Al** | "Randevu oluştu ve hastanın randevu listesinde aktif olarak göründü." |

### 3. Çift randevu engeli (1 dakika)

| Tıkla / yap | Söyle |
|---|---|
| Aynı doktor, Tarih: **03.12.2026**, Saat: **10:30**, **Randevu Al** | "Aynı doktora aynı gün ve saate ikinci randevu verilemiyor. Uygulama önce kontrol ediyor." |
| Tarih: **02.12.2026**, Saat: **10:00**, **Randevu Al** | "Bu saatte Murat Kaya'nın başka bir hastaya ait randevusu zaten var, o da engellendi." |
| Listeden 03.12.2026 10:30 randevusunu seç, **Seçili Randevuyu İptal Et** | "İptal edilince randevu silinmiyor, durumu iptal oluyor." |
| Aynı doktor ve saat için tekrar **Randevu Al** | "İptal edilmiş randevu saati bloke etmiyor, yeni randevu alınabildi. Çünkü kural kısmi bir indeks: uq_cift_randevu sadece durumu iptal olmayan satırlarda doktor, tarih ve saatin tekrarını yasaklıyor." |
| Sözü bitir | "Ekran kontrolü atlansa bile aynı kuralı veritabanı indeksi de koruyor. Şimdi Sude doktor tarafını gösterecek." |

## Bir şey ters giderse

| Sorun | Çözüm |
|---|---|
| "Bu TC ile kayıtlı hasta yok" | Hasta ekranında 55512345678'i kaydetmeyi unutmuşuz; önce kaydet. |
| Kerem Aksoy zaten kayıtlı (prova yapıldı) | Veritabanını `sql/00_kurulum.sql` ile sıfırla ya da başka bir TC ve saat kullan. Randevu 21'e dokunma. |
| 03.12.2026 10:30 dolu | Provadan kalmış aktif randevudur, listeden iptal et ya da 03.12.2026 11:00 kullan. |
| Uygulama açılmıyor | PostgreSQL çalışıyor mu ve `app/config.py` şifresi doğru mu kontrol et. |
