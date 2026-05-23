# JS Extractor & Security Analyzer

Bu uygulama, herhangi bir web sitesindeki JavaScript dosyalarını bulup eşzamanlı olarak indiren, formatlayan ve güvenlik analizi gerçekleştiren Python tabanlı bir masaüstü aracıdır.

## Özellikler

* **Hızlı ve Paralel İndirme:** Web sitesindeki tüm JavaScript dosyalarını ThreadPoolExecutor yardımıyla eşzamanlı olarak indirir.
* **JS Güzelleştirici (Beautifier):** Çekilen sıkıştırılmış (minified) JavaScript kodlarını okunabilir hale getirmek için otomatik olarak biçimlendirir.
* **Güvenlik ve Veri Analizi:** İndirilen kodları düzenli ifadelerle (regex) tarayarak olası API anahtarlarını, şifreleri, e-posta adreslerini, harici bağlantıları ve dahili dizin yollarını (endpoint) tespit eder.
* **Kod İçi Arama:** Çekilen kodlar içinde anlık arama yapılmasına ve eşleşen kelimelerin vurgulanmasına olanak tanır.
* **Toplu Kaydetme:** İndirilen ve biçimlendirilen tüm JavaScript dosyalarını yerel diske tek bir tıklama ile kaydeder.
* **Karanlık Tema:** Göz yormayan, modern ve karanlık mod arayüze sahiptir.

## Gereksinimler

Uygulamanın çalışması için bilgisayarınızda Python 3.x sürümünün ve aşağıdaki Python kütüphanelerinin kurulu olması gerekir:

* requests
* beautifulsoup4
* jsbeautifier

Gerekli kütüphaneleri yüklemek için terminalde aşağıdaki komutu çalıştırabilirsiniz:

```bash
pip install requests beautifulsoup4 jsbeautifier
```

## Çalıştırma

Uygulamayı çalıştırmak için proje dizininde terminali açıp şu komutu uygulayın:

```bash
python js_extractor.py
```

## PyInstaller ile EXE Sürümünü Oluşturma (Build)

Uygulamayı herhangi bir Python kurulumu gerektirmeksizin doğrudan Windows üzerinde çalıştırılabilir bir .exe dosyasına dönüştürmek için PyInstaller kullanabilirsiniz.

### 1. PyInstaller Kurulumu

PyInstaller kütüphanesini sisteminize kurmak için aşağıdaki komutu çalıştırın:

```bash
pip install pyinstaller
```

### 2. Derleme (Build) Komutu

Aşağıdaki komut, uygulamayı konsol ekranı olmadan, tüm bağımlılıkları tek bir çalıştırılabilir dosyaya gömecek şekilde paketleyecektir:

```bash
pyinstaller --noconfirm --onefile --windowed --name="JSExtractor" js_extractor.py
```

### Kullanılan Parametrelerin Açıklaması:

* `--noconfirm`: Daha önce oluşturulmuş çıktı klasörleri varsa onay istemeden üzerine yazar.
* `--onefile`: Uygulamayı ve tüm bağımlılıkları tek bir .exe dosyası halinde paketler.
* `--windowed` (veya `-w`): Uygulama başlatıldığında arkada siyah konsol (CMD) ekranının açılmasını engeller, sadece grafik arayüzü (GUI) gösterir.
* `--name="JSExtractor"`: Oluşturulacak çalıştırılabilir dosyanın adını belirler.

### 3. Çıktıya Erişim

Derleme işlemi başarıyla tamamlandıktan sonra proje klasörünüzde şu dizinler oluşacaktır:

* **dist/** -> Oluşturulan `JSExtractor.exe` dosyası bu klasörün içinde yer alır.
* **build/** -> Derleme işlemi sırasında kullanılan geçici dosyaları barındırır. Bu klasörü derleme sonrasında güvenle silebilirsiniz.
* **JSExtractor.spec** -> Derleme yapılandırma dosyasıdır. İhtiyacınız yoksa silebilirsiniz.

Bağımsız olarak çalıştırmak istediğiniz tek dosya `dist/JSExtractor.exe` dosyasıdır.
