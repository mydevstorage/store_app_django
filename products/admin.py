from django.contrib import admin
from .models import *


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    # Отображение общее
    list_display = ('name', 'price', 'quantity', 'category')
    ''' Поля стали лучше, в редактировании. Можно в одну стоку
       Можно менять порядок полей'''
    fields = ('name', 'discription', ('price', 'quantity'),
              'image', 'strip_id', 'category')
    ordering = ('name',)
    search_fields = ('name',)

@admin.register(ProductsCategory)
class ProductsCategoryadmin(admin.ModelAdmin):
    list_display = ('namme', 'id')
    fields = ('namme', 'id')



class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    # Eсли поле не редактируется изначально, то нужно поставить ридонли, иначе ошибка
    readonly_fields = ('created_timestamp',)
    extra = 0
