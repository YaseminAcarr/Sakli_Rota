# 🗺️ Saklı Rota

> Saklı Rota, kullanıcıların keşfettikleri gizli manzara, lezzet, doğa ve fotoğraf duraklarını harita üzerinde paylaşabildiği, interaktif ve sosyal bir web tabanlı yerel rehber uygulamasıdır.

---

## 📸 Proje Ekran Görüntüleri

| Giriş & Kayıt Ekranı | 

<img width="1917" height="870" alt="Ana Sayfa" src="https://github.com/user-attachments/assets/d309f390-7ac1-432c-94be-6567924a66a0" /> 

---
|Harita & Keşfet Arayüzü |

<img width="1917" height="870" alt="Ana Sayfa" src="https://github.com/user-attachments/assets/d7a3bee4-5e35-4191-9eeb-f23a6c62f7c9" />

<img width="1917" height="871" alt="Filtreleme" src="https://github.com/user-attachments/assets/2941085a-caf0-45e2-91f3-3522e78e1844" />

---


## ✨ Özellikler

* **İnteraktif Harita:** Leaflet.js ve OpenStreetMap entegrasyonu ile harita üzerinden kolayca koordinat seçme ve mevcut noktaları görüntüleme.
* **Kategorize Edilmiş Keşif:** Manzara, lezzet durakları, kamp & doğa, fotoğraf kadrajı ve tarih gibi farklı kategorilerde anlık filtreleme yapabilme.
* **Kullanıcı Yetkilendirme:** Güvenli oturum yönetimi (Flask Session tabanlı) ve kullanıcıya özel içerik kontrolü.
* **CRUD İşlemleri:** Kullanıcıların kendi ekledikleri noktaları fotoğraflı bir şekilde eklemesi, güncellemesi ve silmesi.
* **Kişiselleştirilmiş Görünüm:** "Sadece Benimkiler" veya "Herkesi Göster" seçenekleriyle dinamik harita katmanları.
* **Sıfır Kurulum Veritabanı:** SQLite altyapısı sayesinde harici bir veritabanı sunucusuna ihtiyaç duymadan otomatik tablo ve şema oluşturma.

---

## 🛠️ Kullanılan Teknolojiler

* **Frontend:** HTML5, CSS3, JavaScript (Vanilla JS), [Leaflet.js](https://leafletjs.com/)
* **Backend:** Python, [Flask](https://flask.palletsprojects.com/), Flask-CORS, Werkzeug
* **Veritabanı:** SQLite3 (`database.py` modüler mimarisiyle)

---

## 📂 Proje Dizin Yapısı
```text
Sakli_Rota/
│
├── static/                   # Statik dosyalar
│   ├── uploads/              # Kullanıcıların yüklediği mekan fotoğrafları
│   └── logo.png              # Proje logosu ve favicon
│
├── database.py               # SQLite veritabanı bağlantı ve şema yönetimi
├── lokasyon.py               # Flask backend sunucusu ve API rotaları
├── index.html                # Arayüz ana HTML dosyası
├── script.js                 # Harita, form ve frontend API istekleri
├── style.css                 # Arayüz stil ve tasarım dosyası
├── görsel.jpg                # Giriş ekranı arkaplan görseli
├── .gitignore                # Git takip dışı bırakılan dosyalar
└── README.md                 # Proje dokümantasyonu ve kurulum rehberi
```
---

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
pip install Flask flask-cors Werkzeug
```
### 4. Uygulamayı Başlatın
```bash
python lokasyon.py
```
## 5. Arayüzü Açın
VS Code üzerinden index.html dosyasına sağ tıklayıp "Open with Live Server" seçeneği ile projeyi tarayıcınızda çalıştırabilirsiniz.
