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

Doktorun muayene sonunda koyduğu teşhisler bu tabloda tutulur. Bir muayenede birden fazla teşhis konabileceği için teşhisleri ayrı bir tabloda tutuyoruz.

- Her teşhisin kendine ait bir numarası vardır (teshis_id).
- Her teşhis bir muayeneye bağlıdır (muayene_id). Boş bırakılamaz.
- Teşhisin adı tutulur (teshis_adi), örneğin "Akut üst solunum yolu enfeksiyonu". Boş bırakılamaz.
- Teşhisin ICD-10 kodu tutulur (teshis_kodu), örneğin "J06.9". Boş olabilir.

| Sütun | Açıklama | Kural |
|---|---|---|
| teshis_id | Teşhisin numarası | Birincil anahtar |
| muayene_id | Teşhisin konduğu muayene | Yabancı anahtar (muayene), boş olamaz |
| teshis_kodu | ICD-10 kodu, örn. J06.9 | Boş olabilir |
| teshis_adi | Teşhisin adı | Boş olamaz |

## İlişkiler

- bolum – doktor: Bir bölümde birden fazla doktor çalışır (1 – N).
- doktor – randevu: Bir doktorun birden fazla randevusu olabilir (1 – N).
- randevu – muayene: Bir randevudan en fazla bir muayene çıkar (1 – 1).
- muayene – teshis: Bir muayenede birden fazla teşhis konabilir (1 – N).
- muayene – recete: Bir muayenede en fazla bir reçete yazılır (1 – 1).
- İçinde doktor olan bir bölüm silinemez.
