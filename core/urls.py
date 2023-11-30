from core.views import analyze_folder, document_classification
from django.urls import path

urlpatterns = [
    path('', analyze_folder, name='analyze_folder'),
    path('classify', document_classification, name='document_classification'),
]
