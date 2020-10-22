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
        cart_products = Cart.objects.all()
        products = []
        order_products = []
        for item in cart_products:
            product = item.product
            qty = item.qty
            product.amount -= qty
            products.append(product)
            order_product = OrderProduct(order=object, product=product, qty=qty)
            order_products.append(order_product)
        # массовое создание всех товаров в заказе
        OrderProduct.objects.bulk_create(order_products)
        # массовое обновление остатка у всех товаров
        Product.objects.bulk_update(products, ('amount',))
        # массовое удаление всех товаров в корзине
        cart_products.delete()

        return Response({"message": "Заказ  создан"}, status=200)

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            return []
        return super().get_permissions()