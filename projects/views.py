from django.shortcuts import render
from .forms import ImageUploadForm
from .models import load_trained_model, predict_image, load_class_names
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from transformers import pipeline

model = load_trained_model()

def home(request):
    return render(request, 'projects_home.html')

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Formdan gelen dosyayı al
        image = request.FILES['image']

        # Görüntüyü kaydetmek için bir geçici dosya oluşturun
        with open('temp_image.jpg', 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)

        # Modeli kullanarak tahmin yapın
        prediction = predict_image(model, 'temp_image.jpg')

        # Tahmin sonucunu döndürün
        predicted_class = load_class_names(prediction)
        return render(request, 'result.html', {'prediction': predicted_class})

    # Eğer formda POST yapılmadıysa, boş formu göster
    form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})


# Alternatif yükleme ve tahmin işlevi
def leaf_disease(request):
    if request.method == "POST" and request.FILES.get('image'):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES['image']
            prediction = predict_image(model, image)
            predicted_class = load_class_names(prediction)
            return render(request, 'result.html', {'prediction': predicted_class})

    form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})

# Hugging Face sentiment analizi modeli
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased")

class SentimentAnalysisView(APIView):
    def post(self, request):
        # Giriş metnini al
        text = request.data.get('text')

        # Metin boşsa hata döndür
        if not text:
            return Response({"error": "Text is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Sentiment analizi yap
        result = sentiment_pipeline(text)[0]
        
        # Sonucu döndür
        return Response({
            "input_text": text,
            "sentiment": result['label'],
            "score": round(result['score'], 2)
        }, status=status.HTTP_200_OK)
