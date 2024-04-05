from django.contrib import admin
from django.urls import path, include

from .views.fetch_files import FileListView

urlpatterns = [
    path('admin', admin.site.urls),
    path('api/files', FileListView.as_view()),
]
