from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from api_v1.views import ProductViewSet, OrderApi

app_name = 'api_v1'

router = DefaultRouter()
router.register(r'product', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('orders/<int:pk>/', OrderApi.as_view(), name='order_api'),
    path('orders/', OrderApi.as_view(), name='orderproduct_api'),
    path('login/', obtain_auth_token, name='api_token_auth'),
]