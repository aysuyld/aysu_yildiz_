from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home),
    path('prediction', views.upload_image),
    path('leaf_disease', views.leaf_disease, name='upload_image'),
    path('text_analysis', views.SentimentAnalysisView.as_view(), name='analyze_sentiment')
]