# Canlı Demo Senaryosu: Doktor Paneli, Muayene ve Teşhis

Hazırlayan: Sude
Sunumdaki yeri: 7. bölüm (Eray'ın hasta ve randevu demosundan sonra, Veronika'nın reçete demosundan önce)
Süre: yaklaşık 3–4 dakika

## Demodan önce (sunumdan 10 dakika önce)

1. **Veritabanını sıfırla.** Demo veritabanını değiştiriyor: muayene ekliyor ve randevunun durumunu "tamamlandi" yapıyor. Prova ya da önceki bir deneme yapıldıysa 21 numaralı randevu artık aktif olmaz. Bu yüzden demodan hemen önce veritabanını baştan kur:

   ```
   psql -U postgres -d hastane_randevu -f sql/00_kurulum.sql
   ```

   Eray'ın demosu da veriyi değiştirdiği için bu komutu **Eray'ın demosundan önce bir kez** çalıştırmak yeterli. Eray'ın demosu Hakan Aydın'ın 1 Aralık 09:00 randevusuna dokunmamalı.

2. `app` klasöründe uygulamayı aç ve ana menünün geldiğini kontrol et:

   ```
   python main.py
   ```

   Açılışta "Bağlantı hatası" çıkarsa PostgreSQL çalışmıyordur ya da `app/config.py` içindeki şifre yanlıştır.

3. Ekran yansıtılırken yazılar okunsun diye pencereleri büyük aç.

## Demo adımları

### 1. Bölümler ve doktorlar (30 saniye)

| Tıkla / yap | Söyle |
|---|---|
| Ana menüde **Bölümler ve Doktorlar** | "Hastanede beş bölüm var, her birinde iki doktor çalışıyor." |
| Soldan **Kardiyoloji**'yi seç | "Bir bölüm seçince o bölümün doktorları geliyor. Doktor tablosu bölüme bolum_id yabancı anahtarıyla bağlı, 1–N ilişki." |
| Pencereyi kapat | |

### 2. Doktor paneli (1 dakika)

| Tıkla / yap | Söyle |
|---|---|
| Ana menüde **Doktor Paneli** | "Doktor burada kendi gününü görüyor." |
| Doktor: **Prof. Dr. Hakan Aydın (Kardiyoloji)** | |
| Tarih kutusunu sil, **01.12.2026** yaz, **Listele** | "1 Aralık'ta saat 09:00'da Emine Çetin'in randevusu var, durumu aktif, muayenesi yapılmamış." |
| (İsteğe bağlı) | "Aynı saatte iptal edilmiş bir randevu daha var (randevu 19), ama iptal edilenler listede gösterilmiyor." |
| **Emine Çetin** satırına çift tıkla | "Randevuya çift tıklayınca muayene ekranı açılıyor." |

### 3. Muayene ve teşhis girişi (1,5 dakika)

| Tıkla / yap | Söyle |
|---|---|
| Hiçbir şey yazmadan **Muayeneyi kaydet** | "Şikâyet boşken kayıt yapılmıyor, uyarı çıkıyor." |
| Şikâyet: **Merdiven çıkarken nefes darlığı ve çarpıntı** | |
| Notlar: **Tansiyon 150/95 ölçüldü.** | |
| Tekrar **Muayeneyi kaydet** | "Teşhis girmeden de kaydedemiyoruz: her muayenede en az bir teşhis olmalı. Bu kontrolü uygulama yapıyor." |
| Teşhis listesinden **I10 - Esansiyel (primer) hipertansiyon**, **Ekle** | "Teşhisler ICD-10 kataloğundan, yani teshis tablosundan geliyor." |
| Teşhis: **R00.2 - Çarpıntı**, Açıklama: **Eforla artıyor**, **Ekle** | "Bir muayeneye birden fazla teşhis eklenebiliyor." |
| Tekrar **I10** seçip **Ekle** | "Aynı teşhis aynı muayeneye iki kez eklenemiyor. Veritabanında muayene_teshis tablosunun birincil anahtarı (muayene_id, teshis_kodu)." |
| **Muayeneyi kaydet** → "Muayene kaydedildi." | "Muayene ve iki teşhis kaydedildi. Muayene ile teşhis arasında N–N ilişki var, bunu muayene_teshis ara tablosu kuruyor." |

### 4. Trigger: randevu "tamamlandi" oldu (30 saniye)

| Tıkla / yap | Söyle |
|---|---|
| Muayene ekranında **Kapat** | |
| Doktor panelinde liste kendiliğinden yenilenir | "Randevunun durumu artık **tamamlandi**, Muayene sütununda **Yapıldı** yazıyor. Bunu Python yapmadı: muayene tablosuna INSERT olunca veritabanındaki trigger randevunun durumunu güncelledi." |
| Satıra tekrar çift tıkla | "Kayıtlı muayene açılınca şikâyet değiştirilemiyor ve ikinci muayene açılamıyor. Bir randevudan tek muayene çıkar; bu 1–1 ilişkiyi muayene.randevu_id üzerindeki UNIQUE kısıtı sağlıyor." |

### 5. Reçeteye geçiş (Veronika'ya devir)

| Tıkla / yap | Söyle |
|---|---|
| Muayene ekranında **Reçete yaz** | "Reçete yazmak için Veronika'nın ekranına geçiyoruz. Muayene seçili ve kilitli geliyor." |
| Sözü Veronika'ya bırak | "Reçeteyi Veronika anlatacak." |

## Bir şey ters giderse

| Sorun | Çözüm |
|---|---|
| Listede Emine Çetin yok ya da durumu "tamamlandi" | Veritabanı sıfırlanmamış. Sunumu bekletmeden **Prof. Dr. Murat Kaya**, **02.12.2026** ile devam et (randevu 22, Ali Erdem, 10:00). Diğer yedek seçenekler: Cem Şahin 03.12.2026, Burak Çelik 04.12.2026, Oğuz Polat 05.12.2026. |
| "Bu randevu için zaten bir muayene kaydı var." | Aynı şey: başka bir aktif randevu seç. |
| Bağlantı hatası | PostgreSQL servisini başlat, `app/config.py`'deki şifreyi kontrol et. |

## Hocanın sorabileceği sorular

- **Muayene ile randevu neden 1–1?** Bir randevuda hasta bir kez muayene olur. muayene.randevu_id UNIQUE olduğu için bir randevuya ikinci muayene bağlanamaz.
- **Muayene ile teşhis neden N–N?** Bir muayenede birden çok teşhis konabilir, aynı teşhis de birçok muayenede konabilir. Bu yüzden muayene_teshis ara tablosu var.
- **Teşhis tablosu hangi normal formda?** 3NF. teshis_kodu teşhisin adını belirliyor; adı her muayenede tekrar yazmamak için teşhisleri ayrı bir katalog tablosuna aldık.
- **Randevu nasıl "tamamlandi" oluyor?** muayene tablosundaki AFTER INSERT trigger'ı, eklenen muayenenin randevusunun durumunu güncelliyor.
