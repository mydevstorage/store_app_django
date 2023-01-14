from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from django.utils.timezone import now
from datetime import timedelta



from user.models import *

class UserRegisterViewTest(TestCase):

    def setUp(self):
        self.path = reverse('user:register')

        self.data = {
            'first_name': 'Джеки',
            'last_name': 'Чан',
            'username': 'djeky_chan',
            'email': 'dj@mail.com',
            'password1': '12345678Jj',
            'password2': '12345678Jj',
        }

    def test_user_register_get(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed(response, "user/register.html")

    def test_user_register_post_success(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)

        # check creating of user
        self.assertTrue(User.objects.filter(username=username).exists())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('user:login'))

        # checking of email sending
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )
            
    def test_register_error_message(self):
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # Ищет точное совпадение
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)


