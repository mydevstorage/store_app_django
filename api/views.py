# from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from products.models import Products
from products.serializers import *
from rest_framework.permissions  import IsAuthenticated, IsAdminUser
from products.models import Basket
from rest_framework import status
from rest_framework.response import Response

class ProductsViewSet(ModelViewSet):
    '''Use all requests: GET, PUT, UPDATE, DELETE'''
    queryset = Products.objects.all() 
    serializer_class = ProductsSerializer
    
    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()

class BasketViewSet(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            product_id = request.data['product_id']
            products = Products.objects.filter(id=product_id)
            if not products.exists():
                return Response({'product_id':'There is no such product, try again'},
                                status=status.HTTP_400_BAD_REQUEST)
            obj, is_created = Basket.create_or_update(product_id, request.user)
            serializer = self.get_serializer(obj)
            return Response(serializer.data,
                status.HTTP_201_CREATED if is_created else status.HTTP_200_OK)
        except KeyError:
            return Response({'product_id':'This field is required!!!'},
                                status=status.HTTP_400_BAD_REQUEST)



       


