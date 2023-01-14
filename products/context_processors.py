from products.models import Basket

def basket(request):
    user = request.user
    return {'basket': Basket.objects.filter(user=user) if user.is_authenticated else []}