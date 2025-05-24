from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import OrderCreateForm
from products.models import Cart
from orders.models import OrderItem

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, request=request)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], amount=item['amount'])
            request.session['order_id'] = order.id
            cart.clear()
            return redirect(reverse('payment:process'))
        else:
            return HttpResponse(f'Форма невалидна: {form.errors}')
    form = OrderCreateForm(request=request)
    return render(request, 'orders/create.html', {'cart' : cart, 'form' : form})


