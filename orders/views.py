from http import HTTPStatus
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from .forms import OrderForm
from common.utils import TitleMixin
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from products.models import Basket
from orders.models import *
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

stripe.api_key = settings.STRIPE_SECRET_KEY 


class SuccessOrderView(TitleMixin, TemplateView):
    template_name = "orders/success.html"
    title = 'Store - Спасибо за заказ!'


class CanceledOrderView(TemplateView):
    template_name = "orders/cancel.html"


class OrderListView(TitleMixin, ListView):
    '''queryset = Order.objects.all() прописать обязательно'''
    template_name = "orders/orders.html"
    title = 'Store - Заказы'
    queryset = Order.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(initiator=self.request.user)
    

class OrderDetailView(DetailView):
    '''Отобразит автоматически из БД по pk  необходимый заказ'''
    model = Order
    template_name = "orders/order.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Обязательно в этом классе object, без s
        context["title"] = f'Store - Заказ # {self.object.id}'
        return context
    


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'Store - Оформление заказа'

    def post(self, request, *args: str, **kwargs):
        '''Попробовать вынести логику корзины из контроллера'''
        basket = Basket.objects.filter(user=self.request.user)

        line_items = []
        for item in basket:
            unit = {
                'price': item.product.strip_id,
                'quantity': item.quantity,
            }
            line_items.append(unit)
        super().post(request, *args, **kwargs)
        checkout_session = stripe.checkout.Session.create(
        line_items= line_items,
        # Важное добавление.. object это как instance .. объект в которым работаем
        metadata = {'order_id': self.object.id},
        mode='payment',
        success_url='{}{}'.format(settings.DOMAIN_NAME,
                    reverse('orders:order_success')),
        cancel_url='{}{}'.format(settings.DOMAIN_NAME,
                    reverse('orders:order_cancel')),
        )

        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)


    def form_valid(self, form):
        '''При валидации добавляем еще одно обязательное поле initiator'''
        ''' instance -  это мы берем из формы сам объект, без этого не работает'''
        form.instance.initiator = self.request.user
        return super().form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
    # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
    # Invalid signature
        return HttpResponse(status=400)

  # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = stripe.checkout.Session.retrieve(
        event['data']['object']['id'],
        expand=['line_items'],
        )       

    # line_items = session.line_items
    # Fulfill the purchase...
        fulfill_order(session)

  # Passed signature verification
    return HttpResponse(status=200)

def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()