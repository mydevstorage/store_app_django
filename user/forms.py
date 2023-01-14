from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.forms import ValidationError
# from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError
# from captcha.fields import CaptchaField
from .models import *
from django.utils.timezone import now
import uuid
from datetime import timedelta
from .tasks import *

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control py-4",
                              'placeholder': "Введите имя пользователя"})) 		
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control py-4",
                              'placeholder': "Введите пароль"}))	

    class Meta:
        model = User  # Указывается с какой моделью связь
        fields = ['username', 'password']  # Поля с которыми будем работать


class UserRegisterForm(UserCreationForm): 
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control py-4",
                              'placeholder': "Введите имя"})) 	  
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control py-4",
                              'placeholder': "Введите фамилию"})) 	
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control py-4",
                              'placeholder': "Введите логин"})) 	      
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': "form-control py-4",
                              'placeholder': "Введите электронную почту"})) 	                
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control py-4",
                              'placeholder': "Введите пароль"})) 			
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control py-4",
                              'placeholder': "Введите подтверждение пароля"})) 	

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')  # Поля с коротымы работаем

    def save(self, commit=True):
        '''Переопределяем функцию сохранения при регистрации, добавляем новые операции'''
        user = super().save(commit)
        send_email_verification.delay(user.id)
        # expiration = now() + timedelta(hours=48)
        # record = EmailVerification.objects.create(code=uuid.uuid4(),user=user, expiration=expiration)
        # record.send_verification_email()
        return user

    def clean_email(self):   
        '''Кастомная валидация дубликатов почты'''
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise ValidationError('Такой адрес электронной почты уже зарегистрирован')
        return email


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control py-4"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control py-4"}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': "custom-file-input"}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control py-4", 'readonly': True}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': "form-control py-4", 'readonly': True}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'image', 'username', 'email']