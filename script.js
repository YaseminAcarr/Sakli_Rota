const API_URL = "http://127.0.0.1:5000/api"; // (Python/Flask) sunucu adresi
const el = (id) => document.getElementById(id); // Kısayol: document.getElementById
let map,             
  layers,            
  tempMarker,        
  editId = null,    
  userId = null;   

// --- 1. HARİTA KURULUMU ---
map = L.map("map").setView([40.9128, 38.3895], 13); 
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { 
  maxZoom: 19,
}).addTo(map);
layers = L.layerGroup().addTo(map); 

// Haritaya tıklayınca pin bırak
map.on("click", (e) => {
  const { lat, lng } = e.latlng; // Tıklanan koordinatları formdaki gizli inputlara yaz
  el("lat").value = lat.toFixed(6);
  el("lon").value = lng.toFixed(6);
  el("coords").innerText = `${lat.toFixed(6)}, ${lng.toFixed(6)} ${
    editId ? "(Yeni)" : ""  
  }`;  // Varsa eski geçici pini sil, yenisini ekle
  if (tempMarker) map.removeLayer(tempMarker);
  tempMarker = L.marker(e.latlng).addTo(map);
});

// --- 2. MERKEZİ İSTEK FONKSİYONU ---
async function istek(endpoint, method = "GET", body = null) {
  const opts = { method, credentials: "include" }; 
  if (body) {
    // Dosya/Resim Yükleme (FormData) ise olduğu gibi bırak, JSON ise string'e çevir
    opts.body = body instanceof FormData ? body : JSON.stringify(body);
    if (!(body instanceof FormData))
      opts.headers = { "Content-Type": "application/json" };
  }
  try { // İletişim ve Cevap
    const res = await fetch(API_URL + endpoint, opts); 
    return await res.json();
  } catch (e) {
    console.error("Backend bağlantı hatası:", e); 
    return { hata: true };
  }
}

// --- 3. KULLANICI İŞLEMLERİ ---
async function checkUser() { // Sayfa yüklendiğinde oturum kontrolü yapar
  const d = await istek("/user-info");
  userId = d.giris_var ? d.id : null;
  el("login-screen").classList.toggle("hidden", d.giris_var); // Giriş varsa login ekranını gizle
  el("app-screen").classList.toggle("hidden", !d.giris_var); // Giriş yoksa uygulama ekranını gizle
  if (d.giris_var) {
    el("display-username").innerText = d.kullanici;
    haritaGetir();
    setTimeout(() => map.invalidateSize(), 100); 
  }
}
checkUser(); // Başlat
// Giriş ve Kayıt işlemlerini yöneten ortak fonksiyon
const authIslem = (path, uId, pId) => {
  istek(path, "POST", {
    kullanici_adi: el(uId).value,
    sifre: el(pId).value,
  }).then((d) => {
    if (d.hata) alert(d.hata);
    else if (d.mesaj === "Kayıt başarılı!") {
      alert(d.mesaj);
      window.formDegistir(); 
    } else checkUser(); // Başarılı girişse ana ekrana geç
  });
};

// HTML'den çağrılan fonksiyonlar
window.girisYap = () => authIslem("/login", "login-user", "login-pass");
window.kayitOl = () => authIslem("/register", "reg-user", "reg-pass");
window.cikisYap = () => istek("/logout", "POST").then(() => checkUser());
window.formDegistir = () => { 
  el("login-form").classList.toggle("hidden");
  el("register-form").classList.toggle("hidden");
};

