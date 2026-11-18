# 4c- Normalleştirme

Normalleştirme, tablolardaki gereksiz tekrarları azaltmak ve ekleme, güncelleme, silme sırasında ortaya çıkan hataları (anomalileri) önlemek için tabloları adım adım düzenleme işlemidir. Bu bölümde tablolarımızın 1NF, 2NF ve 3NF kurallarına nasıl uyduğunu bir örnek üzerinden gösteriyoruz.

## Başlangıç: Normalleştirilmemiş Tablo

Hastanede bugün bilgiler kâğıda yazıldığı için, bir randevuyla ilgili her şey tek bir satırda tutuluyor gibi düşünebiliriz. Bunu tek bir büyük tablo olarak yazarsak şöyle olur:

**RANDEVU_KAYDI** (randevu_id, tc_no, hasta_ad, hasta_soyad, hasta_telefon, doktor_ad, doktor_soyad, bolum_adi, randevu_tarihi, randevu_saati, sikayet, teshisler, ilaclar)

| randevu_id | tc_no | hasta_ad | doktor_ad | bolum_adi | randevu_tarihi | teshisler | ilaclar |
|---|---|---|---|---|---|---|---|
| 1 | 12345678901 | Ayşe | Mehmet | Dahiliye | 10.12.2026 | J06.9 Üst solunum yolu enf., R50.9 Ateş | Parol 500 mg (2x1), Augmentin 1 g (2x1) |
| 2 | 12345678901 | Ayşe | Mehmet | Dahiliye | 20.12.2026 | J06.9 Üst solunum yolu enf. | Parol 500 mg (3x1) |

Bu tablodaki sorunlar:

- **Bir hücrede birden fazla değer var:** `teshisler` ve `ilaclar` sütunlarında virgülle ayrılmış birden fazla bilgi bulunuyor. "En çok yazılan ilaç hangisi?" gibi bir soruyu bu hâliyle sorgulamak çok zor.
- **Tekrar:** Ayşe'nin bilgileri ve Dr. Mehmet'in bölümü her randevuda yeniden yazılıyor.
- **Güncelleme anomalisi:** Hastanın telefonu değişirse bütün satırlarını tek tek düzeltmek gerekiyor; biri unutulursa veriler çelişiyor.
- **Ekleme anomalisi:** Hiç randevusu olmayan yeni bir doktor ya da yeni bir ilaç sisteme eklenemiyor.
- **Silme anomalisi:** Bir doktorun tek randevusu silinirse doktorun hangi bölümde çalıştığı bilgisi de kayboluyor.

## Birinci Normal Form (1NF)

Bir tablonun 1NF'de olması için her hücrede tek (atomik) bir değer olmalı, tekrar eden sütun grupları bulunmamalı ve her satır bir birincil anahtarla ayırt edilebilmelidir.

Tabloyu 1NF'ye getirmek için çok değerli `teshisler` ve `ilaclar` sütunlarını ayrı satırlara ayırdık:

- Bir muayenede birden fazla teşhis konabildiği için teşhisleri ayrı bir **teshis** tablosuna taşıdık. Her satır tek bir teşhis tutuyor (teshis_kodu, teshis_adi).
- Bir reçetede birden fazla ilaç olabildiği için her ilaç ayrı bir satırda tutuluyor. Bu satırlar daha sonra **recete_ilac** tablosu oldu.
- Hasta adı ve soyadı tek sütunda değil, `ad` ve `soyad` olarak iki ayrı sütunda tutuluyor.

1NF'den sonra ilaç bilgisi şu şekilde görünür:

**RECETE_SATIRI** (recete_id, ilac_id, ilac_adi, etken_madde, doz, kullanim_sekli, kutu_adedi)

| recete_id | ilac_id | ilac_adi | etken_madde | doz |
|---|---|---|---|---|
| 1 | 3 | Parol 500 mg | Parasetamol | 2x1 |
| 1 | 7 | Augmentin 1 g | Amoksisilin + Klavulanik asit | 2x1 |
| 2 | 3 | Parol 500 mg | Parasetamol | 3x1 |

Artık her hücrede tek değer var, ancak tekrar sorunu tamamen bitmedi: "Parol 500 mg – Parasetamol" bilgisi her reçetede yeniden yazılıyor.

## İkinci Normal Form (2NF)

Bir tablonun 2NF'de olması için önce 1NF'de olması, ayrıca anahtar olmayan her sütunun birincil anahtarın **tamamına** bağlı olması gerekir. Birincil anahtar birden fazla sütundan oluşuyorsa, bir sütunun anahtarın sadece bir parçasına bağlı olmasına **kısmi bağımlılık** denir ve 2NF'de buna izin verilmez.

Yukarıdaki RECETE_SATIRI tablosunun birincil anahtarı (recete_id, ilac_id) ikilisidir. Bağımlılıklara bakınca:

- `doz`, `kullanim_sekli`, `kutu_adedi` → (recete_id, ilac_id). Bunlar "o reçetedeki o ilaca" ait bilgilerdir, yani anahtarın tamamına bağlıdır. ✅
- `ilac_adi`, `etken_madde` → sadece `ilac_id`. Bu bilgiler hangi reçetede yazıldığından bağımsızdır. ❌ Bu bir kısmi bağımlılıktır.

Bu yüzden tabloyu ikiye böldük:

- **ilac** (ilac_id, ilac_adi, etken_madde, ilac_formu)
- **recete_ilac** (recete_id, ilac_id, doz, kullanim_sekli, kutu_adedi)

