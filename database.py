import sqlite3
import os

DB_NAME = 'lokal_rehber.db'

def baglanti_kur():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def veritabani_baslat(upload_folder):
    os.makedirs(upload_folder, exist_ok=True)
    conn = baglanti_kur()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            User_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            KullaniciAdi TEXT NOT NULL UNIQUE,
            Sifre_Hash TEXT NOT NULL,
            Kayit_Tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Categories (
            Kategori_ID INTEGER PRIMARY KEY,
            Kategori_Adi TEXT NOT NULL
        )
    """)

    kategoriler = [
        (1, 'Manzara & Seyir'),
        (2, 'Lezzet Durakları'),
        (3, 'Sessizlik & Huzur'),
        (4, 'Fotoğraf & Kadraj'),
        (5, 'Kamp & Doğa'),
        (6, 'Tarih & Kültür'),
        (7, 'Eğlence & Aktivite')
    ]
    cursor.executemany("INSERT OR IGNORE INTO Categories (Kategori_ID, Kategori_Adi) VALUES (?, ?)", kategoriler)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Locations (
            Lokasyon_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            User_ID INTEGER,
            Kategori_ID INTEGER,
            Baslik TEXT NOT NULL,
            Aciklama TEXT,
            Lat REAL NOT NULL,
            Lon REAL NOT NULL,
            Gorsel TEXT,
            Ekleme_Tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (User_ID) REFERENCES Users(User_ID) ON DELETE CASCADE,
            FOREIGN KEY (Kategori_ID) REFERENCES Categories(Kategori_ID)
        )
    """)
    conn.commit()
    conn.close()