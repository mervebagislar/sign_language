from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import cv2
import mediapipe as mp
import numpy as np
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)
CORS(app)  # CORS desteği için

# Model ve MediaPipe yükleme
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)


def process_image(image_data):
    """Görüntüyü işleyip tahmin yapar"""
    try:
        # Base64 string'den görüntüyü decode et
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        
        # PIL Image'ı OpenCV formatına çevir
        img_array = np.array(image)
        if len(img_array.shape) == 3:
            img_rgb = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        else:
            img_rgb = img_array
        
        # RGB'ye çevir (MediaPipe RGB bekliyor)
        img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)
        
        # El landmark'larını çıkar
        results = hands.process(img_rgb)
        
        if not results.multi_hand_landmarks:
            return None, "El tespit edilemedi"
        
        # Sadece ilk eli kullan
        hand_landmarks = results.multi_hand_landmarks[0]
        
        data_aux = []
        x_ = []
        y_ = []
        
        for i in range(len(hand_landmarks.landmark)):
            x = hand_landmarks.landmark[i].x
            y = hand_landmarks.landmark[i].y
            
            x_.append(x)
            y_.append(y)
        
        for i in range(len(hand_landmarks.landmark)):
            x = hand_landmarks.landmark[i].x
            y = hand_landmarks.landmark[i].y
            data_aux.append(x - min(x_))
            data_aux.append(y - min(y_))
        
        # Sadece 42 uzunluğunda veri varsa tahmin yap
        if len(data_aux) != 42:
            return None, f"Geçersiz veri uzunluğu: {len(data_aux)} (beklenen: 42)"
        
        # Tahmin yap
        prediction = model.predict([np.asarray(data_aux)])
        predicted_character = prediction[0].upper()
        
        # Olasılık skorları (eğer varsa)
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba([np.asarray(data_aux)])[0]
            classes = model.classes_
            confidence = max(probabilities)
        else:
            confidence = 1.0
            classes = []
        
        return {
            'prediction': predicted_character,
            'confidence': float(confidence),
            'all_probabilities': {str(cls): float(prob) for cls, prob in zip(classes, probabilities)} if hasattr(model, 'predict_proba') else {}
        }, None
        
    except Exception as e:
        return None, str(e)


@app.route('/health', methods=['GET'])
def health():
    """API sağlık kontrolü"""
    return jsonify({
        'status': 'healthy',
        'message': 'Sign Language Detector API is running'
    })


@app.route('/status', methods=['GET'])
def status():
    """API durum kontrolü (Flutter uyumluluğu için)"""
    return jsonify({
        'status': 'ok',
        'message': 'Sign Language Detector API is running'
    })


@app.route('/predict', methods=['POST'])
def predict():
    """Görüntüden işaret dili harfini tahmin eder"""
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({
                'error': 'Görüntü verisi bulunamadı. "image" alanında base64 encoded görüntü gönderin.'
            }), 400
        
        image_data = data['image']
        result, error = process_image(image_data)
        
        if error:
            return jsonify({
                'error': error
            }), 400
        
        # Flutter uyumluluğu için direkt prediction ve confidence döndür
        return jsonify({
            'success': True,
            'prediction': result['prediction'],
            'confidence': result['confidence'],
            'all_probabilities': result.get('all_probabilities', {}),
            'result': result  # Geriye uyumluluk için
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'İşlem sırasında hata oluştu: {str(e)}'
        }), 500


@app.route('/predict/file', methods=['POST'])
def predict_file():
    """Dosya upload ile tahmin yapar"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'error': 'Dosya bulunamadı. "file" adında bir dosya gönderin.'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'error': 'Dosya seçilmedi'
            }), 400
        
        # Dosyayı oku
        file_bytes = file.read()
        image = Image.open(BytesIO(file_bytes))
        
        # PIL Image'ı base64'e çevir
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        result, error = process_image(img_base64)
        
        if error:
            return jsonify({
                'error': error
            }), 400
        
        # Flutter uyumluluğu için direkt prediction ve confidence döndür
        return jsonify({
            'success': True,
            'prediction': result['prediction'],
            'confidence': result['confidence'],
            'all_probabilities': result.get('all_probabilities', {}),
            'result': result  # Geriye uyumluluk için
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'İşlem sırasında hata oluştu: {str(e)}'
        }), 500


if __name__ == '__main__':
    print("Sign Language Detector API başlatılıyor...")
    print("API endpoint'leri:")
    print("  GET  /health - API sağlık kontrolü")
    print("  POST /predict - Base64 görüntü ile tahmin")
    print("  POST /predict/file - Dosya upload ile tahmin")
    app.run(host='0.0.0.0', port=5000, debug=True)
