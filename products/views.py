from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from common.utils import TitleMixin
from django.core.cache import cache
from products.models import *


# Всегда в конце ставить View, для других разработчиков
class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'

# def index(request):
#     context = {
#         'title': 'Главная страница'
#     }
#     return render(request, 'products/index.html', context)

class ProductsListView(TitleMixin, ListView):
    model = Products   # По умолчания выбирает все записи из БД
    template_name = "products/products.html"
    context_object_name = 'products'  # Стандарное имя object_list
    paginate_by = 6
    title = 'Store - Каталог'

    def get_context_data(self, **kwargs):
        ''' For traning cached categories'''        
        context = super().get_context_data(**kwargs)
        categories = cache.get('categories')   
        # cache categories
        if not categories:
            context["categories"] = ProductsCategory.objects.all()
            cache.set('categories', context["categories"], 15) 
        else:
            context["categories"] = categories
        return context
    
    def get_queryset(self): # Изначально этот метод выбирает все записи 
        queryset = super().get_queryset()
        # Это все что передается в url как параметр, slag или int/ хранится в self.kwargs
        category_id = self.kwargs.get('category_id')  # Метод get не возвратит ошибку, если придет None
        return queryset.filter(category__pk=category_id) if category_id else queryset
    
    
# def products(request, category_id=None, page_number=1): # Это значит не всегда передается второй агрумент
  
#     if category_id:
#         # Мой эксперементальный запрос  и он верный, выбираем сначала
#         # поле, которое форейн ки, и потом поле в соединенной таблице
#         products = Products.objects.filter(category__pk=category_id)
#     else:
#         products = Products.objects.all()

#     per_page = 1 # Количество товаров на странице
#     paginator = Paginator(products, per_page)
#     products_paginator = paginator.page(page_number)
#     context = {
#     'title': 'Store',
#     'categories': ProductsCategory.objects.all(),
#     'products': products_paginator,
#     }
        
#     return render(request, 'products/products.html', context)
    

@login_required()
def basket_add(request, product_id):
    Basket.create_or_update(product_id, request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required()
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
