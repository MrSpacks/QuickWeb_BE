from rest_framework import serializers
from .models import BusinessCard, SocialLink, VisitStats

# Сериализатор для социальной ссылки
class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ['id', 'platform', 'url', 'created_at']
        read_only_fields = ['id', 'created_at']


# Сериализатор для визитки
class BusinessCardSerializer(serializers.ModelSerializer):
    social_links = SocialLinkSerializer(many=True, read_only=True)  # related_name='social_links' в модели
    avatar = serializers.ImageField(required=False)
    background_image = serializers.ImageField(required=False)
    user = serializers.StringRelatedField(read_only=True)  # показывает username

    class Meta:
        model = BusinessCard
        fields = [
            'id', 'user', 'slug', 'title', 'subtitle', 'description',
            'email', 'phone', 'avatar', 'background_image',
            'template_id', 'background_color', 'font_style',
            'social_links', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'slug', 'user', 'created_at', 'updated_at']


# Сериализатор для статистики посещений
class VisitStatsSerializer(serializers.ModelSerializer):
    card_title = serializers.CharField(source='card.title', read_only=True)  # опционально: отображение заголовка

    class Meta:
        model = VisitStats
        fields = ['id', 'card', 'card_title', 'ip_address', 'visit_date']
        read_only_fields = ['id', 'ip_address', 'visit_date']