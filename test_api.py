"""
API test scripti - Örnek kullanım
"""
import requests
import base64
from PIL import Image
import io

# API URL
API_URL = "http://localhost:5000"

def test_health():
    """API sağlık kontrolü"""
    response = requests.get(f"{API_URL}/health")
    print("Health Check:", response.json())
    return response.json()

def test_predict_base64(image_path):
    """Base64 görüntü ile tahmin"""
    # Görüntüyü oku ve base64'e çevir
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    # API'ye gönder
    response = requests.post(
        f"{API_URL}/predict",
        json={'image': image_base64}
    )
    
    print("Predict (Base64):", response.json())
    return response.json()

def test_predict_file(image_path):
    """Dosya upload ile tahmin"""
    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            f"{API_URL}/predict/file",
            files=files
        )
    
    print("Predict (File):", response.json())
    return response.json()

if __name__ == '__main__':
    print("API Test Scripti")
    print("=" * 50)
    
    # Health check
    test_health()
    print()
    
    # Örnek görüntü ile test (data klasöründen bir görüntü)
    # test_predict_base64('data/a/0.jpg')
    # test_predict_file('data/a/0.jpg')
