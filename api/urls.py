from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusinessCardViewSet, SocialLinkViewSet, VisitStatsViewSet, register_user, login_user

router = DefaultRouter()
router.register(r'cards', BusinessCardViewSet, basename='cards')
router.register(r'social-links', SocialLinkViewSet, basename='social-links')
router.register(r'stats', VisitStatsViewSet, basename='stats')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
]