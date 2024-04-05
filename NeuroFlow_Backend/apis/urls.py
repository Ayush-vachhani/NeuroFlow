from django.urls import path
from .views.file_view import FileListView

urlpatterns = [
    path('files/', FileListView.as_view())
]
