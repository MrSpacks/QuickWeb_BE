from rest_framework import serializers
from .models import BusinessCard, SocialLink, VisitStats
import json

class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ['platform', 'url']  # Убрали id

class BusinessCardSerializer(serializers.ModelSerializer):
    social_links = SocialLinkSerializer(many=True, required=False)
    avatar = serializers.ImageField(required=False, allow_null=True)
    background_image = serializers.ImageField(required=False, allow_null=True)
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

    def to_internal_value(self, data):
        # Создаём изменяемую копию QueryDict
        mutable_data = data.copy() if hasattr(data, 'copy') else data
        # Парсим social_links из строки в список
        if 'social_links' in mutable_data and isinstance(mutable_data['social_links'], str):
            try:
                mutable_data['social_links'] = json.loads(mutable_data['social_links'])
            except json.JSONDecodeError:
                raise serializers.ValidationError({'social_links': 'Invalid JSON format'})
        return super().to_internal_value(mutable_data)

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
        # Обновление полей карточки
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Удаляем старые ссылки и добавляем новые
        instance.social_links.all().delete()
        for link_data in social_links_data:
            SocialLink.objects.create(card=instance, **link_data)
        return instance

class VisitStatsSerializer(serializers.ModelSerializer):
    card_title = serializers.CharField(source='card.title', read_only=True)

    class Meta:
        model = VisitStats
        fields = ['id', 'card', 'card_title', 'ip_address', 'visit_date']
        read_only_fields = ['id', 'ip_address', 'visit_date']