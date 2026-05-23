# JS Extractor & Security Analyzer

Language Selection / Dil Seçimi:
* [English](#english)
* [Türkçe](#türkçe)

---

## English

A Python-based desktop application designed to extract, beautify, and analyze JavaScript files from any website.

### Features

* **Fast Concurrent Downloading:** Downloads all JavaScript files from the target website simultaneously using ThreadPoolExecutor.
* **JS Beautifier:** Automatically formats minified JavaScript code to make it human-readable.
* **Security & Data Analysis:** Uses regular expressions to scan code for potential API keys, credentials, email addresses, external links, and internal endpoint paths.
* **In-Code Search:** Allows real-time search within the retrieved code with highlighted matching keywords.
* **Batch Export:** Saves all downloaded and formatted JavaScript files to a local directory with a single click.
* **Dark Mode UI:** Sleek, modern, and eye-friendly dark mode interface built with Tkinter.

### Requirements

Ensure you have Python 3.x and the following Python packages installed:

* requests
* beautifulsoup4
* jsbeautifier

Install the required packages using pip:

```bash
pip install requests beautifulsoup4 jsbeautifier
```

### Usage

Run the application by executing the following command in the project directory:

```bash
python js_extractor.py
```

### Building Executable (EXE) with PyInstaller

To package the application into a standalone executable for Windows, you can use PyInstaller.

#### 1. Install PyInstaller

```bash
pip install pyinstaller
```

#### 2. Build Command

Run the following command to compile the script into a single executable without a command prompt window:

```bash
pyinstaller --noconfirm --onefile --windowed --name="JSExtractor" js_extractor.py
```

#### Flag Explanations:

* `--noconfirm`: Overwrites existing build directories without asking.
* `--onefile`: Bundles everything into a single .exe executable.
* `--windowed` (or `-w`): Suppresses the console window so only the GUI is displayed.
* `--name="JSExtractor"`: Sets the name of the output executable.

#### 3. Output Location

After compilation, check the following directories:

* **dist/** -> Contains the compiled `JSExtractor.exe` file.
* **build/** -> Holds temporary build files. Can be safely deleted after compilation.
* **JSExtractor.spec** -> Compilation specification file. Can be deleted if not needed.

---

## Türkçe

Bu uygulama, herhangi bir web sitesindeki JavaScript dosyalarını bulup eşzamanlı olarak indiren, formatlayan ve güvenlik analizi gerçekleştiren Python tabanlı bir masaüstü aracıdır.

### Özellikler

* **Hızlı ve Paralel İndirme:** Web sitesindeki tüm JavaScript dosyalarını ThreadPoolExecutor yardımıyla eşzamanlı olarak indirir.
* **JS Güzelleştirici (Beautifier):** Çekilen sıkıştırılmış (minified) JavaScript kodlarını okunabilir hale getirmek için otomatik olarak biçimlendirir.
* **Güvenlik ve Veri Analizi:** İndirilen kodları düzenli ifadelerle (regex) tarayarak olası API anahtarlarını, şifreleri, e-posta adreslerini, harici bağlantıları ve dahili dizin yollarını (endpoint) tespit eder.
* **Kod İçi Arama:** Çekilen kodlar içinde anlık arama yapılmasına ve eşleşen kelimelerin vurgulanmasına olanak tanır.
* **Toplu Kaydetme:** İndirilen ve biçimlendirilen tüm JavaScript dosyalarını yerel diske tek bir tıklama ile kaydeder.
* **Karanlık Tema:** Göz yormayan, modern ve karanlık mod arayüze sahiptir.

### Gereksinimler

Uygulamanın çalışması için bilgisayarınızda Python 3.x sürümünün ve aşağıdaki Python kütüphanelerinin kurulu olması gerekir:

* requests
* beautifulsoup4
* jsbeautifier

Gerekli kütüphaneleri yüklemek için terminalde aşağıdaki komutu çalıştırabilirsiniz:

```bash
pip install requests beautifulsoup4 jsbeautifier
```

### Çalıştırma

Uygulamayı çalıştırmak için proje dizininde terminali açıp şu komutu uygulayın:

```bash
python js_extractor.py
```

### PyInstaller ile EXE Sürümünü Oluşturma (Build)

Uygulamayı herhangi bir Python kurulumu gerektirmeksizin doğrudan Windows üzerinde çalıştırılabilir bir .exe dosyasına dönüştürmek için PyInstaller kullanabilirsiniz.

#### 1. PyInstaller Kurulumu

```bash
pip install pyinstaller
```

#### 2. Derleme (Build) Komutu

```bash
pyinstaller --noconfirm --onefile --windowed --name="JSExtractor" js_extractor.py
```

#### Parametrelerin Açıklaması:

* `--noconfirm`: Onay istemeden önceki çıktı klasörlerinin üzerine yazar.
* `--onefile`: Uygulamayı ve tüm bağımlılıkları tek bir .exe dosyası halinde paketler.
* `--windowed` (veya `-w`): Grafik arayüzü başlatıldığında arka planda CMD penceresinin açılmasını engeller.
* `--name="JSExtractor"`: Oluşturulacak .exe dosyasının adını belirler.

#### 3. Çıktıya Erişim

Derleme işlemi sonrasında oluşan dizinler:

* **dist/** -> Oluşturulan `JSExtractor.exe` dosyası bu klasörün içindedir.
* **build/** -> Geçici derleme dosyalarını barındırır. İşlem bittikten sonra silinebilir.
* **JSExtractor.spec** -> Yapılandırma dosyasıdır. Silinebilir.
