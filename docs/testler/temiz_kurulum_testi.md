# Test: Temiz Kurulum (Projeyi Sıfırdan Kurmak)

Test eden: Sude
Tarih: 18.11.2026

Amaç: Projeyi hiç görmemiş biri (hoca) sadece README.md ve docs/kurulum.md'yi okuyarak projeyi kurup çalıştırabiliyor mu?

## Ortam

- Windows 11, PostgreSQL 18.6, Python 3.14
- Repo GitHub'dan boş bir klasöre yeniden klonlandı (son commit 29548f9).
- Python kütüphaneleri için boş bir sanal ortam (venv) kullanıldı.
- Ekibin veritabanına dokunmamak için ayrı bir veritabanı açıldı: `hastane_randevu_temiz`. Bunun için `app/config.py` dosyasında `dbname` değiştirildi. Test bitince veritabanı ve klasör silindi.

## Sonuçlar

| # | Adım | Beklenen | Gerçek | Sonuç |
|---|---|---|---|---|
| 1 | README'deki `psql -U postgres -d ... -f sql/00_kurulum.sql` komutu | Çalışmalı | Windows'ta `psql` komutu bulunamadı (PATH'te değil). Tam yolla (`C:\Program Files\PostgreSQL\18\bin\psql.exe`) çalıştı. | ⚠️ belge eksiği (Bulgu 1) |
| 2 | `00_kurulum.sql` tam yolla | Hatasız, sadece NOTICE | Hatasız. 11 NOTICE ("table ... does not exist, skipping"), ilk kurulumda normal. | ✅ |
| 3 | Tablo, görünüm, trigger | 10 tablo, 1 görünüm, 1 trigger | 10 tablo, `recete_detay` görünümü, `trg_muayene_randevu_tamamla` trigger'ı | ✅ |
| 4 | Kayıt sayıları | 5 bölüm, 10 doktor, 15 hasta, 25 randevu, 15 muayene, 15 teşhis, 27 muayene_teshis, 15 ilaç, 13 reçete, 28 recete_ilac | Hepsi aynı. Randevular: 15 tamamlandi, 5 iptal, 5 aktif. | ✅ |
| 5 | `python -m pip install -r requirements.txt` | psycopg2 kurulmalı | psycopg2-binary 2.9.13 kuruldu | ✅ (ama README'de yazmıyor, Bulgu 2) |
| 6 | `app/config.py` oluşturma | Belgede anlatılmalı | README ve kurulum.md'de yok. Sadece `config.example.py` dosyasının içindeki yorumda ve `python db.py` hata mesajında yazıyor. | ⚠️ belge eksiği (Bulgu 3) |
| 7 | `python db.py` (app klasöründe) | Bağlantı başarılı | PostgreSQL 18.6, 10 tablonun kayıt sayıları, "Bağlantı başarılı." | ✅ (ama belgede yazmıyor, Bulgu 4) |
| 8 | `python main.py` | Ana menü açılmalı, bağlantı hatası olmamalı | Açıldı, hata yok | ✅ (ama belgede yazmıyor, Bulgu 4) |
| 9 | Hasta İşlemleri | Liste dolu | 15 hasta | ✅ |
| 10 | Randevu İşlemleri | Bölüm listesi dolu | 5 bölüm (randevu listesi hasta seçilince doluyor) | ✅ |
| 11 | Bölümler ve Doktorlar | Liste dolu | 5 bölüm, seçili bölümde 2 doktor | ✅ |
| 12 | Doktor Paneli | Doktor listesi dolu | 10 doktor. Açılışta bugünün tarihi geliyor, o gün randevu olmadığı için liste boş (beklenen). | ✅ |
| 13 | Reçete | Muayene listesi dolu | 15 muayene | ✅ |
| 14 | İstatistikler | 3 sekme dolu | 15 ilaç, 5 bölüm, 10 doktor | ✅ |

### Uçtan uca senaryo

| # | Adım | Beklenen | Gerçek | Sonuç |
|---|---|---|---|---|
| E1 | Yeni hasta: Kemal Yurt, TC 10000001766, 14.02.1979 | Kaydedilmeli | "Hasta kaydedildi (no: 16)." | ✅ |
| E2 | Randevu: Kardiyoloji, Doç. Dr. Elif Yıldız, 07.12.2026 10:00 | Randevu aktif olarak oluşmalı | Randevu 26, durum aktif | ✅ |
| E3 | Aynı doktora aynı tarih ve saatte ikinci randevu | Engellenmeli | "Bu doktorun bu tarih ve saatte başka bir randevusu var." | ✅ |
| E4 | Doktor paneli: Elif Yıldız, 2026-12-07 | Randevu listede görünmeli | 10:00 Kemal Yurt, aktif | ✅ |
| E5 | Doktor panelinde tarihi randevu ekranındaki gibi `07.12.2026` yazmak | Kabul edilmeli | "Tarihi YYYY-AA-GG biçiminde yazın" uyarısı | ❌ (Bulgu 5) |
| E6 | Muayene: şikâyet ve 2 teşhis (I20.9, I10), kaydet | Muayene kaydedilmeli, randevu "tamamlandi" olmalı | Muayene 16, 2 teşhis, randevu durumu tamamlandi (trigger çalıştı) | ✅ |
| E7 | "Reçete yaz" → reçete oluştur → ilaç ekle (Arveles 25 mg, 1x1) | Reçete ve ilaç kaydedilmeli | Reçete 14, 1 ilaç | ✅ |
| E8 | İstatistik ekranında "Yenile" | Sayılar artmalı | Arveles 25 mg: 2 → 3 reçete; Kardiyoloji hasta sayısı: 4 → 5; Elif Yıldız muayene sayısı: 1 → 2 | ✅ |

Özet: Veritabanı kurulumu ve uygulama sorunsuz çalışıyor; 6 ekranın hepsi açılıyor ve uçtan uca senaryo baştan sona tamamlanıyor. Sorunlar çoğunlukla belgelerde: bazı adımlar sadece ekibin bildiği şeylere dayanıyor.

## Bulgular ve önerilen düzeltmeler

Bu testte README.md, docs/kurulum.md, app ve sql dosyaları değiştirilmedi. Düzeltmeleri dosyanın sahibi yapacak.

**Bulgu 1 – Windows'ta `psql` komutu bulunamıyor.** (README.md, docs/kurulum.md)
PostgreSQL'in Windows kurulumu `psql`'i PATH'e eklemiyor. Bu yüzden README'deki komut "'psql' is not recognized…" hatası veriyor. kurulum.md'de sadece Mac için tam yol notu var.
Öneri: Windows için tam yolu ekleyin:
```
"C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d hastane_randevu -f sql/00_kurulum.sql
```
ya da `C:\Program Files\PostgreSQL\18\bin` klasörünü PATH'e eklemeyi anlatın.

**Bulgu 2 – `requirements.txt` kullanılmıyor.** (README.md, docs/kurulum.md)
Repoda `requirements.txt` var ama iki belge de ondan bahsetmiyor; kurulum.md tek tek `python -m pip install psycopg2-binary` diyor.
Öneri: README'nin Kurulum bölümüne `python -m pip install -r requirements.txt` adımını ekleyin. Böylece kütüphane sürümü de sabit kalır.

**Bulgu 3 – `config.py` dosyasının nasıl oluşturulacağı yazmıyor.** (README.md, docs/kurulum.md)
Uygulama `app/config.py` olmadan açılmıyor. Bu dosyanın `config.example.py`'den kopyalanıp şifrenin yazılması gerektiği belgelerde yok; sadece `config.example.py`'nin içindeki yorumda var.
Öneri: README'ye şu adımı ekleyin: "`app/config.example.py` dosyasını aynı klasörde `config.py` adıyla kopyalayın ve `password` kısmına kendi postgres şifrenizi yazın. Veritabanının adı farklıysa `dbname`'i de değiştirin."

**Bulgu 4 – Uygulamanın nasıl çalıştırılacağı yazmıyor.** (README.md)
README kurulumu veritabanı kurulunca bitiriyor. `app` klasörüne geçip `python db.py` (bağlantı testi) ve `python main.py` (uygulama) komutları yok. kurulum.md'deki bağlantı testi ise şifrenin elle yazıldığı ayrı bir `baglanti_testi.py` dosyası kullanıyor; artık bunun yerine `python db.py` kullanılabilir.
Öneri: README'ye "Çalıştırma" başlığı ekleyin:
```
cd app
python db.py      (bağlantı testi: tabloların kayıt sayılarını yazar)
python main.py    (uygulama)
```
Mac'te `python3`.

**Bulgu 5 – Ekranlar arasında tarih biçimi farklı.** (app/doktor_paneli.py, Sude)
Hasta ve randevu ekranları tarihi GG.AA.YYYY (örn. 07.12.2026) biçiminde alıyor, doktor paneli ise YYYY-AA-GG (örn. 2026-12-07). Randevuyu veren görevli ile paneli kullanan doktor farklı biçim yazmak zorunda kalıyor; demo sırasında karışabilir.
Öneri: Doktor paneli iki biçimi de kabul etsin ve açılışta tarihi GG.AA.YYYY göstersin. (Sude düzeltecek.)

**Not – Muayene tarihi.** Muayene kaydında tarih yazılmadığı için veritabanı bugünün tarihini koyuyor. Test gibi ileri tarihli bir randevuya bugünden muayene girilirse muayene tarihi randevu tarihinden önce görünüyor. Gerçek kullanımda doktor muayeneyi randevu günü gireceği için sorun değil, sadece bilgi olarak yazıldı.

**Küçük not – Tkinter.** Windows'ta Python ile birlikte geliyor. Mac/Linux'ta bazen ayrıca kurmak gerekiyor (`python3-tk`). kurulum.md'deki Mac notlarına bir satır eklenebilir.
