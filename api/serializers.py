from rest_framework import serializers
from .models import BusinessCard, SocialLink, VisitStats

class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ['id', 'platform', 'url', 'created_at']
        read_only_fields = ['id', 'created_at']

class BusinessCardSerializer(serializers.ModelSerializer):
    social_links = SocialLinkSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BusinessCard
        fields = [
            'id', 'user', 'slug', 'title', 'subtitle', 'description',
            'email', 'phone', 'avatar', 'background_image', 'template_id',
            'background_color', 'font_style', 'created_at', 'updated_at',
            'is_active', 'social_links'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class VisitStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitStats
        fields = ['id', 'card', 'ip_address', 'visit_date']
        read_only_fields = ['id', 'card', 'ip_address', 'visit_date']