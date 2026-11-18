# GitHub ve Commit Kuralları

1. Herkes **kendi GitHub hesabıyla** commit atar. Başkasının yerine commit atılmaz.
2. Küçük ve sık commit: her commit tek bir anlamlı iş içersin.
   - ✅ `hasta tablosu için CREATE TABLE eklendi`
   - ✅ `randevu çakışma kontrolü eklendi`
   - ❌ `update`, `düzeltme`, `asdf`
3. Herkes **sadece kendi dosyalarını** değiştirir. Başkasının dosyasında bir sorun görürsen dosyayı değiştirmeden önce ona veya ekibe haber ver.
4. Dosyaları GitHub web sitesinden yüklüyoruz, doğrudan `main`'e. Bu yüzden yüklemeden önce sayfayı yenileyip dosyanın son hâline bak.
5. Veritabanı şifresi gibi kişisel bilgiler repoya yüklenmez (`app/config.py` `.gitignore`'dadır).
6. Tablo ve sütun isimleri küçük harfle, Türkçe karakter olmadan ve alt çizgiyle yazılır (`hasta_id`, `dogum_tarihi`).

## GitHub web sitesinden çalışma

- **Yeni dosya:** Repo → **Add file → Create new file**. Dosya adına klasörüyle birlikte yaz (örn. `sql/veri/02_hasta_randevu_veri.sql`), klasör yoksa kendiliğinden oluşur.
- **Dosya yükleme:** **Add file → Upload files** ile sürükle bırak (Word, PDF, resim).
- **Düzenleme:** Dosyayı açıp sağ üstteki kalem simgesine bas.
- Her işlemin sonunda anlamlı bir mesajla **Commit changes**.

## Bilgisayarda Git kullanan için

```bash
git pull                          # en güncel hâli al
git add sql/04_ilac_recete.sql    # sadece kendi dosyanı ekle
git commit -m "recete tablosu eklendi"
git push
```
