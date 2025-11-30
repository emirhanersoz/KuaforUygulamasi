# ✂️ Kuaför Randevu Sistemi

Bu proje, kuaför ve berber salonları için geliştirilmiş kapsamlı bir **Masaüstü Randevu ve Yönetim Sistemi**dir. Python ve PyQt6 kullanılarak geliştirilmiştir. Modern arayüzü, akıllı randevu algoritması ve rol tabanlı yönetim sistemi ile profesyonel bir çözüm sunar.

## 🌟 Özellikler

Sistem üç farklı kullanıcı rolü (Admin, Çalışan, Müşteri) üzerine kurulmuştur:

### 👤 Müşteri Paneli
* **Kolay Kayıt & Giriş:** Sisteme kendi kendine kayıt olma ve giriş yapma.
* **Akıllı Randevu Alma:** Salon, personel ve hizmet seçimi.
* **Otomatik Saat Hesaplama:** Sadece personelin uygun olduğu ve mesai saatleri içindeki boşlukları görme (Çakışma engelleme).
* **Randevu Takibi:** Kendi randevularını listeleme, durumunu (Onaylandı/Bekliyor) görme ve iptal etme.

### ✂️ Çalışan Paneli (Personel)
* **Çalışma Masam:** Kendine özel yönetim paneli.
* **Mesai Yönetimi:** Günlük çalışma saatlerini (Başlangıç-Bitiş) belirleme ve güncelleme.
* **Hizmet Yönetimi:** Kendi verdiği hizmetleri, sürelerini ve ücretlerini belirleme.
* **Randevu Yönetimi:** Gelen randevu taleplerini Onaylama veya Reddetme.

### 🛠 Yönetici Paneli (Admin)
* **Tam Kontrol:** Salon, Personel ve Kullanıcı yönetimi.
* **Kullanıcı Rolleri:** Müşterileri çalışana veya yöneticiye terfi ettirme.
* **Tüm Randevular:** İşletmedeki tüm randevuları görüntüleme ve yönetme.

## 🎨 Arayüz ve Tasarım
* **Modern Tema:** "Soft Lavender & Pink" renk paleti ile ferah ve şık görünüm.
* **Responsive Yapı:** Kullanıcı dostu formlar ve tablolar.
* **Görsel Geri Bildirim:** Renkli durum etiketleri (Onaylandı: Yeşil, İptal: Kırmızı vb.).

## 💻 Teknolojiler

* **Dil:** Python 3.x
* **Arayüz (GUI):** PyQt6
* **Veritabanı:** MySQL
* **ORM:** SQLAlchemy
* **Sürücü:** PyMySQL

## ⚙️ Kurulum ve Çalıştırma

Projeyi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin.

### 1. Gereksinimler
* Python 3.10 veya üzeri
* MySQL Server (XAMPP veya MySQL Workbench)

### 2. Kütüphanelerin Yüklenmesi
Terminali açın ve gerekli kütüphaneleri yükleyin:

```bash
pip install PyQt6 SQLAlchemy pymysql cryptography