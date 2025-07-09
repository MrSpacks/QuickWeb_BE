from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),
    # API (для DRF)
    path('api/', include('api.urls')),  # Подключаем urls.py приложения
    # Публичные визитки
    path('<slug:slug>/', include('api.urls')),  # Для визиток вида example.com/cardname
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Для медиафайлов