from django.urls import path , include 
from .views.file_view import FileListView


urlpatterns = [
    path('files/', FileListView.as_view())
    
]
