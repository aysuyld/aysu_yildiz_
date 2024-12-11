from django.db import models
import tensorflow as tf
#from keras import load_model
import numpy as np
from PIL import Image
import pickle

def load_trained_model():
    # Modelinizi yükleyin
    model = tf.keras.models.load_model('model_1.h5')
    return model

def load_class_names(predict):

    with open('class_name.pkl', 'rb') as file:
        class_names = pickle.load(file)
    predicted_class_index = np.argmax(predict)
    return class_names[predicted_class_index]


def predict_image(model, image_path):
    # Görüntüyü yükleyin ve modelinize uygun hale getirin
    image = Image.open(image_path)
    image = image.resize((224, 224))  # Modelin beklediği boyutları ayarlayın
    image_array = np.array(image)
    image_array = image_array / 255.0  # Normalizasyon
    image_array = np.expand_dims(image_array, axis=0)

    # Tahmin yapın
    prediction = model.predict(image_array)
    return prediction
