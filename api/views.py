from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import BusinessCard, SocialLink, VisitStats
from .serializers import BusinessCardSerializer, SocialLinkSerializer, VisitStatsSerializer

class BusinessCardViewSet(ModelViewSet):
    queryset = BusinessCard.objects.all()
    serializer_class = BusinessCardSerializer

    def get_permissions(self):
        if self.action in ['list', 'create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]  # Публичный доступ для retrieve

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user)
        return self.queryset

class SocialLinkViewSet(ModelViewSet):
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(card__user=self.request.user)

class VisitStatsViewSet(ModelViewSet):
    queryset = VisitStats.objects.all()
    serializer_class = VisitStatsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(card__user=self.request.user)