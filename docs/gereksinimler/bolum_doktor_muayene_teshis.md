# Veri Gereksinimleri: Bölüm, Doktor, Muayene ve Teşhis

Hazırlayan: Sude

## Bölüm (bolum)

Hastanedeki polikliniklerin (bölümlerin) listesi bu tabloda tutulur.

- Her bölümün kendine ait bir numarası vardır (bolum_id). Bu numara her bölüm için farklıdır.
- Her bölümün bir adı vardır (bolum_adi), örneğin "Kardiyoloji", "Dahiliye", "Ortopedi", "Göz Hastalıkları". Bölüm adı boş bırakılamaz ve aynı isimle iki bölüm kaydedilemez.

| Sütun | Açıklama | Kural |
|---|---|---|
| bolum_id | Bölümün numarası | Birincil anahtar |
| bolum_adi | Bölümün adı | Boş olamaz, tekrar edemez |

## Doktor (doktor)

Hastanede çalışan doktorların bilgileri bu tabloda tutulur.

- Her doktorun kendine ait bir numarası vardır (doktor_id).
- Her doktor tek bir bölüme bağlıdır (bolum_id). Bölüm bilgisi boş bırakılamaz.
- Doktorun adı (ad) ve soyadı (soyad) boş bırakılamaz.
- Doktorun unvanı tutulur (unvan), örneğin "Uzm. Dr.", "Doç. Dr.", "Prof. Dr.".
- Doktorun telefon numarası tutulur (telefon). Boş olabilir.

| Sütun | Açıklama | Kural |
|---|---|---|
| doktor_id | Doktorun numarası | Birincil anahtar |
| bolum_id | Doktorun çalıştığı bölüm | Yabancı anahtar (bolum), boş olamaz |
| ad | Doktorun adı | Boş olamaz |
| soyad | Doktorun soyadı | Boş olamaz |
| unvan | Uzm. Dr., Prof. Dr. vb. | Boş olabilir |
| telefon | Doktorun telefonu | Boş olabilir |

## Muayene (muayene)

Randevusuna gelen hastanın doktor tarafından muayene edilmesi bu tabloda kaydedilir.

- Her muayenenin kendine ait bir numarası vardır (muayene_id).
- Her muayene bir randevuya bağlıdır (randevu_id). Boş bırakılamaz. Bir randevudan en fazla bir muayene çıkar, bu yüzden aynı randevu için ikinci bir muayene kaydedilemez.
- Muayenenin tarihi tutulur (muayene_tarihi). Boş bırakılamaz, girilmezse o günün tarihi yazılır.
- Hastanın şikayeti tutulur (sikayet). Boş bırakılamaz.
- Doktor isterse muayene notu ekleyebilir (notlar). Boş olabilir.
- Muayene kaydedilince ilgili randevunun durumu 'tamamlandi' olur.

| Sütun | Açıklama | Kural |
|---|---|---|
| muayene_id | Muayenenin numarası | Birincil anahtar |
| randevu_id | Muayenenin yapıldığı randevu | Yabancı anahtar (randevu), boş olamaz, tekrar edemez |
| muayene_tarihi | Muayenenin tarihi | Boş olamaz, varsayılan: bugün |
| sikayet | Hastanın şikayeti | Boş olamaz |
| notlar | Doktorun notları | Boş olabilir |

## Teşhis (teshis)

Doktorların koyabileceği teşhislerin listesi bu tabloda tutulur. Bu tablo bir katalogdur, yani ICD-10 teşhis listesini tutar. Muayeneye bağlı değildir; hangi muayenede hangi teşhisin konduğu muayene_teshis tablosunda tutulur.

- Her teşhisin bir ICD-10 kodu vardır (teshis_kodu), örneğin "J06.9". Bu kod her teşhis için farklıdır ve teşhisi ayırt etmek için kullanılır.
- Her teşhisin bir adı vardır (teshis_adi), örneğin "Akut üst solunum yolu enfeksiyonu". Boş bırakılamaz.
- Bir teşhisin adı sadece bu tabloda yazılır. Böylece aynı teşhis her muayenede tekrar tekrar yazılmaz.

| Sütun | Açıklama | Kural |
|---|---|---|
| teshis_kodu | ICD-10 kodu, örn. J06.9 | Birincil anahtar |
| teshis_adi | Teşhisin adı | Boş olamaz |

## Muayene–Teşhis (muayene_teshis)

Bir muayenede birden fazla teşhis konabilir, aynı teşhis de birçok farklı muayenede konabilir. Yani muayene ile teşhis arasında çoka çok (N–N) ilişki vardır. Bu ilişkiyi muayene_teshis ara tablosuyla tutuyoruz. Bu tablodaki her satır "şu muayenede şu teşhis kondu" anlamına gelir.

- Her satırda muayenenin numarası (muayene_id) ve teşhisin kodu (teshis_kodu) bulunur. İkisi de boş bırakılamaz.
- Aynı teşhis aynı muayeneye iki kez eklenemez. Bu yüzden birincil anahtar (muayene_id, teshis_kodu) ikilisidir.
- Doktor isterse o teşhisle ilgili kısa bir not ekleyebilir (aciklama), örneğin "Hafif seyirli". Boş olabilir.
- Açıklama bu tabloda durur, çünkü ne sadece muayenenin ne de sadece teşhisin bilgisidir; o muayenede konan o teşhise aittir.

| Sütun | Açıklama | Kural |
|---|---|---|
| muayene_id | Hangi muayene | Yabancı anahtar (muayene), birincil anahtarın parçası |
| teshis_kodu | Hangi teşhis | Yabancı anahtar (teshis), birincil anahtarın parçası |
| aciklama | Doktorun o teşhisle ilgili notu | Boş olabilir |

## İlişkiler

- bolum – doktor: Bir bölümde birden fazla doktor çalışır (1 – N).
- doktor – randevu: Bir doktorun birden fazla randevusu olabilir (1 – N).
- randevu – muayene: Bir randevudan en fazla bir muayene çıkar (1 – 1).
- muayene – teshis: N – N (muayene_teshis ara tablosu ile).
- muayene – recete: Bir muayenede en fazla bir reçete yazılır (1 – 1).
- İçinde doktor olan bir bölüm silinemez.
