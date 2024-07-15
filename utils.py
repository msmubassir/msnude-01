import os
from PIL import Image
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

def save_image(image, label, upload_folder):
    label_folder = 'unlabeled' if label is None else label
    folder_path = os.path.join(upload_folder, label_folder)
    os.makedirs(folder_path, exist_ok=True)
    filepath = os.path.join(folder_path, image.filename)
    image.save(filepath)
    return filepath

def load_data(upload_folder):
    data = []
    labels = []
    for label in ['nude', 'not_nude']:
        folder_path = os.path.join(upload_folder, label)
        for filename in os.listdir(folder_path):
            img_path = os.path.join(folder_path, filename)
            img = Image.open(img_path).resize((128, 128))
            img_array = np.array(img)
            data.append(img_array)
            labels.append(0 if label == 'nude' else 1)
    return np.array(data), np.array(labels)

def train_model(upload_folder):
    data, labels = load_data(upload_folder)
    x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2)
    
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=10, validation_data=(x_test, y_test))
    
    model.save('model/nudity_detector_model.h5')

def predict_image(image_path):
    model = load_model('model/nudity_detector_model.h5')
    img = Image.open(image_path).resize((128, 128))
    img_array = np.array(img).reshape(1, 128, 128, 3)
    prediction = model.predict(img_array)
    return 'nude' if prediction[0] < 0.5 else 'not_nude'
