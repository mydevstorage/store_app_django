from products.models import Basket
from django.urls import reverse_lazy
from django.shortcuts import render, redirect  # HttpResponseRedirect
from .forms import *
from django.contrib import auth, messages
from django.db.models import *
# from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from common.utils import TitleMixin
from django.views.generic.base import TemplateView

class UserLoginView(TitleMixin, LoginView):
    # model =  стоит по автомату User
    template_name = 'user/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизация'
    
 
    # def get_success_url(self):
    #     '''Но можно в настройка прописать LOGIN_REDIRECT_URL = "/" '''
    #     return reverse_lazy('index')

# def login(request):    # Потренироваться переписать все это через классы, тут слишком много логики
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 return redirect('index')      # Можно слелать просто редирект а не усложнять  HttpResponseRedirect(reverse)
#     else:
#         form = UserLoginForm()

#     context = {
#         'form': form,
#     }
#     return render(request, 'user/login.html', context)


class UserCreateView(TitleMixin, SuccessMessageMixin, CreateView):
    title = 'Store - Регистрация'
    model = User
    form_class = UserRegisterForm
    template_name = "user/register.html"
    success_url = reverse_lazy('user:login')
    success_message = 'Регистрация прошла успешно!'
    


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Регистрация прошла успешно!')
#             return redirect('user:login')
#     else:
#         form = UserRegisterForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'user/register.html', context)

class ProfileUpdateView(TitleMixin, LoginRequiredMixin, UpdateView):
    '''Добавлен спец миксик, первым в очереди'''
    model = User
    form_class = UserProfileForm
    template_name = "user/profile.html"
    title = 'Store - Личный кабинет'
    
    # Закоментим тк сделали контекст процессор
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # self Содержит в себе еще и request, можно  еще self.object
    #     context['basket'] = Basket.objects.filter(user=self.request.user)
    #     return context

    def get_success_url(self) -> str:
        '''Это для того чтобы передать тот самый id  в маршрут иначе можно просто success_url'''
        return reverse_lazy('user:profile', args=(self.object.id,)) # Кортеж


# @login_required()
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('user:profile')
#     else:
#         form = UserProfileForm(instance=request.user) 

#     basket = Basket.objects.filter(user=request.user)
#     # Ниже решение в лоб простого суммирования
#     # total_sum = sum(item.sum() for item in basket)
#     # total_quantity = sum(item.quantity for item in basket)

#     context = {
#         'title': 'Store - profile',
#         'form': form,
#         'basket': Basket.objects.filter(user=request.user),
#         # 'total_quantity': total_quantity,
#         # 'total_sum': total_sum,
#     }
#     return render(request, 'user/profile.html', context)

def logout(request):
    '''Вместо этой функции можно в маршрутах просто прописать класс LogoutView.as_view()
       предварительно сделав импорь
       И в настройка LOGOUT_REDIRECT_URL = "/"'''
    auth.logout(request)
    return redirect('index')

class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - Подтверждение электронной почты'
    template_name = 'user/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super().get(request, *args, **kwargs)
        else:
            return redirect('index')


