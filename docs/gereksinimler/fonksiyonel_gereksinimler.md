# Fonksiyonel Gereksinimler

Hazırlayan: Veronika (Eray ve Sude'nin modülleriyle birlikte)

Sistemi üç tür kullanıcı kullanır:

- **Danışma görevlisi:** Hasta kaydını yapar, randevu verir ve iptal eder.
- **Doktor:** Kendi randevularını görür, muayene ve teşhis girer, reçete yazar.
- **Hastane yöneticisi:** İstatistikleri görüntüler (FG-23, FG-24, FG-25).

## Hasta işlemleri (Eray)

- FG-01: Görevli yeni bir hastayı TC kimlik no, ad, soyad, doğum tarihi, cinsiyet, telefon ve adres bilgileriyle kaydedebilmelidir.
- FG-02: Aynı TC kimlik no ile ikinci bir hasta kaydedilememelidir.
- FG-03: Görevli hastayı TC kimlik no veya ad–soyad ile arayabilmelidir.
- FG-04: Görevli hastanın telefon ve adres bilgisini güncelleyebilmelidir.

## Randevu işlemleri (Eray)

- FG-05: Görevli önce bölümü, sonra o bölümdeki doktoru seçerek hastaya randevu verebilmelidir.
- FG-06: Aynı doktora, aynı gün ve aynı saatte ikinci bir randevu verilememelidir.
- FG-07: Geçmiş bir tarihe randevu verilememelidir.
- FG-08: Görevli bir randevuyu iptal edebilmelidir. İptal edilen randevu silinmez, durumu "iptal" olur.
- FG-09: Bir hastanın tüm randevuları (geçmiş ve gelecek) listelenebilmelidir.

## Bölüm ve doktor işlemleri (Sude)

- FG-10: Hastanedeki bölümler listelenebilmelidir.
- FG-11: Seçilen bölümde çalışan doktorlar listelenebilmelidir.

## Doktor paneli ve muayene (Sude)

- FG-12: Doktor, seçtiği gündeki randevularını saat sırasıyla görebilmelidir.
- FG-13: Doktor bir randevu için muayene kaydı (şikâyet, notlar) girebilmelidir. Bir randevu için sadece bir muayene açılabilmelidir.
- FG-14: Muayene kaydedilince randevunun durumu "tamamlandı" olmalıdır.
- FG-15: Doktor bir muayeneye, teşhis listesinden (ICD-10 kodu ve adıyla) seçerek bir veya birden fazla teşhis ekleyebilmelidir. Aynı teşhis aynı muayeneye iki kez eklenememelidir.
- FG-16: Bir hastanın geçmiş muayeneleri ve teşhisleri görüntülenebilmelidir.

## Reçete ve ilaç (Veronika)

- FG-17: Doktor muayene sonunda reçete yazabilmelidir. Bir muayene için en fazla bir reçete yazılabilmelidir.
- FG-18: Doktor reçeteye listeden ilaç seçerek, doz, kullanım şekli ve kutu adedi girerek birden fazla ilaç ekleyebilmelidir.
- FG-19: Aynı ilaç aynı reçeteye iki kez eklenememelidir.
- FG-20: Bir reçetenin içindeki ilaçlar listelenebilmelidir.
- FG-21: Bir hastaya geçmişte yazılmış tüm reçeteler görüntülenebilmelidir.

## Ana menü ve istatistikler (Veronika)

- FG-22: Uygulama açıldığında tüm ekranlara geçilebilen bir ana menü görünmelidir.
- FG-23: En çok yazılan ilaçlar listelenebilmelidir.
- FG-24: Bölümlere göre hasta sayısı görüntülenebilmelidir.
- FG-25: Doktor başına yapılan muayene sayısı görüntülenebilmelidir.

## Genel

- FG-26: Uygulama veritabanına bağlanamazsa kullanıcıya anlaşılır bir hata mesajı göstermelidir.
- FG-27: Zorunlu bir alan boş bırakıldığında kayıt yapılmamalı ve kullanıcı uyarılmalıdır.
