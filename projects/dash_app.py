from dash import dcc, html, Input, Output
from django_plotly_dash import DjangoDash
import numpy as np
import cv2
import io
from PIL import Image
import tensorflow as tf
#from keras.models import load_model
import pickle
import base64

# Dash uygulaması Django'da çalışacak şekilde tanımlandı
app = DjangoDash('PlantDiseasePrediction')  # Dash uygulamanız için bir isim verin

model = tf.keras.models.load_model("model_1.h5")
with open("class_name.pkl", "rb") as file:
    class_names = pickle.load(file)

app.layout = html.Div([
    html.H1("Bitki Hastalığı Tahmini Uygulaması"),
    dcc.Upload(
        id="upload-image",
        children=html.Div(["Bir yaprak görüntüsü yüklemek için tıklayın"]),
        style={
            "width": "100%",
            "height": "60px",
            "lineHeight": "60px",
            "borderWidth": "1px",
            "borderStyle": "dashed",
            "borderRadius": "5px",
            "textAlign": "center",
            "margin": "10px"
        },
        multiple=False
    ),
    html.Div(id="output-image"),
    html.Div(id="prediction-output")
])

# Görüntü yükleme işlevi
def preprocess_image(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    image = Image.open(io.BytesIO(decoded))
    img_array = np.array(image)
    img_resized = cv2.resize(img_array, (224, 224))  # Modele uygun boyut
    img_resized = img_resized / 255.0  # Normalizasyon
    img_reshaped = np.expand_dims(img_resized, axis=0)
    return img_reshaped

# Callback
@app.callback(
    [Output("output-image", "children"), Output("prediction-output", "children")],
    [Input("upload-image", "contents")]
)
def update_output(contents):
    if contents is not None:
        img_array = preprocess_image(contents)
        prediction = model.predict(img_array)
        pred_index = np.argmax(prediction)

        output_image = html.Img(src=contents, style={"width": "300px", "margin": "10px"})

        if pred_index < len(class_names):
            prediction_text = f"Tahmin Edilen Sınıf: {class_names[pred_index]}"
        
        probabilities_text = [
            html.P(f"{class_names[i]}: %{prob * 100:.2f}")
            for i, prob in enumerate(prediction[0])
        ]

        return output_image, [html.H3(prediction_text)] + probabilities_text
    return None, None
