import os

import cv2


DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Türkçe alfabedeki tüm harfler için sınıflar
classes = ['a', 'b', 'c','ç', 'd', 'e', 'f', 'g', 'ğ', 'h', 'ı', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'ö', 'p', 'r', 's', 'ş', 't', 'u', 'ü', 'v', 'y', 'z']
dataset_size = 100

cap = cv2.VideoCapture(0)

for class_name in classes:
    class_dir = os.path.join(DATA_DIR, class_name)
    if not os.path.exists(class_dir):
        os.makedirs(class_dir)

    print('Collecting data for class: {}'.format(class_name))
    print('Press "Q" when ready to start collecting images...')

    # Hazırlık ekranı
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.putText(frame, 'Ready? Press "Q" to start!', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                    cv2.LINE_AA)
        cv2.putText(frame, 'Class: {}'.format(class_name), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2,
                    cv2.LINE_AA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(25) == ord('q'):
            break

    # Görüntü toplama
    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()
        if not ret:
            break
        
        # İlerleme bilgisi göster
        cv2.putText(frame, 'Collecting: {}/{}'.format(counter, dataset_size), (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, 'Class: {}'.format(class_name), (50, 100), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        cv2.waitKey(25)
        
        img_path = os.path.join(class_dir, '{}.jpg'.format(counter))
        cv2.imwrite(img_path, frame)
        
        counter += 1
    
    print('Completed collecting {} images for class: {}'.format(counter, class_name))
    print('-' * 50)

cap.release()
cv2.destroyAllWindows()
print('Data collection completed!')
print('Total classes: {}'.format(len(classes)))
print('Total images collected: {}'.format(len(classes) * dataset_size))
