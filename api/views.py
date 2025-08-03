from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import BusinessCard, SocialLink, VisitStats
from .serializers import BusinessCardSerializer, SocialLinkSerializer, VisitStatsSerializer
from rest_framework import viewsets


@api_view(['GET'])
@permission_classes([AllowAny])
def card_detail(request, slug):
    try:
        card = BusinessCard.objects.get(slug=slug, is_active=True)
    except BusinessCard.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BusinessCardSerializer(card)
    return Response(serializer.data)
class BusinessCardViewSet(viewsets.ModelViewSet):
    queryset = BusinessCard.objects.all()
    serializer_class = BusinessCardSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user)
        return self.queryset.filter(is_active=True)

    def perform_create(self, serializer):
        print("perform_create called with data:", self.request.data)
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        print("perform_update called with data:", self.request.data)
        serializer.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        print("Retrieve response:", serializer.data)  # Отладка
        return Response(serializer.data)
        
    queryset = BusinessCard.objects.all()
    serializer_class = BusinessCardSerializer
    lookup_field = 'slug'
    def get_permissions(self):
        if self.action in ['retrieve', 'list']:  # Публичный доступ для retrieve и list
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user)
        return self.queryset.filter(is_active=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SocialLinkViewSet(viewsets.ModelViewSet):
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

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not all([username, email, password]):
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)