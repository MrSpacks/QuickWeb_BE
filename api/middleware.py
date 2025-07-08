from django.urls import resolve
from .models import BusinessCard, VisitStats

class VisitTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Проверяем, что запрос не к админке, API или статическим файлам
        if not request.path.startswith(('/admin/', '/api/', '/media/', '/static/')):
            slug = request.path.strip('/')
            try:
                card = BusinessCard.objects.get(slug=slug)
                VisitStats.objects.create(
                    card=card,
                    ip_address=request.META.get('REMOTE_ADDR')
                )
            except BusinessCard.DoesNotExist:
                pass
                
        return response