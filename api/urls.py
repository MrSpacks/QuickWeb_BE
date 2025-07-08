from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BusinessCardViewSet, SocialLinkViewSet, VisitStatsViewSet

router = DefaultRouter()
router.register(r'cards', BusinessCardViewSet)
router.register(r'social-links', SocialLinkViewSet)
router.register(r'stats', VisitStatsViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
