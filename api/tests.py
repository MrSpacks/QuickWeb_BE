from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import BusinessCard

"""Тесты для API визиток"""
class APITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="123456")  # Создаем тестового пользователя
        self.card = BusinessCard.objects.create( 
            user=self.user,
            slug="bla-bla-card",
            title="Бла бла визитка",
            is_active=True,
        )

    def test_card_detail_found(self):  #  Тест на успешное получение детали карточки
        url = reverse("cards-detail", args=[self.card.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_card_detail_not_found(self): # Тест на случай, когда карточка не найдена
        url = reverse("cards-detail", args=["no-such-slug"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_register_user(self): # Тест на успешную регистрацию пользователя
        url = reverse("register")
        data = {"username": "sleepy", "email": "zzz@example.com", "password": "pass123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_missing_field(self): # Тест на регистрацию с отсутствующим полем
        url = reverse("register")
        response = self.client.post(url, {"username": "no_email"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_success(self): # Тест на успешный логин
        url = reverse("login")
        response = self.client.post(url, {"username": "testuser", "password": "123456"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user_invalid(self): # Тест на логин с неверными данными
        url = reverse("login")
        response = self.client.post(url, {"username": "testuser", "password": "wrong"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_business_cards(self): # Тест на получение списка карточек
        url = reverse("cards-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_business_card_requires_auth(self): # Тест на создание карточки без авторизации
        url = reverse("cards-list")
        data = {"slug": "another-card", "title": "Я устал, я мухожук"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_social_link_requires_auth(self): 
        url = reverse("social-links-list")
        data = {"card": self.card.id, "platform": "github", "url": "https://github.com/zzz"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

