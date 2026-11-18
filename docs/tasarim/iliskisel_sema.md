# İlişkisel Şema

Hazırlayan: Eray

Bu bölümde ER diyagramını ilişkisel şemaya çevirdik. ER diyagramında 8 varlık ve 7 ilişki var. Yabancı anahtarlar ER diyagramında görünmez, onları bu adımda ekledik.

## Dönüştürme Kuralları

1. **Varlık kuralı:** Her varlık bir tablo olur, nitelikleri tablonun sütunları olur. Anahtar nitelik tablonun birincil anahtarı olur.
2. **1 – N kuralı:** "1" tarafın birincil anahtarı, "N" tarafındaki tabloya yabancı anahtar olarak eklenir.
3. **1 – 1 kuralı:** Bir tarafın birincil anahtarı diğer tabloya yabancı anahtar olarak eklenir ve bu sütun UNIQUE yapılır. Böylece bir kayda en fazla bir kayıt bağlanabilir.
4. **N – N kuralı:** İlişki ayrı bir tablo olur. Bu tabloya iki tarafın birincil anahtarları yabancı anahtar olarak konur ve ikisi birlikte birincil anahtarı oluşturur. İlişkinin nitelikleri de bu tabloya eklenir.

## Kuralların Projede Uygulanışı

**Varlık kuralı**
- bolum, doktor, randevu, hasta, ilac, recete, muayene ve teshis varlıklarının her biri bir tablo oldu.
- teshis tablosunun birincil anahtarı teshis_kodu (ICD-10 kodu) oldu.

**1 – N kuralı**
- bolum 1 – N doktor: doktor tablosuna bolum_id eklendi.
- hasta 1 – N randevu: randevu tablosuna hasta_id eklendi.
- doktor 1 – N randevu: randevu tablosuna doktor_id eklendi.

**1 – 1 kuralı**
- randevu 1 – 1 muayene: muayene tablosuna randevu_id eklendi ve UNIQUE yapıldı.
- muayene 1 – 1 recete: recete tablosuna muayene_id eklendi ve UNIQUE yapıldı.

**N – N kuralı**
- recete N – N ilac ("içerir"): recete_ilac ara tablosu oluştu. Birincil anahtarı (recete_id, ilac_id) ikilisidir. İlişkinin nitelikleri olan doz, kullanim_sekli ve kutu_adedi bu tabloya eklendi.
- muayene N – N teshis ("konur"): muayene_teshis ara tablosu oluştu. Birincil anahtarı (muayene_id, teshis_kodu) ikilisidir. İlişkinin niteliği olan aciklama bu tabloya eklendi.

## Sonuç Şema

Sonuçta 10 tablo çıktı: 8 tablo varlıklardan, 2 tablo N – N ilişkilerinden geldi. Birincil anahtarlar **kalın**, yabancı anahtarlar *italik* yazıldı.

1. bolum(**bolum_id**, bolum_adi)
2. doktor(**doktor_id**, *bolum_id*, ad, soyad, unvan, telefon)
   - bolum_id → bolum
3. hasta(**hasta_id**, tc_no, ad, soyad, dogum_tarihi, cinsiyet, telefon, adres)
4. randevu(**randevu_id**, *hasta_id*, *doktor_id*, randevu_tarihi, randevu_saati, durum)
   - hasta_id → hasta
   - doktor_id → doktor
5. muayene(**muayene_id**, *randevu_id*, muayene_tarihi, sikayet, notlar)
   - randevu_id → randevu (UNIQUE)
6. teshis(**teshis_kodu**, teshis_adi)
7. muayene_teshis(***muayene_id***, ***teshis_kodu***, aciklama)
   - muayene_id → muayene
   - teshis_kodu → teshis
   - birincil anahtar: (muayene_id, teshis_kodu)
8. ilac(**ilac_id**, ilac_adi, etken_madde, ilac_formu)
9. recete(**recete_id**, *muayene_id*, recete_tarihi, aciklama)
   - muayene_id → muayene (UNIQUE)
10. recete_ilac(***recete_id***, ***ilac_id***, doz, kullanim_sekli, kutu_adedi)
    - recete_id → recete
    - ilac_id → ilac
    - birincil anahtar: (recete_id, ilac_id)

## Ek Kısıtlar

- hasta.tc_no UNIQUE olmalı. Aynı TC ile ikinci hasta kaydedilemez.
- Aynı doktora aynı tarih ve saatte iki aktif randevu olamaz. Yani aktif randevularda (doktor_id, randevu_tarihi, randevu_saati) üçlüsü tekrar edemez.
- randevu.durum sadece 'aktif', 'iptal' ya da 'tamamlandi' olabilir.
- recete_ilac.kutu_adedi en az 1 olmalı.
