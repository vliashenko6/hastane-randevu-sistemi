# 7a- UML Kullanım Durumu Şeması

Kullanım durumu (use case) şeması, sistemi kimlerin kullandığını ve her kullanıcının sistemde neler yapabildiğini gösterir. Şemayı fonksiyonel gereksinimlerden (FG-01 – FG-27) yola çıkarak draw.io'da çizdik (docs/tasarim/uml_kullanim_durumu.png).

Şemada kullanılan şekiller:

- **Çöp adam:** aktör, yani sistemi kullanan kişi
- **Büyük dikdörtgen:** sistemin sınırı. İçindeki her şey bizim uygulamamızın yaptığı işlerdir.
- **Oval:** kullanım durumu, yani aktörün sistemde yaptığı bir iş
- **Düz çizgi:** aktör ile kullanım durumu arasındaki bağlantı
- **Kesikli ok «include»:** bir iş yapılırken diğer iş de her zaman yapılır.
- **Kesikli ok «extend»:** bir iş, başka bir işe bazen (isteğe bağlı) eklenir.

## Aktörler

Sistemde üç aktör var:

- **Danışma Görevlisi:** Hasta kaydını yapar, randevu verir ve iptal eder.
- **Doktor:** Kendi randevularını görür, muayene ve teşhis girer, reçete yazar.
- **Hastane Yöneticisi:** İstatistikleri görüntüler.

Hasta sistemi doğrudan kullanmadığı için aktör olarak çizilmedi. Hasta randevusunu telefonla ya da danışmaya gelerek alıyor, sisteme bilgileri görevli giriyor.

## Kullanım Durumları

| Aktör | Kullanım durumu | Gereksinim |
|---|---|---|
| Danışma Görevlisi | Hasta kaydet | FG-01, FG-02 |
| Danışma Görevlisi | Hasta ara | FG-03 |
| Danışma Görevlisi | Hasta bilgilerini güncelle | FG-04 |
| Danışma Görevlisi | Randevu ver | FG-05, FG-06, FG-07 |
| Danışma Görevlisi | Randevu iptal et | FG-08 |
| Danışma Görevlisi | Randevu geçmişini görüntüle | FG-09 |
| (Randevu ver içinde) | Bölüm ve doktorları listele | FG-10, FG-11 |
| Doktor | Günlük randevuları görüntüle | FG-12 |
| Doktor | Muayene kaydı gir | FG-13, FG-14 |
| (Muayene kaydı gir içinde) | Teşhis ekle | FG-15 |
| Doktor | Reçete yaz | FG-17, FG-18, FG-19 |
| Doktor | Hasta geçmişini görüntüle | FG-16, FG-20, FG-21 |
| Hastane Yöneticisi | İstatistikleri görüntüle | FG-23, FG-24, FG-25 |

## İlişkiler

- **Randevu ver «include» Bölüm ve doktorları listele:** Görevli randevu verirken önce bölümü, sonra o bölümdeki doktoru seçmek zorunda (FG-05). Yani randevu verme işi her seferinde bölüm ve doktor listelemeyi de içeriyor.
- **Muayene kaydı gir «include» Teşhis ekle:** Doktor muayene kaydı girerken muayeneye en az bir teşhis ekliyor. Teşhisler muayene_teshis ara tablosuna kaydediliyor, bir muayeneye birden fazla teşhis eklenebiliyor.
- **Reçete yaz «extend» Muayene kaydı gir:** Her muayenede reçete yazılmıyor. Doktor gerek görürse muayeneye reçete ekliyor. Bu yüzden ilişki «include» değil «extend» oldu. Bu durum veritabanında da muayene ile reçete arasındaki 1 – 1 ilişkiyle uyumlu: bir muayenede en fazla bir reçete olabilir ama reçete zorunlu değil.

Ana menü (FG-22) ve hata mesajları (FG-26, FG-27) bütün ekranlarda ortak olduğu ve kullanıcının yaptığı ayrı bir iş olmadığı için şemaya ayrı kullanım durumu olarak eklenmedi.
