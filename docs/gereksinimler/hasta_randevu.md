# Veri Gereksinimleri: Hasta ve Randevu

Hazırlayan: Eray

## Hasta (hasta)

Hastanede kaydı bulunan hastaların bilgileri bu tabloda tutulur.

- Her hastanın kendine ait bir numarası vardır (hasta_id). Bu numara her hasta için farklıdır.
- Her hastanın TC kimlik numarası tutulur (tc_no). 11 haneli olmalıdır, boş bırakılamaz ve tekrar edemez. Aynı TC ile ikinci bir hasta kaydedilemez.
- Hastanın adı (ad), soyadı (soyad) ve doğum tarihi (dogum_tarihi) boş bırakılamaz. Doğum tarihi gelecekte bir tarih olamaz.
- Cinsiyet tutulur (cinsiyet). Sadece 'E' veya 'K' girilebilir.
- Hastaya ulaşmak için telefon numarası tutulur (telefon). Boş bırakılamaz.
- Hastanın adresi tutulur (adres). Boş olabilir.

| Sütun | Açıklama | Kural |
|---|---|---|
| hasta_id | Hastanın numarası | Birincil anahtar |
| tc_no | TC kimlik numarası | 11 haneli, boş olamaz, tekrar edemez |
| ad | Hastanın adı | Boş olamaz |
| soyad | Hastanın soyadı | Boş olamaz |
| dogum_tarihi | Doğum tarihi | Boş olamaz, gelecekte bir tarih olamaz |
| cinsiyet | E veya K | Sadece 'E' veya 'K' olabilir |
| telefon | Telefon numarası | Boş olamaz |
| adres | Hastanın adresi | Boş olabilir |

## Randevu (randevu)

Hastaların doktorlardan aldığı randevular bu tabloda tutulur.

- Her randevunun kendine ait bir numarası vardır (randevu_id).
- Her randevu bir hastaya (hasta_id) ve bir doktora (doktor_id) bağlıdır. İkisi de boş bırakılamaz.
- Randevunun tarihi (randevu_tarihi) ve saati (randevu_saati) boş bırakılamaz. Geçmiş bir tarihe randevu verilemez.
- Randevunun durumu tutulur (durum). Sadece 'aktif', 'iptal' veya 'tamamlandi' olabilir. Durum girilmezse 'aktif' yazılır.
- İptal edilen randevu silinmez, durumu 'iptal' olur. Muayene yapılınca durum 'tamamlandi' olur.
- Aynı doktora aynı gün ve aynı saatte iki aktif randevu verilemez. Bu çift randevu engeli projenin en önemli kuralıdır.

| Sütun | Açıklama | Kural |
|---|---|---|
| randevu_id | Randevunun numarası | Birincil anahtar |
| hasta_id | Randevuyu alan hasta | Yabancı anahtar (hasta), boş olamaz |
| doktor_id | Randevu verilen doktor | Yabancı anahtar (doktor), boş olamaz |
| randevu_tarihi | Randevunun günü | Boş olamaz, geçmiş tarih olamaz |
| randevu_saati | Randevunun saati | Boş olamaz |
| durum | Randevunun durumu | 'aktif', 'iptal' veya 'tamamlandi'; varsayılan: 'aktif' |

Çift randevu kuralı: aynı doktor_id, randevu_tarihi ve randevu_saati için en fazla bir aktif randevu olabilir.

## İlişkiler

- hasta – randevu: Bir hasta birden fazla randevu alabilir (1 – N).
- doktor – randevu: Bir doktorun birden fazla randevusu olabilir (1 – N).
- randevu – muayene: Bir randevudan en fazla bir muayene çıkar (1 – 1).
- Randevusu olan bir hasta silinemez.
