# 7b- UML Sınıf Diyagramı

Sınıf diyagramı, Python uygulamasının hangi sınıflardan oluştuğunu, her sınıfın neleri tuttuğunu, hangi işleri yaptığını ve sınıfların birbiriyle nasıl bağlandığını gösterir. Diyagramı draw.io'da çizdik (docs/tasarim/uml_sinif_diyagrami.png). Sınıfların adları ve metotları, app klasöründeki Python dosyalarıyla aynıdır.

Şemada kullanılan şekiller:

- **Üç bölmeli dikdörtgen:** sınıf. Üstte sınıfın adı, ortada alanları (veriler), altta metotları (yaptığı işler) yazar.
- **+ işareti:** dışarıdan kullanılabilen (public) metot
- **- işareti:** sadece sınıfın kendi içinde kullanılan (private) alan
- **Düz ok:** iki sınıf arasındaki ilişki. Okun üstündeki yazı ilişkinin türünü söyler.

## Sınıflar

Diyagramda dokuz sınıf var:

- **AnaMenu:** Uygulamanın ilk penceresi (tk.Tk'den türer). Her ekran için bir düğmesi vardır. hasta_ac(), randevu_ac(), bolum_doktor_ac(), doktor_paneli_ac(), recete_ac() ve istatistik_ac() metotları ilgili ekranı açar, cikis() uygulamayı kapatır.
- **HastaEkrani:** Hasta kaydetme, arama ve güncelleme ekranı (FG-01 – FG-04). Metotları hasta_kaydet(), hasta_ara(), hasta_guncelle() ve listeyi_yenile().
- **RandevuEkrani:** Randevu alma, iptal etme ve listeleme ekranı (FG-05 – FG-09). Metotları randevu_al(), randevu_iptal(), cakisma_kontrol(), gecmis_tarih_kontrol() ve randevulari_listele().
- **BolumDoktorEkrani:** Bölümleri ve doktorları listeler (bolumleri_listele(), doktorlari_listele()).
- **DoktorPaneli:** Doktorun günlük randevularını gösterir, seçilen randevu için muayene ekranını açar (gunluk_randevulari_getir(), muayene_ac()).
- **MuayeneEkrani:** Muayene kaydını ve teşhisleri girer (muayene_kaydet(), teshis_ekle(), recete_ac()). Hangi randevunun muayenesi olduğunu randevu_id alanında tutar.
- **ReceteEkrani:** Reçete oluşturur ve reçeteye ilaç ekler (recete_olustur(), ilac_ekle()). Hangi muayenenin reçetesi olduğunu muayene_id alanında tutar.
- **IstatistikEkrani:** Yönetici için istatistikleri gösterir (istatistikleri_getir()).
- **Veritabani:** PostgreSQL bağlantısını yöneten sınıf (db.py). getir(), getir_tek(), calistir(), ekle() ve hata_mesaji() metotlarını içerir. baglanti alanında açık bağlantıyı tutar.

Yedi ekran sınıfı tk.Toplevel'dan türer, yani ana menüden açılan ayrı birer pencere olarak çalışır. Hepsinin yapıcısı ana pencereyi alır ve ana_pencere alanında saklar. Bu alan sadece sınıfın kendi içinde kullanıldığı için başında - işareti var. Metotların hepsi ekran tarafından çağrıldığı için + ile gösterildi.

## İlişkiler

- **AnaMenu → ekranlar «açar»:** Ana menüdeki her düğme bir ekranı açar. Ok AnaMenu'den ekran sınıfına doğru çizildi.
- **DoktorPaneli → MuayeneEkrani «açar»:** Doktor panelinde bir randevu seçilince o randevunun muayene ekranı açılır.
- **MuayeneEkrani → ReceteEkrani «açar»:** Muayene kaydı girildikten sonra reçete ekranı açılabilir. Bu ilişki, kullanım durumu şemasındaki "Reçete yaz «extend» Muayene kaydı gir" ilişkisine karşılık gelir.
- **Ekranlar → Veritabani «kullanır»:** Bütün ekranlar veriyi okumak ve yazmak için Veritabani sınıfındaki ortak db nesnesini kullanır. Ekranlar veritabanına doğrudan bağlanmaz. Böylece bağlantı kodu tek yerde durur, SQL değerleri her zaman %s ile parametre olarak gönderilir ve veritabanı hataları her ekranda aynı Türkçe mesajlarla gösterilir.

## Neden Hasta ve Randevu sınıfı yok?

Sınıf diyagramında Hasta, Randevu gibi ayrı model sınıfları çizmedik. Çünkü bu verilerin yapısı zaten veritabanı tablolarında tanımlı (hasta, randevu vb.). Ekranlar SQL ile tablodan veriyi alıp doğrudan kullanıyor. Ayrıca bir model sınıfı yazsaydık aynı alanları hem tabloda hem Python'da iki kere tanımlamış olurduk. Uygulama küçük olduğu için bu fazladan katman işleri sadece karmaşıklaştırırdı. Verilerin yapısı ve ilişkileri ER diyagramı ile ilişkisel şemada gösterildiği için sınıf diyagramı yalnızca uygulamanın ekran ve bağlantı yapısını anlatıyor.