// --- 4. CRUD İŞLEMLERİ ---
window.haritaGetir = async (benim = false) => { 
  layers.clearLayers(); // Eski pinleri temizle
  const kat = el("filtre-kategori").value;
  const url = `/locations?t=1${benim ? "&benim=true" : ""}${ // URL oluşturma: Filtreler varsa URL'ye ekle
    kat !== "0" ? "&kategori=" + kat : ""
  }`;

  const data = await istek(url);  //Python gidip mekan listesini ister.
  if (!data || data.hata) return;

  data.forEach((yer) => {  
    const img = yer.Gorsel // Resim varsa HTML kodunu hazırla, yoksa boş bırak
      ? `<img src="http://127.0.0.1:5000/${yer.Gorsel}" class="popup-img">`
      : "";
    const safeBaslik = yer.Baslik.replace(/'/g, "\\'"); 
    const safeAciklama = (yer.Aciklama || "").replace(/'/g, "\\'");

    const btn = // Sadece mekanı ekleyen kişi Düzenle/Sil butonlarını görebilir
      userId === yer.User_ID
        ? `
            <div class="popup-btn-group">
                <button onclick="duzenle(${yer.Lokasyon_ID}, '${safeBaslik}', '${yer.Kategori_ID}', ${yer.Lat}, ${yer.Lon}, '${safeAciklama}')" style="background:#f39c12;">Düzenle</button>
                <button onclick="sil(${yer.Lokasyon_ID})" style="background:#e74c3c;">Sil</button>
            </div>`
        : "";
   // Popup içeriği
    const html = `<div style="min-width:200px">${img}<b>${
      yer.Baslik
    }</b><br><small>${yer.Kategori_Adi || "Genel"}</small><p>${
      yer.Aciklama || ""
    }</p><small>👤 ${yer.KullaniciAdi}</small>${btn}</div>`;
    L.marker([yer.Lat, yer.Lon]).addTo(layers).bindPopup(html); // Pini haritaya ekle ve içeriği bağla
  });
};
// Düzenle butonuna basınca formu doldurur
window.duzenle = (id, baslik, kat, lat, lon, aciklama) => {
  editId = id;
  el("baslik").value = baslik;
  el("aciklama").value = aciklama;
  el("kategori").value = kat;
  el("lat").value = lat;
  el("lon").value = lon;  
  // UI Güncellemesi
  el("coords").innerText = `${lat}, ${lon} (Düzenleniyor)`;
  el("kaydetBtn").innerText = "Güncelle";
  el("kaydetBtn").className = "btn-green";
  el("kaydetBtn").style.background = "#f39c12";
  el("iptalBtn").classList.remove("hidden");
};

window.sil = (id) => // Silme işlemi
  confirm("Silinsin mi?") &&
  istek(`/locations/${id}`, "DELETE").then((d) => {
    alert(d.mesaj);
    haritaGetir();
  });
// Formu temizle ve "Yeni Ekleme" moduna dön
window.formuSifirla = () => {
  el("yerEkleForm").reset();
  editId = null;
  el("coords").innerText = "Haritadan seçin";
  el("kaydetBtn").innerText = "Kaydet";
  el("kaydetBtn").style.background = "#4caf50";
  el("iptalBtn").classList.add("hidden");
  if (tempMarker) map.removeLayer(tempMarker);
};

// Form Gönderimi (Otomatik Veri Toplama)
el("yerEkleForm").addEventListener("submit", async (e) => {
  e.preventDefault(); // Sayfanın yenilenmesini engelle
  const fd = new FormData(el("yerEkleForm")); // name="" olan her şeyi otomatik alır

  // Hidden inputların FormData'ya girdiğinden emin olalım (Eksik Veri Kontrolü)
  if (!fd.has("lat")) fd.append("lat", el("lat").value);
  if (!fd.has("lon")) fd.append("lon", el("lon").value);
  if (!fd.has("kategori_id")) fd.append("kategori_id", el("kategori").value);
  // editId varsa güncelleme (PUT), yoksa yeni kayıt (POST) yap  (Ekleme/Düzenleme)
  const url = editId ? `/locations/${editId}` : "/locations";
  const method = editId ? "PUT" : "POST";

  const d = await istek(url, method, fd);
  alert(d.mesaj || d.hata);
  if (!d.hata) {
    haritaGetir(); // Listeyi yenile
    formuSifirla(); // Formu temizle
  }
});
