from rest_framework import serializers
from .models import *
from django.db.models import fields


class ProductsSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='namme',
                           queryset = ProductsCategory.objects.all())
    class Meta:
        model = Products
        fields = ('id', 'name', 'discription', 'price', 'quantity',
                  'image', 'category',)


class BasketSerializer(serializers.ModelSerializer):
    product = ProductsSerializer()
    sum = fields.DecimalField()                                                       
    total_sum = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ('id', 'product', 'quantity', 'sum', 'created_timestamp',
                  'total_quantity', 'total_sum')
        read_only_fields = ('created_timestamp',)
      

    def get_total_sum(self, obj):
        return Basket.objects.filter(user__id=obj.user.id).total_sum()

    def get_total_quantity(self, obj):
        return Basket.objects.filter(user__id=obj.user.id).total_quantity() 
    