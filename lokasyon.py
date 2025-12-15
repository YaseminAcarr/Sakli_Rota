from flask import Flask, request, jsonify, session
from flask_cors import CORS
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__) # Flask uygulamasını başlatma
app.secret_key = 'gizli_anahtar_sakli_rota'  # Kullanıcı giriş yaptığında tarayıcı çerezlerini şifrelemek için kullanılır.
CORS(app, supports_credentials=True, origins=["http://127.0.0.1:5500", "http://localhost:5500"]) # HTML ve Python farklı portlarda çalıştığı için

# --- Ayarlar ---
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456', 
    'database': 'lokal_rehber'
}

def baglanti_kur():
    return mysql.connector.connect(**db_config)

def allowed_file(filename):      
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- 1. KAYIT OL  ---
@app.route('/api/register', methods=['POST'])
def kayit_ol():
    veri = request.get_json()
    try:
        conn = baglanti_kur()
        cursor = conn.cursor()        
        cursor.execute("INSERT INTO Users (KullaniciAdi, Sifre_Hash) VALUES (%s, %s)", (veri.get('kullanici_adi'), veri.get('sifre')))
        conn.commit()
        conn.close()
        return jsonify({'mesaj': 'Kayıt başarılı!'}), 201
    except mysql.connector.Error as err:
        return jsonify({'hata': f'Hata: {err}'}), 409

# --- 2. GİRİŞ YAP ---
@app.route('/api/login', methods=['POST'])
def giris_yap():
    veri = request.get_json()
    conn = baglanti_kur()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users WHERE KullaniciAdi = %s", (veri.get('kullanici_adi'),))
    kullanici = cursor.fetchone()
    conn.close()

    if kullanici and kullanici['Sifre_Hash'] == veri.get('sifre'):
        session['user_id'] = kullanici['User_ID']
        session['username'] = kullanici['KullaniciAdi']
        return jsonify({'mesaj': 'Giriş başarılı', 'kullanici': kullanici['KullaniciAdi']}), 200
    else:
        return jsonify({'hata': 'Hatalı kullanıcı adı veya şifre!'}), 401

# --- 3. ÇIKIŞ YAP  ---
@app.route('/api/logout', methods=['POST'])
def cikis_yap():
    session.clear()
    return jsonify({'mesaj': 'Çıkış yapıldı'}), 200

# --- 4. KULLANICI BİLGİSİ  ---  # Frontend sayfayı yenilediğinde kullanıcının hala giriş yapmış olup olmadığını kontrol eder.
@app.route('/api/user-info', methods=['GET'])
def user_info():
    if 'user_id' in session:
        return jsonify({'giris_var': True, 'kullanici': session['username'], 'id': session['user_id']})
    return jsonify({'giris_var': False})

# --- 5. LİSTELEME  ---
@app.route('/api/locations', methods=['GET'])
def lokasyonlari_getir():
    conn = baglanti_kur()
    cursor = conn.cursor(dictionary=True)
    
    sadece_benim = request.args.get('benim') == 'true'
    kategori_filtre = request.args.get('kategori') 
    user_id = session.get('user_id')

    # LEFT JOIN ile Kategoriler ve Kullanıcılar tablolarından isim bilgilerini de çekiyor
    sql = """
        SELECT L.Lokasyon_ID, L.Baslik, L.Aciklama, L.Lat, L.Lon, L.Gorsel, C.Kategori_Adi, U.KullaniciAdi, L.User_ID, L.Kategori_ID
        FROM Locations L
        LEFT JOIN Categories C ON L.Kategori_ID = C.Kategori_ID
        LEFT JOIN Users U ON L.User_ID = U.User_ID
        WHERE 1=1 
    """
    
    params = []
    
    if sadece_benim and user_id: # Filtre: Sadece giriş yapan kullanıcının eklediği yerler
        sql += " AND L.User_ID = %s"
        params.append(user_id)
    
    if kategori_filtre and kategori_filtre != "0": # Filtre: Belirli bir kategori seçildiyse
        sql += " AND L.Kategori_ID = %s"
        params.append(kategori_filtre)
        
    sql += " ORDER BY L.Ekleme_Tarihi DESC" 

    cursor.execute(sql, params)
    sonuclar = cursor.fetchall()
    conn.close()
    return jsonify(sonuclar), 200

