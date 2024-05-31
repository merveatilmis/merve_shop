# store/views.py
from django.shortcuts import render, get_object_or_404, redirect
from store.models import Products

def product_list(request):
    products = Products.get_all_products()
    return render(request, 'store/product_list.html', {'products': products})

def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart
    return redirect('product_list')

def cart_detail(request):
    cart = request.session.get('cart', {})
    product_ids = cart.keys()
    products = Products.get_products_by_id(product_ids)
    cart_items = []
    for product in products:
        cart_items.append({
            'product': product,
            'quantity': cart[str(product.id)],
            'total_price': product.price * cart[str(product.id)]
        })
    return render(request, 'store/cart_detail.html', {'cart_items': cart_items})
