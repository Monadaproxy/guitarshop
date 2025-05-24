from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('cart', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>', views.cart_remove, name='cart_remove'),
]