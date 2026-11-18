# 8b- Uygulama Kullanıcı Arayüzleri: Ana Menü, Reçete ve İstatistik

Hazırlayan: Veronika

Ekran görüntüleri `docs/ekran_goruntuleri/` klasöründe.

## Ana Menü (veronika_ana_menu.png)

Uygulama `python main.py` komutuyla açıldığında ana menü gelir. Buradan altı ekrana geçilir: Hasta İşlemleri, Randevu İşlemleri, Bölümler ve Doktorlar, Doktor Paneli, Reçete ve İstatistikler (FG-22). Uygulama açılırken veritabanına bağlanılıp bağlanılamadığı kontrol edilir; bağlantı kurulamazsa kullanıcıya Türkçe bir hata mesajı gösterilir (FG-26).

## Reçete Ekranı (veronika_recete_ekrani.png)

Doktorun muayene sonunda reçete yazdığı ekran.

- **Muayene:** Muayene tarih, hasta ve doktor bilgisiyle listeden seçilir. Ekran doktorun muayene ekranından açıldığında muayene otomatik seçilir ve değiştirilemez. Muayenenin reçetesi varsa numarası ve tarihi gösterilir.
- **Reçete:** Muayenenin reçetesi yoksa doktor isterse bir açıklama yazar ve "Reçete Oluştur" düğmesine basar (FG-17). Bir muayeneye ikinci reçete yazılamaz; reçete varsa bu düğme kapalıdır.
- **İlaç Ekle:** İlaç listeden seçilir, doz, kullanım şekli ve kutu adedi girilerek reçeteye eklenir (FG-18). İlaç ya da doz boş bırakılırsa uyarı verilir. Aynı ilaç aynı reçeteye ikinci kez eklenmeye çalışılırsa "Bu ilaç bu reçeteye zaten eklenmiş." mesajı çıkar (FG-19).
- **Reçetedeki İlaçlar:** Reçetedeki ilaçlar doz, kullanım şekli ve kutu adediyle tabloda listelenir (FG-20). Seçilen ilaç "Seçili İlacı Çıkar" ile reçeteden çıkarılabilir.
- **Hastanın Geçmiş Reçeteleri (veronika_gecmis_receteler.png):** Hastaya daha önce yazılmış bütün reçeteler tarih, doktor, ilaç ve dozuyla ayrı bir pencerede gösterilir (FG-21). Bu liste `recete_detay` görünümünden (VIEW) okunur.

## İstatistik Ekranı (veronika_istatistik_ekrani.png)

Hastane yöneticisinin kullandığı ekran. Üç sekmeden oluşur:

- **En Çok Yazılan İlaçlar:** Her ilacın kaç reçetede yazıldığı ve toplam kaç kutu verildiği, en çok yazılandan aza doğru (FG-23).
- **Bölümlere Göre Hasta Sayısı:** Her bölüme randevu almış farklı hasta sayısı; iptal edilen randevular sayılmaz (FG-24).
- **Doktor Başına Muayene:** Her doktorun yaptığı muayene sayısı, bölümüyle birlikte (FG-25).

"Yenile" düğmesi istatistikleri veritabanından tekrar okur.
