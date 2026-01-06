# İşaret Dili Harf Tanıma Sistemi

Türkçe işaret dili harflerini tanıyan bir makine öğrenmesi projesi. Bu proje, web kamerasından alınan el işaretlerini gerçek zamanlı olarak tanıyabilen bir sistem içerir.


## 📋 Proje Hakkında

Bu proje, Türkçe işaret dili alfabesindeki harfleri tanımak için geliştirilmiş bir makine öğrenmesi sistemidir. Sistem, el pozisyonlarını analiz ederek hangi harfi gösterdiğinizi tahmin eder.

### Özellikler

- ✅ **Gerçek Zamanlı Tanıma**: Web kamerasından canlı görüntü işleme
- ✅ **REST API**: Flask tabanlı web servisi ile entegrasyon
- ✅ **Yüksek Doğruluk**: %98.5 doğruluk oranı
- ✅ **Türkçe Alfabe Desteği**: 29 harf (a-z, ç, ğ, ı, ö, ş, ü)
- ✅ **Kendi Veri Setimiz**: Tüm veriler manuel olarak toplanmıştır

## 🛠️ Kullanılan Teknolojiler

### Makine Öğrenmesi
- **scikit-learn**: Random Forest Classifier algoritması ile model eğitimi
- **NumPy**: Sayısal hesaplamalar ve veri işleme

### Görüntü İşleme
- **OpenCV (cv2)**: Video yakalama, görüntü işleme ve görselleştirme
- **MediaPipe**: Google'ın el landmark tespit kütüphanesi (21 nokta tespiti)
- **PIL/Pillow**: Görüntü formatı dönüşümleri

### Web API
- **Flask**: REST API geliştirme framework'ü
- **Flask-CORS**: Cross-Origin Resource Sharing desteği

### Veri Yönetimi
- **pickle**: Model ve veri seti serileştirme

## 📊 Veri Seti

**Önemli**: Bu projede kullanılan tüm veriler kendimiz tarafından toplanmıştır. 

- **Toplam Görüntü Sayısı**: ~2,900 görüntü
- **Harf Başına Görüntü**: 100 görüntü
- **Toplama Yöntemi**: Web kamerası ile manuel veri toplama
- **Veri Formatı**: JPG görüntüler, her harf için ayrı klasörlerde saklanmıştır

### Desteklenen Harfler

a, b, c, ç, d, e, f, g, ğ, h, ı, i, j, k, l, m, n, o, ö, p, r, s, ş, t, u, ü, v, y, z

## 🚀 Kurulum

### Gereksinimler

Python 3.7 veya üzeri gereklidir.

### Adımlar

1. **Repository'yi klonlayın:**
```bash
git clone <repository-url>
cd sign-language-detector-python
```

2. **Sanal ortam oluşturun (önerilir):**
```bash
python -m venv env
# Windows
env\Scripts\activate
# Linux/Mac
source env/bin/activate
```

3. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

## 📝 Kullanım

### 1. Veri Toplama

Kendi veri setinizi oluşturmak için:

```bash
python collect_imgs.py
```

Bu script:
- Web kamerasını açar
- Her harf için 100 görüntü toplar
- Görüntüleri `data/` klasörüne kaydeder
- Her harf için ayrı klasör oluşturur

### 2. Veri Seti Oluşturma

Toplanan görüntülerden özellik çıkarımı yapmak için:

```bash
python create_dataset.py
```

Bu script:
- `data/` klasöründeki tüm görüntüleri işler
- MediaPipe ile el landmark'larını çıkarır (21 nokta × 2 koordinat = 42 özellik)
- Normalize edilmiş koordinatları `data.pickle` dosyasına kaydeder

### 3. Model Eğitimi

```bash
python train_classifier.py
```

Bu script:
- `data.pickle` dosyasından veriyi yükler
- Veriyi %80 eğitim, %20 test olarak böler
- Random Forest Classifier ile model eğitir
- Eğitilmiş modeli `model.p` dosyasına kaydeder
- Test doğruluğunu konsola yazdırır

### 4. Gerçek Zamanlı Tahmin

Web kamerası ile canlı tahmin için:

```bash
python inference_classifier.py
```

Bu script:
- Web kamerasını açar
- Gerçek zamanlı olarak el işaretlerini analiz eder
- Ekranda tahmin edilen harfi gösterir

### 5. REST API

API'yi başlatmak için:

```bash
python api.py
```

API `http://localhost:5000` adresinde çalışacaktır.

Detaylı API dokümantasyonu için [README_API.md](README_API.md) dosyasına bakın.

## 🏗️ Proje Yapısı

```
sign-language-detector-python/
│
├── data/                  # Toplanan görüntüler (her harf için ayrı klasör)
├── collect_imgs.py       # Veri toplama scripti
├── create_dataset.py     # Özellik çıkarımı scripti
├── train_classifier.py   # Model eğitimi scripti
├── inference_classifier.py  # Gerçek zamanlı tahmin scripti
├── api.py                # Flask REST API
├── test_api.py          # API test scripti
├── model.p              # Eğitilmiş model (pickle formatı)
├── data.pickle          # İşlenmiş veri seti (pickle formatı)
├── requirements.txt     # Python bağımlılıkları
├── README.md           # Bu dosya
└── README_API.md        # API dokümantasyonu
```

## 🔬 Teknik Detaylar

### El Landmark Tespiti

- **MediaPipe Hands**: Google'ın el tespit modeli
- **21 Landmark Noktası**: Her el için 21 anatomik nokta
- **Koordinat Normalizasyonu**: Her görüntü için bağıl koordinatlar (min değerler çıkarılarak)

### Özellik Vektörü

- **Boyut**: 42 (21 nokta × 2 koordinat: x, y)
- **Normalizasyon**: Her koordinat, o görüntüdeki minimum x ve y değerlerinden çıkarılarak normalize edilir
- **Tek El Desteği**: Sistem şu anda sadece tek el işaretlerini destekler

### Makine Öğrenmesi Modeli

- **Algoritma**: Random Forest Classifier
- **Doğruluk**: %98.5
- **Veri Bölünmesi**: %80 eğitim, %20 test
- **Stratified Split**: Sınıf dağılımını koruyarak bölme

### API Endpoint'leri

- `GET /health` - API sağlık kontrolü
- `POST /predict` - Base64 encoded görüntü ile tahmin
- `POST /predict/file` - Dosya upload ile tahmin

## 📈 Model Performansı

- **Test Doğruluğu**: %98.5
- **Sınıf Sayısı**: 29 harf
- **Toplam Örnek**: ~2,900 görüntü
- **Özellik Sayısı**: 42 (normalize edilmiş el koordinatları)

## 🤝 Katkıda Bulunma

Bu proje açık kaynaklıdır ve katkılarınızı bekliyoruz. Pull request göndermekten çekinmeyin!

## 📄 Lisans

Bu proje [License](License) dosyasında belirtilen lisans altındadır.

## 🙏 Teşekkürler

- Google MediaPipe ekibine el tespit kütüphanesi için
- scikit-learn topluluğuna makine öğrenmesi araçları için
- OpenCV topluluğuna görüntü işleme kütüphanesi için

---

**Not**: Bu projede kullanılan tüm veriler manuel olarak toplanmıştır. Veri seti oluşturma süreci oldukça zaman alıcı olup, her harf için 100 görüntü toplanmıştır.
