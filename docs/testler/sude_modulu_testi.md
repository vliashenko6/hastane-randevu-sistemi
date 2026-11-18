# Test: Sude'nin Modülü (Bölümler ve Doktorlar, Doktor Paneli, Muayene)

Test eden: Eray
Tarih: 18.11.2026

GitHub'daki son kodu indirdim (Sude'nin doktor paneli değişikliği dahil), `config.py` dosyasını oluşturup veritabanını `sql/00_kurulum.sql` ile baştan kurdum. Ekranları gerçek veritabanıyla denedim: ekranları Python ile açıp düğme ve kutuları kod üzerinden çalıştırdım, çıkan uyarı metinlerini kaydettim. Testten sonra veritabanını yine `00_kurulum.sql` ile sıfırladım (randevu 22 tekrar aktif, muayene sayısı başlangıçtaki 15'e döndü).

## Bölümler ve Doktorlar ekranı (FG-10, FG-11)

| # | Ne denendi | Beklenen | Sonuç |
|---|---|---|---|
| 1 | Ekranı açtım | 5 bölüm listelenir | ✅ Dahiliye, Göz Hastalıkları, Kardiyoloji, Kulak Burun Boğaz, Ortopedi geldi. Her birinin yanında doktor sayısı 2 yazıyor. İlk bölüm kendiliğinden seçili. |
| 2 | Kardiyoloji'yi seçtim | Sadece o bölümün 2 doktoru gelir, unvan ve telefon görünür | ✅ Doç. Dr. Elif Yıldız (02160000102) ve Prof. Dr. Hakan Aydın (02160000101) geldi. |
| 3 | Başka bölüm seçtim (Göz Hastalıkları) | Liste değişir | ✅ Doç. Dr. Aylin Koç ve Uzm. Dr. Burak Çelik geldi, Kardiyoloji doktorları gitti. |

## Doktor Paneli (FG-12)

| # | Ne denendi | Beklenen | Sonuç |
|---|---|---|---|
| 4 | Paneli açtım | Tarih kutusunda bugünün tarihi GG.AA.YYYY biçiminde | ✅ 18.11.2026 yazıyordu. |
| 5 | Prof. Dr. Hakan Aydın, 03.11.2026, Listele | Randevular saat sırasıyla gelir | ✅ 09:00 Ahmet Yılmaz, 09:30 Ayşe Kara geldi. Altta "2 randevu" yazıyor. |
| 6 | Aynı doktor, 01.12.2026, Listele | Randevu 21 (Emine Çetin, 09:00, aktif) görünür, aynı saatteki iptal randevu (19) görünmez | ✅ Sadece Emine Çetin, 09:00, aktif geldi. İptal randevu listede yok. Bu randevuya muayene girmedim. |
| 7 | Tarihi 2026-12-01 biçiminde yazdım | Yine çalışır | ✅ Aynı randevu geldi. |
| 8 | Tarihe 31.02.2026 yazdım | Uyarı verir | ✅ "Tarihi GG.AA.YYYY biçiminde yazın" uyarısı çıktı. |
| 9 | Tarihe abc yazdım | Uyarı verir | ✅ Aynı uyarı çıktı. |
| 10 | Tarihi boş bıraktım | Uyarı verir | ✅ Aynı uyarı çıktı. |

## Muayene ekranı (FG-13 – FG-16), randevu 22

| # | Ne denendi | Beklenen | Sonuç |
|---|---|---|---|
| 11 | Doktor panelinde Murat Kaya, 02.12.2026 seçtim, randevu 22'yi seçip açtım | Muayene ekranı açılır | ✅ Ali Erdem, Uzm. Dr. Murat Kaya, 02.12.2026 10:00 bilgisiyle açıldı. Satıra çift tık olayı da koda bağlı. Ben satırı seçip açan fonksiyonu çağırdım, fareyle çift tıklamadım. |
| 12 | Şikâyet boşken Muayeneyi kaydet | Uyarı verir | ✅ "Şikâyet alanı boş bırakılamaz." |
| 13 | Şikâyet yazıp teşhis eklemeden kaydet | "En az bir teşhis" uyarısı | ✅ "Muayeneye en az bir teşhis eklemelisiniz." |
| 14 | Bir teşhis ekledim (E11.9), aynısını tekrar eklemeyi denedim | "Zaten eklendi" uyarısı | ✅ İlki listeye girdi, ikincisinde "Bu teşhis zaten eklendi." çıktı. |
| 15 | İkinci, farklı bir teşhis ekledim (H10.9, açıklama "hafif") | Eklenir | ✅ Listede iki teşhis oldu. |
| 16 | Muayeneyi kaydettim | "Muayene kaydedildi" mesajı çıkar | ✅ Mesaj çıktı, ekranda "Muayene no: 16 (kayıtlı)" yazdı, kaydet düğmesi pasif oldu. |
| 17 | Doktor panelinde randevunun durumuna baktım | tamamlandi olur (trigger) | ✅ Durum tamamlandi, Muayene sütunu "Yapıldı" oldu. |
| 18 | Aynı randevuyu tekrar açtım | Kayıtlı muayene açılır, yeniden kaydedilemez | ✅ Şikâyet ve iki teşhis geldi, şikâyet kutuları kilitli, kaydet düğmesi pasif. |
| 19 | Aynı randevuya veritabanından ikinci muayene eklemeyi denedim | Reddedilir | ✅ "Bu randevu için zaten bir muayene kaydı var." (UNIQUE kuralı). |
| 20 | Reçete yaz düğmesi | Veronika'nın reçete ekranı bu muayene seçili ve kilitli açılır | ✅ Reçete ekranı açıldı, muayene 16 seçili, seçim kutusu pasif. "Bu muayene için henüz reçete yazılmamış." yazıyor. |

## Sonuç

20 denemenin hepsi beklendiği gibi çalıştı, kodda düzeltilmesi gereken hata bulamadım.

## Küçük notlar (hata değil)

- Doktor paneli ve muayene ekranı Murat Kaya'yı "Uzm. Dr. Murat Kaya" olarak gösteriyor (veritabanındaki unvan bu). Test listesinde "Prof. Dr." yazıyordu, doğrusu Uzm. Dr.
- Kayıtlı bir muayenede kaydet düğmesi pasif olduğu için ikinci kayıt ekrandan zaten yapılamıyor. Kural ayrıca veritabanında da var (madde 19).
