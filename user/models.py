from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils.timezone import now
from django.template.loader import get_template
# from django.shortcuts import render

class User(AbstractUser):             
    '''При переопределении в настройках нужно прописать это обязательно'''
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True) # Уникальный id для пользователя
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()  # срок годности ссылки для верификации

    def __str__(self) -> str:
        return f'EmailVerification for {self.user.email}'

    def send_verification_email(self):
        link = reverse('user:email_verification', kwargs={'email': self.user.email,
                                                          'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учетной записи для {self.user.username}'
        # message = "Для подтвердждения учетной записи для {} перейдите по ссылке {}".format(
        #     self.user.username,
        #     verification_link
        # )
        
        send_mail(
        subject=subject, message='',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[self.user.email],
        fail_silently=False,
        html_message=get_template('emails/email_verify.html')
        .render({'link': verification_link, 'username': self.user.username})
        )

    def is_expired(self):
        return True if now() >= self.expiration else False