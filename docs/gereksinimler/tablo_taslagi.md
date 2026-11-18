# Ortak Tablo Taslağı

Gereksinimleri yazarken herkes aynı tablo ve sütun isimlerini kullansın diye bu listeyi hazırladık. 3. adımda ER diyagramını çizerken gerekirse değiştireceğiz.

İsimler küçük harf, Türkçe karakter yok, kelimeler alt çizgiyle ayrılıyor.

| Tablo | Sütunlar | Sorumlu |
|---|---|---|
| hasta | hasta_id, tc_no, ad, soyad, dogum_tarihi, cinsiyet, telefon, adres | Eray |
| randevu | randevu_id, hasta_id, doktor_id, randevu_tarihi, randevu_saati, durum | Eray |
| bolum | bolum_id, bolum_adi | Sude |
| doktor | doktor_id, bolum_id, ad, soyad, unvan, telefon | Sude |
| muayene | muayene_id, randevu_id, muayene_tarihi, sikayet, notlar | Sude |
| teshis | teshis_kodu, teshis_adi | Sude |
| muayene_teshis | muayene_id, teshis_kodu, aciklama | Sude |
| ilac | ilac_id, ilac_adi, etken_madde, ilac_formu | Veronika |
| recete | recete_id, muayene_id, recete_tarihi, aciklama | Veronika |
| recete_ilac | recete_id, ilac_id, doz, kullanim_sekli, kutu_adedi | Veronika |

## Tablolar arası bağlantılar

- Bir bölümde birden fazla doktor çalışır, her doktor tek bir bölüme bağlıdır. (bolum 1 – N doktor)
- Bir hasta birden fazla randevu alabilir. (hasta 1 – N randevu)
- Bir doktorun birden fazla randevusu olur. (doktor 1 – N randevu)
- Bir randevudan en fazla bir muayene çıkar. (randevu 1 – 1 muayene)
- Bir muayenede birden fazla teşhis konabilir, aynı teşhis de birçok muayenede konabilir. (muayene N – N teshis, muayene_teshis ara tablosu ile)
- Bir muayene sonunda en fazla bir reçete yazılır. (muayene 1 – 1 recete)
- Bir reçetede birden fazla ilaç olabilir, bir ilaç da birçok reçetede yazılabilir. (recete N – N ilac, recete_ilac ara tablosu ile)

## Değişiklik notu (18.11)

İlk taslakta teshis tablosunda teshis_kodu ile teshis_adi birlikte tutuluyordu. ICD-10 kodu teşhisin adını belirlediği için (J06.9 her zaman aynı hastalık) bu, 3NF'yi bozan geçişli bir bağımlılık oluşturuyordu. Bu yüzden teshis tablosunu bir katalog yaptık (teshis_kodu, teshis_adi) ve muayene ile teşhisi muayene_teshis ara tablosuyla bağladık. Böylece tablo sayısı 10 oldu.