# --- 6. YER EKLEME ---
@app.route('/api/locations', methods=['POST'])
def lokasyon_ekle():
    if 'user_id' not in session:
        return jsonify({'hata': 'Oturum açmalısınız'}), 401
        
    gorsel_yolu = None
    if 'gorsel' in request.files: # İstekte dosya var mı kontrol et
        file = request.files['gorsel']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename) 
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # Dosyayı kaydet
            gorsel_yolu = f"static/uploads/{filename}"

    conn = baglanti_kur()
    cursor = conn.cursor()       
    sql = "INSERT INTO Locations (User_ID, Kategori_ID, Baslik, Aciklama, Lat, Lon, Gorsel) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (session['user_id'], request.form['kategori_id'], request.form['baslik'], request.form['aciklama'], request.form['lat'], request.form['lon'], gorsel_yolu)
    cursor.execute(sql, val)
    conn.commit()
    conn.close()
    return jsonify({'mesaj': 'Başarıyla eklendi!'}), 201

# --- 7. YER GÜNCELLEME ---
@app.route('/api/locations/<int:id>', methods=['PUT'])
def lokasyon_guncelle(id):
    if 'user_id' not in session:
        return jsonify({'hata': 'Yetkisiz erişim'}), 401

    conn = baglanti_kur()
    cursor = conn.cursor(dictionary=True)
    
    # Önce kaydın var olup olmadığını ve bu kullanıcıya ait olup olmadığını kontrol et
    cursor.execute("SELECT * FROM Locations WHERE Lokasyon_ID=%s AND User_ID=%s", (id, session['user_id']))
    mevcut_kayit = cursor.fetchone()
    
    if not mevcut_kayit:
        conn.close()
        return jsonify({'hata': 'Kayıt bulunamadı veya yetkiniz yok.'}), 403

    baslik = request.form['baslik']
    aciklama = request.form['aciklama']
    kategori_id = request.form['kategori_id']
    lat = request.form['lat']
    lon = request.form['lon']

    yeni_gorsel_yolu = None
    gorsel_guncellenecek = False

    if 'gorsel' in request.files: # Yeni bir resim yüklenmiş mi?
        file = request.files['gorsel']
        if file and file.filename != '' and allowed_file(file.filename):
            # Yeni dosya kaydet
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            yeni_gorsel_yolu = f"static/uploads/{filename}"
            gorsel_guncellenecek = True
            
            # Eski dosyayı sil
            eski_gorsel = mevcut_kayit['Gorsel']
            if eski_gorsel and os.path.exists(eski_gorsel):
                try:
                    os.remove(eski_gorsel)
                except:
                    pass
    
    if gorsel_guncellenecek:
        sql = "UPDATE Locations SET Baslik=%s, Aciklama=%s, Kategori_ID=%s, Lat=%s, Lon=%s, Gorsel=%s WHERE Lokasyon_ID=%s"
        val = (baslik, aciklama, kategori_id, lat, lon, yeni_gorsel_yolu, id)
    else:
        sql = "UPDATE Locations SET Baslik=%s, Aciklama=%s, Kategori_ID=%s, Lat=%s, Lon=%s WHERE Lokasyon_ID=%s"
        val = (baslik, aciklama, kategori_id, lat, lon, id)

    cursor.execute(sql, val)
    conn.commit()
    conn.close()
    
    return jsonify({'mesaj': 'Başarıyla güncellendi!'}), 200

# --- 8. YER SİLME  ---
@app.route('/api/locations/<int:id>', methods=['DELETE'])
def lokasyon_sil(id):
    if 'user_id' not in session:
        return jsonify({'hata': 'Yetkisiz erişim'}), 401

    conn = baglanti_kur()
    cursor = conn.cursor(dictionary=True)
    # Silinecek kaydın resim yolunu al
    cursor.execute("SELECT Gorsel FROM Locations WHERE Lokasyon_ID = %s AND User_ID = %s", (id, session['user_id']))
    kayit = cursor.fetchone()
    
    if not kayit:
        conn.close()
        return jsonify({'hata': 'Kayıt bulunamadı veya yetkiniz yok.'}), 403
    # Veritabanından sil
    cursor.execute("DELETE FROM Locations WHERE Lokasyon_ID = %s", (id,))
    conn.commit()
    conn.close()

    if kayit['Gorsel']: # Eğer kayda ait bir resim varsa, onu da klasörden sil
        try:
            if os.path.exists(kayit['Gorsel']):
                os.remove(kayit['Gorsel'])
        except Exception as e:
            print(f"Dosya silinemedi: {e}")

    return jsonify({'mesaj': 'Kayıt silindi.'}), 200

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
