from rest_framework import serializers
from .models import BusinessCard, SocialLink, VisitStats

class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ['platform', 'url']  # Убрали id, created_at

class BusinessCardSerializer(serializers.ModelSerializer):
    social_links = SocialLinkSerializer(many=True, required=False)
    avatar = serializers.ImageField(required=False)
    background_image = serializers.ImageField(required=False)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BusinessCard
        fields = [
            'id', 'user', 'slug', 'title', 'subtitle', 'description',
            'email', 'phone', 'avatar', 'background_image',
            'template_id', 'background_color', 'font_style',
            'social_links', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def create(self, validated_data):
        print("Validated data (create):", validated_data)
        social_links_data = validated_data.pop('social_links', [])
        card = BusinessCard.objects.create(**validated_data)
        for link_data in social_links_data:
            SocialLink.objects.create(card=card, **link_data)
        return card

    def update(self, instance, validated_data):
        print("Validated data (update):", validated_data)
        social_links_data = validated_data.pop('social_links', [])
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.subtitle = validated_data.get('subtitle', instance.subtitle)
        instance.description = validated_data.get('description', instance.description)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.background_image = validated_data.get('background_image', instance.background_image)
        instance.template_id = validated_data.get('template_id', instance.template_id)
        instance.background_color = validated_data.get('background_color', instance.background_color)
        instance.font_style = validated_data.get('font_style', instance.font_style)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()

        instance.social_links.all().delete()  # Удаляем старые ссылки
        for link_data in social_links_data:
            SocialLink.objects.create(card=instance, **link_data)
        return instance

class VisitStatsSerializer(serializers.ModelSerializer):
    card_title = serializers.CharField(source='card.title', read_only=True)

    class Meta:
        model = VisitStats
        fields = ['id', 'card', 'card_title', 'ip_address', 'visit_date']
        read_only_fields = ['id', 'ip_address', 'visit_date']