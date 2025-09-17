# serializers.py

from rest_framework import serializers
from .models import BusinessCard, SocialLink, VisitStats
import json

class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ['platform', 'url']

class BusinessCardSerializer(serializers.ModelSerializer):
    social_links = SocialLinkSerializer(many=True, required=False)
    avatar = serializers.ImageField(required=False, allow_null=True)
    background_image = serializers.ImageField(required=False, allow_null=True)
    text_color = serializers.CharField(max_length=7, default='#000000')
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BusinessCard
        fields = [
            'id', 'user', 'slug', 'title', 'subtitle', 'description',
            'email', 'phone', 'avatar', 'background_image',
            'template_id', 'background_color', 'text_color', 'font_style',
            'social_links', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    # We can remove to_internal_value as it's not strictly necessary with this approach.

    def create(self, validated_data):
        print("DEBUG: Validated data в create:", validated_data)
        social_links_data = self.context['request'].data.get('social_links', '[]')
        try:
            social_links_list = json.loads(social_links_data)
        except json.JSONDecodeError:
            social_links_list = []

        # Remove social_links from validated_data to avoid conflicts
        validated_data.pop('social_links', None)

        card = BusinessCard.objects.create(**validated_data)
        
        for link_data in social_links_list:
            SocialLink.objects.create(card=card, **link_data)
        
        return card

    def update(self, instance, validated_data):
        print("DEBUG: Validated data в update:", validated_data)
        social_links_data = self.context['request'].data.get('social_links', '[]')
        try:
            social_links_list = json.loads(social_links_data)
        except json.JSONDecodeError:
            social_links_list = []

        # Remove social_links from validated_data
        validated_data.pop('social_links', None)
        
        # Update other fields of the card
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Delete old links and create new ones
        instance.social_links.all().delete()
        for link_data in social_links_list:
            SocialLink.objects.create(card=instance, **link_data)

        return instance
class VisitStatsSerializer(serializers.ModelSerializer):
    card_title = serializers.CharField(source='card.title', read_only=True)

    class Meta:
        model = VisitStats
        fields = ['id', 'card', 'card_title', 'ip_address', 'visit_date']
        read_only_fields = ['id', 'ip_address', 'visit_date']