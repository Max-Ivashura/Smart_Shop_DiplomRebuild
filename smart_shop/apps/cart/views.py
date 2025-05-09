from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView
from .models import Cart, CartItem
from apps.products.models import Product
from django.contrib.sessions.backends.db import SessionStore


def _get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart


class CartDetailView(DetailView):
    template_name = "cart/cart.html"

    def get_object(self):
        return _get_or_create_cart(self.request)


def add_to_cart(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True,
        stock__gt=0  # Только доступные товары
    )
    cart = _get_or_create_cart(request)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        if cart_item.quantity + 1 <= product.stock:
            cart_item.quantity += 1
            cart_item.save()

    return redirect("cart:detail")


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect("cart:detail")


def update_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    new_quantity = int(request.POST.get("quantity", 1))

    if 1 <= new_quantity <= cart_item.product.stock:
        cart_item.quantity = new_quantity
        cart_item.save()

    return redirect("cart:detail")
