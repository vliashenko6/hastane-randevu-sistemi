# 8b- Uygulama Kullanıcı Arayüzleri: Bölümler ve Doktorlar, Doktor Paneli, Muayene

Hazırlayan: Sude

Ekran görüntüleri `docs/ekran_goruntuleri/` klasöründe. Üç ekran da ana menüden açılır.

## Bölümler ve Doktorlar (sude_bolum_doktor.png)

Ana menüdeki "Bölümler ve Doktorlar" düğmesiyle açılır.

- Solda hastanedeki bütün bölümler, her bölümde çalışan doktor sayısıyla birlikte listelenir (FG-10).
- Bir bölüm seçilince sağ tarafta o bölümde çalışan doktorlar unvan, ad soyad ve telefon bilgisiyle gelir (FG-11). Görüntüde Kardiyoloji seçilmiş.
- Telefonu girilmemiş doktorlarda telefon yerine "-" yazar.

## Doktor Paneli (sude_doktor_paneli.png)

Doktorun bir gündeki randevularını gördüğü ekran (FG-12).

- Doktor listeden seçilir; listede doktorun unvanı ve bölümü de yazar. Tarih, hasta ve randevu ekranlarındaki gibi GG.AA.YYYY biçiminde girilir (YYYY-AA-GG de kabul edilir); açılışta bugünün tarihi yazılıdır.
- "Listele" düğmesine basınca o günkü randevular saat sırasıyla gelir. İptal edilen randevular listede gösterilmez.
- Her randevuda hastanın adı, TC kimlik numarası, randevu durumu ve muayenenin yapılıp yapılmadığı görünür. Görüntüde Prof. Dr. Hakan Aydın'ın 3 Kasım 2026'daki iki randevusu var, ikisinin de muayenesi yapılmış.
- Tarih yanlış biçimde yazılırsa uyarı verilir (FG-27).
- Bir randevu seçilip "Muayene" düğmesine basılınca (ya da satıra çift tıklanınca) muayene ekranı açılır. Muayene ekranı kapanınca liste yenilenir.

## Muayene Ekranı

Doktor panelinde seçilen randevu için açılır. Üstte hasta, doktor, randevu tarihi ve saati yazar.

### Yeni muayene (sude_muayene_yeni.png)

- Doktor hastanın şikâyetini ve isterse notlarını yazar (FG-13).
- Teşhis, ICD-10 teşhis listesinden kodu ve adıyla seçilir. İstenirse o teşhisle ilgili kısa bir açıklama yazılır ve "Ekle" ile listeye eklenir. Bir muayeneye birden fazla teşhis eklenebilir; aynı teşhis ikinci kez eklenemez (FG-15). Görüntüde iki teşhis eklenmiş: I10 ve R00.2.
- "Muayeneyi kaydet" ile muayene ve teşhisler kaydedilir. Şikâyet boşsa ya da hiç teşhis eklenmemişse kayıt yapılmaz ve uyarı verilir (FG-27). Her muayeneye en az bir teşhis girilmesi kuralını uygulama kontrol ediyor.
- Muayene kaydedilince randevunun durumu veritabanındaki trigger sayesinde otomatik olarak "tamamlandi" olur (FG-14).
- İptal edilmiş bir randevuya muayene girilemez, kaydet düğmesi kapalı gelir.

### Kayıtlı muayene (sude_muayene_kayitli.png)

- Muayenesi yapılmış bir randevu açılınca şikâyet ve notlar gösterilir ama değiştirilemez; "Muayeneyi kaydet" düğmesi kapalıdır. Bir randevu için ikinci muayene açılamaz (FG-13).
- Muayenenin teşhisleri `muayene_teshis` tablosundan okunup listelenir. Kayıtlı muayeneye sonradan teşhis eklenebilir; aynı teşhis tekrar eklenmeye çalışılırsa "Bu teşhis bu muayeneye zaten eklenmiş." mesajı çıkar.
- "Reçete yaz" düğmesi reçete ekranını bu muayene seçili olarak açar (FG-17). Görüntüde 1 numaralı muayene var: üç teşhis konmuş (I20.9, R00.2, R07.4).
