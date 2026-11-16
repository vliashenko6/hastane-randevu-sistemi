# Veri Gereksinimleri: İlaç, Reçete ve Reçete–İlaç

Hazırlayan: Veronika

## İlaç (ilac)

Hastanede yazılabilecek ilaçların listesi bu tabloda tutulur.

- Her ilacın kendine ait bir numarası vardır (ilac_id). Bu numara her ilaç için farklıdır.
- Her ilacın bir adı vardır (ilac_adi), örneğin "Parol 500 mg". İlaç adı boş bırakılamaz ve aynı isimle iki ilaç kaydedilemez.
- İlacın etken maddesi tutulur (etken_madde), örneğin "Parasetamol".
- İlacın formu tutulur (ilac_formu): tablet, kapsül, şurup, krem, iğne gibi.

| Sütun | Açıklama | Kural |
|---|---|---|
| ilac_id | İlacın numarası | Birincil anahtar |
| ilac_adi | İlacın ticari adı | Boş olamaz, tekrar edemez |
| etken_madde | İlacın etken maddesi | Boş olamaz |
| ilac_formu | Tablet, şurup vb. | Boş olabilir |

## Reçete (recete)

Doktorun muayene sonunda yazdığı reçete bu tabloda tutulur.

- Her reçetenin kendine ait bir numarası vardır (recete_id).
- Her reçete bir muayeneye bağlıdır (muayene_id). Reçetenin hangi hastaya ve hangi doktor tarafından yazıldığı bu muayene üzerinden bulunur.
- Bir muayene için en fazla bir reçete yazılabilir. Her muayenede reçete yazılmak zorunda değildir.
- Reçetenin yazıldığı tarih tutulur (recete_tarihi). Tarih girilmezse o günün tarihi yazılır.
- Doktor isterse reçeteye kısa bir not ekleyebilir (aciklama), örneğin "Tok karnına alınacak".

| Sütun | Açıklama | Kural |
|---|---|---|
| recete_id | Reçetenin numarası | Birincil anahtar |
| muayene_id | Reçetenin yazıldığı muayene | Yabancı anahtar (muayene), tekrar edemez |
| recete_tarihi | Reçetenin yazıldığı tarih | Boş olamaz, varsayılan: bugün |
| aciklama | Doktorun notu | Boş olabilir |

## Reçete–İlaç (recete_ilac)

Bir reçetede birden fazla ilaç olabilir, bir ilaç da farklı reçetelerde yazılabilir. Yani reçete ile ilaç arasında çoka çok (N–N) ilişki vardır. Bu ilişkiyi recete_ilac ara tablosuyla tutuyoruz. Bu tablodaki her satır "şu reçetede şu ilaç var" anlamına gelir.

- Her satırda reçetenin numarası (recete_id) ve ilacın numarası (ilac_id) bulunur.
- Aynı ilaç aynı reçeteye iki kez eklenemez. Bu yüzden birincil anahtar (recete_id, ilac_id) ikilisidir.
- İlacın dozu tutulur (doz), örneğin "2x1".
- İlacın nasıl kullanılacağı tutulur (kullanim_sekli), örneğin "Sabah ve akşam, tok karnına".
- Kaç kutu verileceği tutulur (kutu_adedi). En az 1 olmalıdır.
- Doz, kullanım şekli ve kutu adedi bu tabloda durur, çünkü bunlar ne sadece reçetenin ne de sadece ilacın bilgisidir; o reçetedeki o ilaca aittir.

| Sütun | Açıklama | Kural |
|---|---|---|
| recete_id | Hangi reçete | Yabancı anahtar (recete), birincil anahtarın parçası |
| ilac_id | Hangi ilaç | Yabancı anahtar (ilac), birincil anahtarın parçası |
| doz | Örn. 2x1 | Boş olamaz |
| kullanim_sekli | Örn. tok karnına | Boş olabilir |
| kutu_adedi | Verilecek kutu sayısı | En az 1, varsayılan 1 |

## İlişkiler

- recete – muayene: Bir muayenede en fazla bir reçete yazılır (1 – 1).
- recete – ilac: Bir reçetede birden fazla ilaç, bir ilaç birden fazla reçetede olabilir (N – N). recete_ilac tablosu bu ilişkiyi iki tane 1 – N ilişkiye böler:
  - recete 1 – N recete_ilac
  - ilac 1 – N recete_ilac
- Bir reçete silinirse o reçeteye ait recete_ilac satırları da silinir. Bir reçetede kullanılmış bir ilaç ise silinemez.
