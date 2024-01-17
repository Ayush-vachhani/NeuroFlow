from django.urls import path
from ML_Trainer import views

urlpatterns = [
    path('csv_columns/', views.CSVColumnsView.as_view(), name='csv_columns'),
]
