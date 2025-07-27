from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api.views import card_detail  # Импортируем card_detail напрямую

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Для API
    path('<slug:slug>/', card_detail, name='card_detail'),  # Публичные визитки
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)