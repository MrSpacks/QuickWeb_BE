from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Модель для визитки
class BusinessCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    background_image = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    template_id = models.CharField(max_length=50)
    background_color = models.CharField(max_length=7, default='#FFFFFF')
    font_style = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Business Card"
        verbose_name_plural = "Business Cards"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title or f"card-{self.user.username}")
            slug = base_slug
            counter = 1
            while BusinessCard.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.user.username})"

# Модель для социальных сетей
class SocialLink(models.Model):
    card = models.ForeignKey(BusinessCard, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=50)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"

    def __str__(self):
        return f"{self.platform} - {self.card}"

# Модель для статистики посещений
class VisitStats(models.Model):
    card = models.ForeignKey(BusinessCard, on_delete=models.CASCADE, related_name='visits')
    ip_address = models.GenericIPAddressField()
    visit_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Visit Stat"
        verbose_name_plural = "Visit Stats"
        unique_together = ('card', 'ip_address', 'visit_date')

    def __str__(self):
        return f"Visit to {self.card} from {self.ip_address} at {self.visit_date}"