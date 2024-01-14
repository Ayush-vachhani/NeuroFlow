from django.urls import path
from ML_Trainer import views

urlpatterns = [
    path('', views.index, name='index'),
]
