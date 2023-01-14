from .views import *                                
from django.urls import path


app_name= 'orders'

urlpatterns = [
    path('order_create/', OrderCreateView.as_view(), name='order_create'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order_success/', SuccessOrderView.as_view(), name='order_success'),
    path('order_cancel/', CanceledOrderView.as_view(), name='order_cancel'),
    path('', OrderListView.as_view(), name='order_list'),
]
