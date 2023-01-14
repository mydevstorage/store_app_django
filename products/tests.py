from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

from products.models import *
# from os import environ
# from django import setup

# environ.setdefault(
#     'DJANGO_SETTINGS_MODULE', 'main.settings'
# )
# setup()


class IndexViewTest(TestCase):
    '''Каждый метод должен называться с test_'''

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')
    
class ProductsListViewTest(TestCase):
    '''Одинаковые проверки можно вынести в приватный метод _method
       и одинаковые переменные можно вынести в setUp метод'''

    fixtures = ['cat.json', 'goods.json'] # Загружаем фикстуры для тестовой БД

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)
        products = Products.objects.all()[:2]
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')
        # Проверка, что выводится именно две карточки
        self.assertEqual(list(response.context_data['products']), list(products))
    
    def test_category_list_(self):
        category = ProductsCategory.objects.first()
        path = reverse('products:category', args=[category.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(
            list(response.context_data['products']),
            list(Products.objects.filter(category__id=category.id))
            )