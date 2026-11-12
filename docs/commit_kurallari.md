# GitHub ve Commit Kuralları

1. Herkes **kendi GitHub hesabıyla** ve kendi bilgisayarından commit atar. Başkasının yerine commit atılmaz.
2. Küçük ve sık commit: her commit tek bir anlamlı iş içersin.
   - ✅ `hasta tablosu için CREATE TABLE eklendi`
   - ✅ `randevu çakışma kontrolü eklendi`
   - ❌ `update`, `düzeltme`, `asdf`
3. Çalışmaya başlamadan önce `git pull`, bitirince `git push`.
4. Büyük işler kendi branch'inde yapılır ve Pull Request ile `main`'e birleştirilir. PR'ı Veronika onaylar.
   - Branch isim örnekleri: `eray/hasta-tablosu`, `sude/doktor-paneli`, `veronika/recete-ekrani`
5. Veritabanı şifresi gibi kişisel bilgiler repoya yüklenmez (`app/config.py` `.gitignore`'dadır).
6. Tablo ve sütun isimleri küçük harfle, Türkçe karakter olmadan ve alt çizgiyle yazılır (`hasta_id`, `dogum_tarihi`).

## Sık Kullanılan Komutlar

```bash
git pull                          # en güncel hâli al
git checkout -b eray/hasta-tablosu  # yeni branch aç
git add .                         # değişiklikleri hazırla
git commit -m "hasta tablosu eklendi"
git push -u origin eray/hasta-tablosu
```
