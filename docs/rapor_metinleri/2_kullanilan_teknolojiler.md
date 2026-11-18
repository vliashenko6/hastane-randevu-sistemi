# 2- Kullanılan Teknolojiler

**PostgreSQL 18.** PostgreSQL, açık kaynaklı bir ilişkisel veritabanı yönetim sistemidir. Projede hasta, doktor, randevu, muayene gibi tüm verileri tek bir veritabanında tutmak için kullandık. Birincil anahtar, yabancı anahtar, UNIQUE ve CHECK gibi kısıtlamalar sayesinde çift randevu gibi hataları veritabanı seviyesinde engelleyebiliyoruz.

**pgAdmin 4.** pgAdmin, PostgreSQL'i görsel olarak yönetmeye yarayan bir araçtır. Tabloları oluştururken, sorguları denerken ve verileri kontrol ederken kullandık. Komut satırına göre daha rahat olduğu için ekip olarak tercih ettik.

**Python 3.** Python, uygulamanın yazıldığı programlama dilidir. Öğrenmesi kolay olduğu ve veritabanı ile arayüz kütüphaneleri için iyi destek verdiği için seçtik. Uygulamanın tüm mantığı Python ile yazıldı.

**psycopg2.** psycopg2, Python ile PostgreSQL arasında bağlantı kuran bir kütüphanedir. Uygulamadan veritabanına sorgu göndermek, kayıt eklemek, silmek ve sonuçları almak için kullandık. Bağlantı testini de bu kütüphane ile yaptık.

**Tkinter.** Tkinter, Python ile birlikte gelen masaüstü arayüz kütüphanesidir. Ayrıca bir şey kurmak gerekmediği için kullanımı kolaydır. Randevu alma, hasta ve doktor ekranlarını Tkinter ile yapıyoruz.

**draw.io.** draw.io, ücretsiz bir diyagram çizim aracıdır. ER diyagramını ve UML şemalarını bununla çizdik. Tarayıcıdan çalıştığı ve ekipçe kolay paylaşıldığı için seçtik.

**Git ve GitHub.** Git sürüm takibi için, GitHub ise bu dosyaları internette ortak tutmak için kullanılır. Üç kişi aynı projede çalıştığımız için herkes kendi hesabıyla değişiklik yapıyor ve eski sürümlere geri dönebiliyoruz. Kod, rapor ve belgeler bu repoda duruyor.
