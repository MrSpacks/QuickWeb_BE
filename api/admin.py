from django.contrib import admin
from .models import BusinessCard, SocialLink, VisitStats

@admin.register(BusinessCard)
class BusinessCardAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'slug', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'slug', 'user__username')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(user=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not change:  # При создании новой визитки
            obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'card', 'url')
    search_fields = ('platform', 'url')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(card__user=request.user)
        return qs

@admin.register(VisitStats)
class VisitStatsAdmin(admin.ModelAdmin):
    list_display = ('card', 'ip_address', 'visit_date')
    list_filter = ('visit_date',)
    search_fields = ('ip_address', 'card__title')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(card__user=request.user)
        return qs