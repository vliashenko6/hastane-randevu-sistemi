# 4a- VI (ER) Diyagramı

Veri gereksinimlerinden yola çıkarak önce sistemde hangi varlıkların olduğunu, bu varlıkların hangi bilgileri tuttuğunu ve birbirleriyle nasıl ilişkili olduğunu belirledik. Bunu Chen gösterimiyle bir ER (Varlık–İlişki) diyagramı olarak draw.io'da çizdik (docs/er_diyagrami.png).

Diyagramda kullanılan şekiller:

- **Dikdörtgen:** varlık (ileride tablo olur)
- **Oval:** nitelik (ileride sütun olur). Altı çizili nitelikler anahtardır.
- **Eşkenar dörtgen:** iki varlık arasındaki ilişki
- **1 ve N:** ilişkinin kardinalitesi, yani bir kaydın karşı tarafta kaç kayıtla eşleşebileceği

## Varlıklar

Sistemde 8 varlık var: **bolum**, **doktor**, **hasta**, **randevu**, **muayene**, **teshis**, **recete** ve **ilac**.

Randevuyu ilişki değil varlık olarak modelledik. Randevunun kendi numarası, tarihi, saati ve durumu var; ayrıca muayene de randevuya bağlanıyor. Kendi bilgileri ve başka ilişkileri olduğu için ayrı bir varlık olması gerekiyordu.

Teşhis varlığı, ICD-10 kodlarından oluşan bir teşhis listesini (katalog) temsil ediyor. Anahtarı teşhis kodu (örn. J06.9).

## İlişkiler

| İlişki | Kardinalite | Açıklama |
|---|---|---|
| bolum – *çalışır* – doktor | 1 – N | Bir bölümde birden fazla doktor çalışır, her doktor tek bir bölümdedir. |
| doktor – *atanır* – randevu | 1 – N | Bir doktorun birden fazla randevusu olur, her randevu tek bir doktora aittir. |
| hasta – *alır* – randevu | 1 – N | Bir hasta birden fazla randevu alabilir, her randevu tek bir hastaya aittir. |
| randevu – *yapılır* – muayene | 1 – 1 | Bir randevudan en fazla bir muayene çıkar. |
| muayene – *yazılır* – recete | 1 – 1 | Bir muayenede en fazla bir reçete yazılır. |
| muayene – *konur* – teshis | N – N | Bir muayenede birden fazla teşhis konabilir, bir teşhis de birçok muayenede konabilir. Doktorun o teşhisle ilgili notu (aciklama) ilişkinin niteliğidir. |
| recete – *içerir* – ilac | N – N | Bir reçetede birden fazla ilaç olabilir, bir ilaç da birçok reçetede yazılabilir. Doz, kullanım şekli ve kutu adedi ilişkinin nitelikleridir. |

Kardinaliteleri belirlerken her ilişkiye iki yönden baktık. Örneğin "bir bölümde kaç doktor olabilir?" sorusunun cevabı "çok", "bir doktor kaç bölümde olabilir?" sorusunun cevabı "bir" olduğu için bolum ile doktor arasındaki ilişki 1 – N oldu.

## Diyagramla ilgili notlar

- ER diyagramında yabancı anahtarlar gösterilmez, varlıklar arasındaki bağlantıyı ilişkiler gösterir. Yabancı anahtarlar ilişkisel şemaya geçerken eklendi (bkz. 4b).
- Doz ve kullanım şekli gibi bilgiler ne sadece reçeteye ne de sadece ilaca aittir; "o reçetedeki o ilaca" aittir. Bu yüzden bu bilgileri içerir ilişkisinin niteliği olarak gösterdik. Aynı şekilde teşhisle ilgili açıklama da konur ilişkisinin niteliğidir.
- İki çoka çok ilişki (içerir ve konur), ilişkisel şemada recete_ilac ve muayene_teshis ara tablolarına dönüşüyor.
