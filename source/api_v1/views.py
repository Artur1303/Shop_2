from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS, IsAdminUser

from api_v1.serializers import ProductSerializer, OrderSerializer
from webapp.models import Product, Order, OrderProduct, Cart


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return super().get_permissions()


class OrderApi(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request,*args,**kwargs):
        print(request)
        object = get_object_or_404(Order, pk=kwargs.get('pk'))
        slr = OrderSerializer(object)
        return Response(slr.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        object = Order.objects.create(name=data['name'], address=data['address'], phone=data['phone'])
        cart_ids = self.request.session.get('cart_ids', [])
        for i in data['order_products']:
            order_product = OrderProduct.objects.create(product_id=i['product']['id'], order_id=object.pk, qty=i['qty'])

        return Response({"message": "Заказ  создан"}, status=200)

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            return []
        return super().get_permissions()