from .views import *                                
from django.urls import path
# from django.views.decorators.cache import cache_page

app_name= 'products'
urlpatterns = [
    # path('', cache_page(15)(ProductsListView.as_view()), name='index'),
    path('', ProductsListView.as_view(), name='index'),
    # контроллер будет тот же, просто в него добавим условие проверки
    path('category/<int:category_id>', ProductsListView.as_view(), name='category'),
    # #
    path('page/<int:page>', ProductsListView.as_view(), name='paginator'),
    # int прописывается так же как и в контроллеле параметр функции и в шаблоне его передаем 
    path('basket/add/<int:product_id>/', basket_add, name='basket_add'),
    path('basket/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]
