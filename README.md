# 🗺️ Saklı Rota

> Saklı Rota, kullanıcıların keşfettikleri gizli manzara, lezzet ve doğa duraklarını harita üzerinde paylaşabildiği, interaktif ve sosyal bir web tabanlı yerel rehber uygulamasıdır.

![Proje Ekran Görüntüsü](static/logo.png) <!-- Varsa ana ekran GIF/Görseli buraya eklenebilir -->

## ✨ Özellikler

* **İnteraktif Harita:** Leaflet.js entegrasyonu ile harita üzerinden kolayca koordinat seçme ve mevcut noktaları görüntüleme.
* **Kategorize Edilmiş Keşif:** Manzara, lezzet durakları, kamp & doğa ve tarih gibi farklı kategorilerde filtreleme yapabilme[cite: 2, 3].
* **Kullanıcı Yetkilendirme:** Güvenli oturum yönetimi (Session tabanlı) ve kullanıcıya özel içerik yönetimi[cite: 2].
* **CRUD İşlemleri:** Kullanıcıların kendi ekledikleri noktaları fotoğraflı bir şekilde eklemesi, güncellemesi ve silmesi[cite: 2, 3].
* **Kişiselleştirilmiş Filtreleme:** "Sadece Benimkiler" veya "Herkesi Göster" seçenekleriyle dinamik harita katmanları[cite: 2, 3].

## 🛠️ Kullanılan Teknolojiler

* **Frontend:** HTML5, CSS3, JavaScript (Vanilla JS), [Leaflet.js](https://leafletjs.com/)
* **Backend:** Python, [Flask](https://flask.palletsprojects.com/), Flask-CORS
* **Veritabanı:** MySQL, `mysql-connector-python`

---
## 📂 Proje Dizin Yapısı
```text
Sakli_Rota/
│
├── static/                   # Statik dosyalar (Görseller, stiller, logolar)
│   ├── uploads/              # Kullanıcıların yüklediği mekan fotoğrafları
│   ├── görsel.jpg            # Giriş ekranı arkaplan görseli
│   └── logo.png              # Proje logosu ve favicon
│
├── app.py                    # Flask backend sunucusu ve API rotaları
├── index.html                # Arayüz ana HTML dosyası
├── style.css                 # Arayüz stil ve tasarım dosyası
├── script.js                 # Harita, form ve frontend API istekleri
└── README.md                 # Proje dokümantasyonu ve kurulum rehberi
```
## 🚀 Kurulum ve Çalıştırma

Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları takip edebilirsiniz:

### 1. Projeyi Klonlayın
```bash
git clone [https://github.com/YaseminAcarr/Sakli_Rota.git](https://github.com/YaseminAcarr/Sakli_Rota.git)
cd Sakli_Rota
```
### 2. Sanal Ortam Oluşturun ve Aktif Edin
```bash
python -m venv venv
# Windows için:
venv\Scripts\activate
# macOS / Linux için:
source venv/bin/activate
```
### 3. Gerekli Kütüphaneleri Yükleyin
```bash
pip install Flask flask-cors mysql-connector-python Werkzeug
```
### 4. Veritabanı Ayarları
MySQL üzerinde lokal_rehber adında bir veritabanı oluşturun.
Flask uygulamasındaki (app.py) bağlantı ayarlarını kendi yerel veritabanı şifrenize göre güncelleyin:
```bash
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'SİZİN_ŞİFRENİZ', 
    'database': 'lokal_rehber'
}
```
### 5. Uygulamayı Başlatın
```bash
python app.py
```
