# Test: Veronika'nın Modülü (Ana Menü, Reçete, İstatistik)

Test eden: Sude
Tarih: 18.11.2026

Veritabanı `sql/00_kurulum.sql` ile baştan kuruldu, uygulama `python main.py` ile açıldı.

## Sonuçlar

| # | Ne denendi | Beklenen | Sonuç |
|---|---|---|---|
| 1 | Ana menüden altı ekranın açılması | Hepsi açılmalı | ✅ |
| 2 | Muayene ekranında "Reçete yaz" | Reçete ekranı o muayene seçili ve kilitli açılmalı | ✅ |
| 3 | Reçetesi olmayan muayene | "İlaç Ekle" kapalı olmalı | ✅ |
| 4 | Reçete oluşturma (FG-17) | Reçete numarası ve tarihi görünmeli | ✅ |
| 5 | Aynı muayeneye ikinci reçete | Engellenmeli | ✅ "Reçete Oluştur" kapanıyor |
| 6 | İlaç ya da doz boşken "İlaç Ekle" | Uyarı vermeli | ✅ "İlaç ve doz boş bırakılamaz." |
| 7 | Reçeteye iki ilaç ekleme (FG-18, FG-20) | İkisi de listede görünmeli | ✅ |
| 8 | Aynı ilacı ikinci kez ekleme (FG-19) | Hata mesajı | ✅ "Bu ilaç bu reçeteye zaten eklenmiş." |
| 9 | Kutu adedi 0 | Reddedilmeli | ✅ "Kutu adedi en az 1 olmalı." |
| 10 | Kutu adedine harf yazma | Reddedilmeli | ✅ "Kutu adedi bir sayı olmalı." |
| 11 | Seçili ilacı çıkarma | Listeden silinmeli | ✅ |
| 12 | Hastanın geçmiş reçeteleri (FG-21) | Eski ve yeni reçeteler görünmeli | ✅ |
| 13 | Ana menüden Reçete ekranı | Muayene listesi dolu, seçim açık olmalı | ✅ |
| 14 | İstatistik ekranı (FG-23, FG-24, FG-25) | Üç sekme de dolu olmalı | ✅ |
| 15 | Doktor başına muayene toplamı | Muayene tablosundaki kayıt sayısına eşit olmalı | ✅ |
| 16 | Bölümlere göre hasta sayısı | Sude'nin sorgu 1 sonucuyla aynı olmalı | ✅ |
| 17 | Unvanı boş bir doktor eklenince istatistik ekranı | Doktorun adı görünmeli | ❌ |

## Bulunan hata

**17 - Unvanı boş olan doktorun adı görünmüyor.**

`doktor.unvan` sütunu boş olabiliyor (NULL). Doktor adı `d.unvan || ' ' || d.ad || ' ' || d.soyad` şeklinde birleştiriliyor. PostgreSQL'de NULL ile birleştirilen metin de NULL olduğu için unvanı boş bir doktorun adı tamamen kayboluyor. İstatistik ekranında bu doktorun adı yerine "None" yazıyor.

Aynı birleştirme şu yerlerde de var:

- `app/istatistik_ekrani.py`: Doktor Başına Muayene sekmesi
- `app/recete_ekrani.py`: muayene seçme listesi
- `sql/04_ilac_recete.sql`: `recete_detay` görünümündeki `doktor` sütunu (geçmiş reçeteler penceresi)

Örnek verilerde bütün doktorların unvanı olduğu için şu an ekranda görünmüyor, ama unvansız yeni bir doktor eklenirse ortaya çıkar.

Önerilen düzeltme: `COALESCE(d.unvan || ' ', '') || d.ad || ' ' || d.soyad` (Sude'nin doktor paneli ve muayene ekranında bu şekilde yazıldı).
