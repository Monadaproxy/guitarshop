from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from .serializers import ProductSerializer
from .models import Product, Cart, ProductImage
from django.views.decorators.http import require_POST
from .forms import CartAddProductForm
from orders.models import Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'POST', 'HEAD', 'OPTIONS']:
            return True
        return request.user.is_staff


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        paginator = Paginator(self.get_queryset(), 3)
        page_number = request.GET.get('page')

        try:
            products = paginator.page(page_number)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        serializer = self.get_serializer(products, many=True)

        return render(request, 'products/list.html', {'products': serializer.data, 'page_obj' : products, 'product_list' : serializer.data})

    def update(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.partial_update(request, *args, **kwargs)
        return super().update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        product = self.get_object()
        return render(request, 'products/detail.html', {'product': response.data, 'prod' : product, 'cart_product_form' : CartAddProductForm})

    @action(detail=True, methods=['POST'])
    def custom_update(self, request, pk=None):
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return HttpResponse(serializer.data)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'post']:
            return [IsAdminUser()]
        return []

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product = product,
            amount = cd['amount'],
            override_amount = cd['override_amount']
        )
    product.amount -= 1
    product.save()
    return redirect('cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    product.amount += 1
    product.save()
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    unpaid_order = Order.objects.filter(user=request.user, paid=False)
    return render(request, 'products/cart_detail.html',{'cart' : cart, 'unpaid_order' : unpaid_order})




