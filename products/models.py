from user.models import User
from django.db import models
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY 


class ProductsCategory(models.Model):
    namme = models.CharField(max_length=150, unique=True)
    discription = models.TextField(null=True, blank=True)

    def __str__(self): 
        return self.namme

    class Meta:
        # Это в админке буду названия адекватные
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['id']

class Products(models.Model):
    name = models.CharField(max_length=255)
    # Поле не обязательное для заполнения, если пустые скобки
    discription = models.TextField() 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images', blank=True)
    category = models.ForeignKey('ProductsCategory', on_delete=models.CASCADE)
    strip_id = models.CharField(max_length=128, blank=True)

    def __str__(self): 
        return f'Продукт: {self.name} | Категория: {self.category.namme}'

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['id']

    def save(self, force_insert=False , force_update=False, using= None, update_fields=None):
        if not self.strip_id:
            stripe_product_price = self.create_stripe_price()
            self.strip_id = stripe_product_price['id']
        return super().save(force_insert, force_update, using, update_fields)

    def create_stripe_price(self):
        '''Эти строки из документации API strip'''
        stripe_product = stripe.Product.create(name=self.name)
        stripe_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price * 100),
            currency='rub',
        )
        return stripe_price

class BasketQuerySet(models.QuerySet):
    '''Создали нужные нам методы, которые имеют доступ в шаблоне,
       к списку переданному через контекст, вне цикла'''
    # Как бы расширили менеджер объектов objects #
    def total_sum(self):
        return sum(item.sum() for item in self)

    def total_quantity(self):
        return sum(item.quantity for item in self)


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    # Добавляется время после создания, автоматически
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def sum(self):
        return self.product.price * self.quantity

    def __str__(self) -> str:
        return f'Корзина для {self.user.email} | Продукт: {self.product.name}'

    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum())
        }
        return basket_item

    @classmethod
    def create_or_update(cls, product_id, user):
        '''Basket.create_or_update > OK!'''
        basket_item = Basket.objects.filter(user=user, product_id=product_id)
        if not basket_item.exists():
            obj = Basket.objects.create(user=user, product_id=product_id, quantity=1)
            is_created = True
            return obj, is_created
        else:
            is_created = False
            basket = basket_item.first()
            basket.quantity += 1
            basket.save()
            return basket, is_created


