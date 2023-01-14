from django.db import models
from products.models import Basket
from user.models import User                                                                                                    

class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2 
    DELIVERED = 3
    STATUSES = ((CREATED, 'Создан'),
                (PAID, 'Оплачен'),
                (ON_WAY, 'В пути'),
                (DELIVERED, 'Доставлен')
                 )
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)
     
    def __str__(self):
         return f'Order #{self.id}. {self.first_name} {self.last_name}'
         

    def update_after_payment(self):
        basket = Basket.objects.filter(user=self.initiator)
        self.status = self.PAID
        self.basket_history = {
            'purchased_items': [item.de_json() for item in basket],
            'total_sum': float(basket.total_sum())
        }
        basket.delete()
        self.save()

    def get_status_diplay(self):
        stat_dict = {0: 'Создан', 1:'Оплачен', 2: 'В пути', 3: 'Доставлен'}
        return stat_dict[self.status]
     

