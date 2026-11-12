# Hastane Randevu Sistemi

**Veri Tabanı Sistemleri (BİM 381) dersi grup projesi**

Bu proje, hayali müşterimiz **Doğuş Özel Hastanesi** için geliştirilen bir hastane randevu ve muayene takip sistemidir. Projede PostgreSQL üzerinde bir veritabanı tasarlanır ve bu veritabanını kullanan Python + Tkinter tabanlı bir masaüstü uygulaması geliştirilir.

## Müşteri ve Problem

Doğuş Özel Hastanesi'nde randevular telefonla alınıyor, kâğıt ya da dağınık Excel dosyalarında tutuluyor. Bunun sonucunda:

- Aynı doktora aynı saatte **çift randevu** verilebiliyor.
- Hastanın geçmiş randevularına, muayenelerine ve teşhislerine hızlıca ulaşılamıyor.
- Doktorlar günlük hasta listelerini önceden göremiyor.
- Reçeteler kâğıt üzerinde kalıyor, yazılan ilaçlar takip edilemiyor.
- Yönetim bölüm yoğunluğu gibi istatistikleri raporlayamıyor.

Bu sistem tüm bu bilgileri ilişkisel bir veritabanında toplar ve bir arayüz üzerinden yönetilmesini sağlar.

## Sistemin Özellikleri

- **Hasta işlemleri:** kayıt, güncelleme, TC kimlik no ile arama
- **Randevu işlemleri:** bölüm ve doktor seçerek randevu alma, çakışma kontrolü, iptal, randevu geçmişi
- **Doktor paneli:** seçilen gündeki randevuların listesi
- **Muayene ve teşhis:** randevuya bağlı muayene ve teşhis kaydı
- **Reçete ve ilaç:** bir reçeteye doz ve kullanım şekliyle birden fazla ilaç ekleme
- **İstatistikler:** en çok yazılan ilaçlar, bölüm bazında hasta sayısı, doktor başına muayene sayısı

## Veritabanı Tabloları (Taslak)

| Tablo | Açıklama |
|---|---|
| `hasta` | Hastanın kimlik ve iletişim bilgileri |
| `randevu` | Hasta, doktor, tarih, saat ve randevu durumu |
| `bolum` | Poliklinikler |
| `doktor` | Doktor bilgileri (her doktor bir bölüme bağlı) |
| `muayene` | Randevu sonucunda yapılan muayene |
| `teshis` | Muayenede konulan teşhisler |
| `ilac` | İlaç kataloğu |
| `recete` | Muayene sonucunda yazılan reçete |
| `recete_ilac` | Reçete ↔ İlaç N–N ilişkisinin ara tablosu |

> Tablo ve sütun isimleri küçük harfle, Türkçe karakter kullanılmadan ve alt çizgiyle yazılır (örn. `hasta_id`, `dogum_tarihi`).

## Kullanılan Teknolojiler

- **PostgreSQL** + pgAdmin: veritabanı
- **Python 3**: uygulama dili
- **psycopg2**: Python–PostgreSQL bağlantısı
- **Tkinter**: masaüstü arayüz
- **draw.io**: ER ve UML diyagramları
- **Git & GitHub**: sürüm kontrolü

## Klasör Yapısı

```
hastane-randevu-sistemi/
├── sql/        # CREATE TABLE, INSERT ve sorgu scriptleri
├── app/        # Python + Tkinter uygulaması
├── docs/       # ER/UML diyagramları, ekran görüntüleri, proje planı, kurulum notları
├── rapor/      # Proje raporu
└── README.md
```

## Ekip

| Üye | Sorumlu Olduğu Modül |
|---|---|
| Veronika Liashenko | Reçete + İlaç, veritabanı bağlantısı, ana menü |
| Eray | Hasta + Randevu |
| Sude | Doktor + Bölüm + Muayene + Teşhis |

Ayrıntılı iş dağılımı için: [docs/Hastane_Randevu_Proje_Plani.pdf](docs/Hastane_Randevu_Proje_Plani.pdf)
Commit kuralları için: [docs/commit_kurallari.md](docs/commit_kurallari.md)

## Kurulum ve Çalıştırma

*(Proje ilerledikçe güncellenecektir.)*
