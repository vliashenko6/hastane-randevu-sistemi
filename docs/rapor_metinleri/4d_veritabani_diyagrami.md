# 4d- Veritabanı Diyagramı

ER diyagramı kavramsal bir modeldi; veritabanı diyagramı ise tabloları PostgreSQL'de oluşturduktan sonraki gerçek hâli gösteriyor. Diyagramı `sql/00_kurulum.sql` ile kurulan hastane_randevu veritabanındaki tablolara göre hazırladık (docs/tasarim/veritabani_diyagrami.png).

ER diyagramından farklı olarak bu diyagramda:

- Her kutu bir **tablo**, kutudaki her satır bir **sütun**dur. Sütunun yanında PostgreSQL'deki veri tipi yazar (integer, varchar(50), date, time vb.).
- **PK** birincil anahtarı, **FK** yabancı anahtarı, **U** tekrar edemeyen (UNIQUE) sütunu gösterir.
- Yabancı anahtarlar artık görünür. Tablolar arasındaki çizgiler bir yabancı anahtardan bağlandığı birincil anahtara gider.
- Çizgi uçlarında tek çizgi "1", karga ayağı "N (çok)" anlamına gelir.

## Diyagramda görülenler

- Veritabanında 10 tablo var: 8 tablo varlıklardan, 2 tablo (muayene_teshis ve recete_ilac) çoka çok ilişkilerden geldi.
- **1 – N ilişkiler:** bolum – doktor, hasta – randevu, doktor – randevu, muayene – muayene_teshis, teshis – muayene_teshis, recete – recete_ilac, ilac – recete_ilac.
- **1 – 1 ilişkiler:** randevu – muayene ve muayene – recete. Bunlar muayene.randevu_id ve recete.muayene_id sütunlarındaki UNIQUE kısıtıyla sağlanıyor; böylece bir randevuya en fazla bir muayene, bir muayeneye en fazla bir reçete bağlanabiliyor.
- **Çoka çok ilişkiler:** muayene – teshis ve recete – ilac ilişkileri doğrudan çizilmiyor. Her biri ara tablo üzerinden iki tane 1 – N ilişkiye bölünmüş durumda. Ara tablolarda iki sütun hem birincil anahtarın parçası hem de yabancı anahtar olduğu için **PK FK** olarak işaretli.
- teshis tablosunun birincil anahtarı bir sayı değil, ICD-10 kodu (teshis_kodu, örn. J06.9). Bu yüzden muayene_teshis tablosundaki teshis_kodu sütunu da varchar(10) tipinde.

## Notlar

- Diyagram, 4b'deki ilişkisel şemayla birebir aynı tabloları, sütunları ve anahtarları gösteriyor. Bu da tasarımın veritabanına doğru aktarıldığını gösteriyor.
- Kurulumla birlikte oluşan recete_detay görünümü (VIEW) gerçek bir tablo olmadığı için diyagramda yer almıyor.
