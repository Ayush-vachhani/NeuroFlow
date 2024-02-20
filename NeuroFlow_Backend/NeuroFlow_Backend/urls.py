from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ML_Trainer.urls'), name='ML_Trainer'),
]
