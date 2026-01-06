import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np


data_dict = pickle.load(open('./data.pickle', 'rb'))

# Sadece 42 uzunluğundaki verileri kullan (tek el için)
data_filtered = []
labels_filtered = []
for i, d in enumerate(data_dict['data']):
    if len(d) == 42:  # Tek el: 21 landmark * 2 (x, y) = 42
        data_filtered.append(d)
        labels_filtered.append(data_dict['labels'][i])

data = np.asarray(data_filtered)
labels = np.asarray(labels_filtered)

print(f'Using {len(data)} samples out of {len(data_dict["data"])} total samples')

x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

model = RandomForestClassifier()

model.fit(x_train, y_train)

y_predict = model.predict(x_test)

score = accuracy_score(y_predict, y_test)

print('{}% of samples were classified correctly !'.format(score * 100))

f = open('model.p', 'wb')
pickle.dump({'model': model}, f)
f.close()
