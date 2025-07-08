from django.contrib import admin
from django.contrib import admin
from django.db.models import Count
from .models import BusinessCard, SocialLink, VisitStats
from datetime import timedelta
from django.utils import timezone

@admin.register(BusinessCard)
class BusinessCardAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'monthly_unique_visits')

    def monthly_unique_visits(self, obj):
        one_month_ago = timezone.now() - timedelta(days=30)
        return VisitStats.objects.filter(
            card=obj, visit_date__gte=one_month_ago
        ).values('ip_address').distinct().count()
    monthly_unique_visits.short_description = "Unique IPs this month"