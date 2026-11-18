# i. Özet

Hazırlayan: Veronika

Bu projede, hayali müşterimiz Doğuş Özel Hastanesi için bir hastane randevu sistemi tasarladık ve geliştirdik. Hastanede randevuların telefonla alınıp kâğıda yazılması; aynı doktora aynı saatte iki randevu verilmesine, hastanın eski muayene ve teşhislerine ulaşılamamasına, reçetelerin takip edilememesine ve istatistik çıkarılamamasına yol açıyordu.

Önce veri ve fonksiyonel gereksinimleri belirledik. Veri gereksinimlerinden yola çıkarak 8 varlık ve 7 ilişkiden oluşan ER diyagramını çizdik, bunu dönüştürme kurallarıyla ilişkisel şemaya çevirdik ve tabloları 3NF'ye kadar normalleştirdik. Normalleştirme sırasında teşhis kodu ile teşhis adı arasındaki geçişli bağımlılığı fark ederek teşhisleri ayrı bir katalog tablosuna aldık. Sonuçta reçete–ilaç ve muayene–teşhis olmak üzere iki çoka çok ilişki içeren 10 tablolu bir veritabanı ortaya çıktı.

Veritabanını PostgreSQL 18 üzerinde oluşturduk. Birincil ve yabancı anahtarlar, UNIQUE ve CHECK kısıtları, çift randevuyu engelleyen kısmi benzersiz indeks, muayene kaydedilince randevuyu tamamlayan bir trigger ve reçete bilgilerini birleştiren bir görünüm (VIEW) kullandık. Örnek verilerle birlikte JOIN, GROUP BY, HAVING, alt sorgu ve VIEW içeren 16 sorgu yazdık.

Uygulamayı Python ile yazdık; veritabanına psycopg2 ile bağlanan, Tkinter arayüzlü ve 6 ekrandan oluşan bir masaüstü uygulaması geliştirdik. Danışma görevlisi hasta kaydı yapıp randevu verebiliyor, doktor günlük randevularını görüp muayene, teşhis ve reçete girebiliyor, hastane yöneticisi de istatistikleri görüntüleyebiliyor. Proje GitHub üzerinde üç kişi tarafından ortak yürütüldü ve her ekip üyesi bir başkasının modülünü test etti.

**Anahtar kelimeler:** veritabanı tasarımı, ER diyagramı, normalleştirme, PostgreSQL, Python, Tkinter, hastane randevu sistemi
