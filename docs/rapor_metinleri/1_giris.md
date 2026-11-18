# 1- Giriş

Bu projede müşteri olarak hayali bir hastane olan **Doğuş Özel Hastanesi**'ni seçtik. Hastanede dahiliye, kardiyoloji, göz hastalıkları gibi farklı bölümler ve bu bölümlerde çalışan doktorlar bulunuyor. Hastalar randevu almak için hastaneyi telefonla arıyor, danışmadaki görevli de randevuyu bir deftere ya da kâğıda yazıyor.

Bu yöntem hastane küçükken işe yarasa da hasta sayısı arttıkça bazı sorunlar ortaya çıkıyor:

- **Çift randevu:** Randevular tek bir yerde tutulmadığı için aynı doktora aynı gün ve saatte iki farklı hastaya randevu verilebiliyor.
- **Geçmiş bilgilere ulaşmak zor:** Hasta tekrar geldiğinde önceki muayeneleri, konulan teşhisler ve doktorun notları kâğıt dosyalar arasında aranıyor. Bu da hem zaman kaybına hem de bilgilerin kaybolmasına yol açıyor.
- **Reçeteler takip edilemiyor:** Hangi hastaya hangi ilacın, ne kadar ve hangi doktor tarafından yazıldığı düzenli olarak tutulmuyor.
- **Raporlama yapılamıyor:** Hangi bölüme daha çok hasta geldiği ya da en çok hangi ilacın yazıldığı gibi sorulara cevap vermek için tüm kâğıtları tek tek saymak gerekiyor.

Bu sorunları çözmek için hastanenin bilgilerini tek bir ilişkisel veritabanında tutan basit bir **hastane randevu sistemi** tasarladık. Sistemde hasta kaydı yapılabilecek, bölüm ve doktor seçilerek randevu alınıp iptal edilebilecek, doktor o günkü randevularını görebilecek, muayene ve teşhis bilgileri kaydedilebilecek ve bir reçeteye birden fazla ilaç yazılabilecek. Aynı doktora aynı saatte ikinci randevu verilmesini veritabanı seviyesinde engelliyoruz.

Veritabanı PostgreSQL ile, uygulama ise Python ve Tkinter ile hazırlandı. Sistemde `hasta`, `randevu`, `bolum`, `doktor`, `muayene`, `teshis`, `ilac`, `recete` ve `recete_ilac` olmak üzere dokuz tablo bulunuyor.

Raporun devamında önce kullanılan teknolojileri, ardından veri ve fonksiyonel gereksinimleri anlatıyoruz. Sonra ER diyagramı, ilişkisel şema ve normalleştirme adımlarıyla veritabanı tasarımını, CREATE TABLE ifadelerini ve sorguları gösteriyoruz. Son olarak UML diyagramlarını ve uygulamanın ekranlarını sunuyoruz.
