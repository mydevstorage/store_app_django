from .views import *                                
from django.urls import path, include
# from django.views.decorators.cache import cache_page
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'products', ProductsViewSet)
router.register(r'basket', BasketViewSet)

app_name= 'api'
urlpatterns = [
    path('', include(router.urls)),
    path('', include(router.urls)),
]