Böylece bir ilacın adı ya da etken maddesi tek bir yerde tutuluyor. İlaç bilgisi değişirse sadece ilac tablosunda bir satır güncelleniyor. Reçete ile ilaç arasındaki çoka çok (N–N) ilişki de recete_ilac ara tablosuyla kurulmuş oluyor.

Projedeki diğer tablolarda birincil anahtar tek sütundan (hasta_id, doktor_id, randevu_id vb.) oluştuğu için kısmi bağımlılık oluşamaz. Bu tablolar 1NF'de oldukları için doğrudan 2NF'dedir.

## Üçüncü Normal Form (3NF)

Bir tablonun 3NF'de olması için önce 2NF'de olması, ayrıca anahtar olmayan hiçbir sütunun başka bir anahtar olmayan sütuna bağlı olmaması gerekir. A → B ve B → C ise C, A'ya B üzerinden dolaylı olarak bağlıdır. Buna **geçişli bağımlılık** denir.

Örnek olarak doktor bilgisini başlangıçtaki gibi bölüm adıyla birlikte tutsaydık:

**DOKTOR** (doktor_id, ad, soyad, unvan, telefon, bolum_id, bolum_adi)

| doktor_id | ad | soyad | bolum_id | bolum_adi |
|---|---|---|---|---|
| 1 | Mehmet | Kaya | 2 | Dahiliye |
| 2 | Zeynep | Arslan | 2 | Dahiliye |
| 3 | Ali | Demir | 1 | Kardiyoloji |

Burada `doktor_id → bolum_id` ve `bolum_id → bolum_adi` bağımlılıkları var. Yani `bolum_adi`, doktora doğrudan değil bölüm üzerinden bağlı. Bu geçişli bağımlılık yüzünden "Dahiliye" her doktor için tekrar yazılıyor. Bölümün adı değişirse bütün doktor satırları güncellenmek zorunda kalıyor, bölümde hiç doktor yoksa da bölüm sisteme eklenemiyor.

Bu yüzden bölüm bilgisini ayrı bir tabloya taşıdık:

- **bolum** (bolum_id, bolum_adi)
- **doktor** (doktor_id, bolum_id, ad, soyad, unvan, telefon)

Aynı mantıkla:

- Randevu tablosunda hastanın adı, soyadı ve telefonu tutulmuyor; sadece `hasta_id` tutuluyor. Hasta bilgileri **hasta** tablosunda.
- Randevu tablosunda bölüm adı tutulmuyor. Randevunun hangi bölüme ait olduğu `doktor_id` üzerinden doktor ve bölüm tablolarından bulunuyor.
- Reçete tablosunda hasta ve doktor bilgisi tutulmuyor. Reçetenin kime ve kim tarafından yazıldığı `muayene_id → randevu_id → hasta_id, doktor_id` yoluyla bulunuyor.
- Muayenede konulan teşhisler muayene tablosunda değil, **teshis** tablosunda `muayene_id` ile tutuluyor.

**Teşhis tablosu hakkında not:** teshis tablosunda `teshis_kodu` (örn. J06.9) ve `teshis_adi` birlikte tutuluyor. Teşhis kodu zorunlu değil ve teşhis adını doktor muayenede kendisi yazıyor. Yani aynı kod için farklı doktorlar farklı ifadeler yazabiliyor; kod, adı tek başına belirlemiyor. Bu yüzden `teshis_kodu → teshis_adi` diye bir bağımlılık kabul etmedik ve tablo 3NF'de kalıyor. Teşhisler ileride sabit bir ICD-10 listesinden seçilecek olursa, kod ve ad ayrı bir katalog tablosuna taşınmalıdır.

## Sonuç

Normalleştirme sonunda tek büyük tablo dokuz tabloya ayrıldı. Her tablonun birincil anahtarı ve bağımlılıkları aşağıda özetlenmiştir:

| Tablo | Birincil anahtar | Bağımlılık | Normal form |
|---|---|---|---|
| hasta | hasta_id | hasta_id → tc_no, ad, soyad, dogum_tarihi, cinsiyet, telefon, adres | 3NF |
| bolum | bolum_id | bolum_id → bolum_adi | 3NF |
| doktor | doktor_id | doktor_id → bolum_id, ad, soyad, unvan, telefon | 3NF |
| randevu | randevu_id | randevu_id → hasta_id, doktor_id, randevu_tarihi, randevu_saati, durum | 3NF |
| muayene | muayene_id | muayene_id → randevu_id, muayene_tarihi, sikayet, notlar | 3NF |
| teshis | teshis_id | teshis_id → muayene_id, teshis_kodu, teshis_adi | 3NF |
| ilac | ilac_id | ilac_id → ilac_adi, etken_madde, ilac_formu | 3NF |
| recete | recete_id | recete_id → muayene_id, recete_tarihi, aciklama | 3NF |
| recete_ilac | (recete_id, ilac_id) | (recete_id, ilac_id) → doz, kullanim_sekli, kutu_adedi | 3NF |

`hasta` tablosunda `tc_no`, `bolum` tablosunda `bolum_adi`, `ilac` tablosunda `ilac_adi`, `muayene` ve `recete` tablosunda ise `randevu_id` ve `muayene_id` da tekrar edemez. Bunlar aday anahtardır. Hepsi kendi satırını tek başına belirlediği için 3NF kuralını bozmaz.

Sonuç olarak tüm tablolarımız 3NF'dedir. Her bilgi tek bir yerde tutulduğu için tekrar azaldı. Bir hasta, doktor, bölüm ya da ilaç bilgisi değiştiğinde yalnızca bir satır güncelleniyor. Henüz randevusu olmayan bir doktor veya hiç yazılmamış bir ilaç da sisteme eklenebiliyor.
