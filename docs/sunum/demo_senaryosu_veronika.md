# Canlı Demo Senaryosu: Reçete ve İstatistikler

Hazırlayan: Veronika
Sunumdaki yeri: 8. bölüm (Sude'nin muayene demosundan hemen sonra, sunumun son demosu)
Süre: yaklaşık 3 dakika

## Demodan önce

- Veritabanı, Eray'ın demosundan önce `sql/00_kurulum.sql` ile bir kez sıfırlanmış olmalı (bkz. Sude'nin senaryosu). Benim demom ayrıca sıfırlama istemiyor.
- Demo, Sude'nin demosunda açılan muayeneden devam ediyor: **Emine Çetin, Prof. Dr. Hakan Aydın, 01.12.2026 09:00** (randevu 21). Sude muayeneyi kaydedip **Reçete yaz** düğmesine basınca reçete ekranı açılmış olacak.
- İstatistik ekranındaki sayıları demodan önce bir kez görmek için hiçbir şey yapmaya gerek yok; sayılar aşağıda yazıyor.

## Demo adımları

### 1. Reçete oluşturma (45 saniye)

| Tıkla / yap | Söyle |
|---|---|
| (Reçete ekranı Sude'nin muayenesiyle açık) | "Muayene ekranından geldiğimiz için muayene seçili ve kilitli: Emine Çetin, Prof. Dr. Hakan Aydın. Bu muayeneye henüz reçete yazılmamış." |
| Açıklama: **Tansiyon takibi yapılacak.** | |
| **Reçete Oluştur** | "Reçete oluştu. Bir muayeneye tek reçete yazılabiliyor; recete tablosunda muayene_id UNIQUE. Reçete Oluştur düğmesi artık kapandı." |

### 2. İlaç ekleme (1 dakika)

| Tıkla / yap | Söyle |
|---|---|
| İlaç: **Norvasc 5 mg**, Doz: **1x1**, Kullanım şekli: **Sabah**, Kutu: **1**, **İlaç Ekle** | "Teşhis hipertansiyon olduğu için tansiyon ilacı yazıyoruz." |
| İlaç: **Beloc ZOK 50 mg**, Doz: **1x1**, Kullanım şekli: **Sabah**, **İlaç Ekle** | "Bir reçetede birden fazla ilaç olabiliyor. Her ilaç recete_ilac ara tablosuna ayrı bir satır olarak kaydediliyor." |
| Tekrar **Norvasc 5 mg**, Doz: **2x1**, **İlaç Ekle** | "Aynı ilacı ikinci kez ekleyemiyoruz: 'Bu ilaç bu reçeteye zaten eklenmiş.' Bunu veritabanındaki bileşik birincil anahtar (recete_id, ilac_id) engelliyor; db.py hatayı Türkçe mesaja çeviriyor." |
| (İsteğe bağlı) Doz boşken **İlaç Ekle** | "Zorunlu alan boşsa kayıt yapılmıyor." |

### 3. Hastanın geçmiş reçeteleri (30 saniye)

| Tıkla / yap | Söyle |
|---|---|
| **Hastanın Geçmiş Reçeteleri** | "Emine Çetin'e daha önce Ortopedi'de yazılmış reçete de geliyor: Majezik ve Voltaren. Bu liste recete_detay görünümünden (VIEW) okunuyor; reçeteyi muayene, randevu, hasta, doktor ve ilaç tablolarıyla birleştiren uzun JOIN'i görünüm olarak kaydettik." |
| Pencereyi ve reçete ekranını kapat | |

### 4. İstatistikler (45 saniye)

| Tıkla / yap | Söyle |
|---|---|
| Ana menüde **İstatistikler** | "Bu ekranı hastane yöneticisi kullanıyor." |
| **En Çok Yazılan İlaçlar** sekmesi | "Demodan önce Parol 4, Norvasc 3 reçetedeydi. Az önce yazdığımız reçeteyle Norvasc 4'e, Beloc 3'e çıktı. Sorgu ilaca göre GROUP BY yapıp COUNT ile sayıyor." |
| **Bölümlere Göre Hasta Sayısı** sekmesi | "Aynı hasta bir bölüme iki kez geldiyse bir kez sayılıyor: COUNT(DISTINCT hasta_id). İptal edilen randevular sayılmıyor." |
| **Doktor Başına Muayene** sekmesi | "Muayene randevu üzerinden doktora bağlı. Prof. Dr. Hakan Aydın'ın muayene sayısı az önce Sude'nin yaptığı muayeneyle bir arttı." |
| Sözü bitir | "Demolarımız bu kadar, sorularınızı alabiliriz." |

## Bir şey ters giderse

| Sorun | Çözüm |
|---|---|
| Reçete ekranı açılmadı / muayene gelmedi | Ana menüden **Reçete**'yi aç, listeden en üstteki (en yeni) muayeneyi seç: Emine Çetin, Prof. Dr. Hakan Aydın. |
| "Bu muayene için zaten bir reçete yazılmış." | Prova sırasında reçete yazılmış ve veritabanı sıfırlanmamış. Listeden reçetesi olmayan başka bir muayene seç (örneğin 7: miyopi, gözlük yazılmıştı) ve devam et. |
| Bağlantı hatası | PostgreSQL çalışmıyor ya da `app/config.py`'deki şifre yanlış. |
