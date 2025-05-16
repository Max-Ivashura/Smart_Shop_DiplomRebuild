from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView

from apps.compare.models import Comparison
from compare.utils import get_user_comparison
from .models import Cart, CartItem
from apps.products.models import Product
from django.contrib.sessions.backends.db import SessionStore


@require_http_methods(["POST"])
def update_quantity(request, cart_item_id):
    try:
        cart_item = CartItem.objects.select_related('product', 'cart').get(
            id=cart_item_id,
            cart=_get_or_create_cart(request)  # Проверка владельца корзины
        )

        new_quantity = int(request.POST.get("quantity", 1))

        if new_quantity < 1 or new_quantity > cart_item.product.stock:
            raise ValueError("Некорректное количество")

        cart_item.quantity = new_quantity
        cart_item.save()

        return JsonResponse({
            'status': 'success',
            'item_total': cart_item.get_total_price,
            'cart_total': cart_item.cart.total_price,
            'total_items': cart_item.cart.items.count()
        })

    except (CartItem.DoesNotExist, ValueError) as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e) if str(e) else "Ошибка обновления"
        }, status=400)


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.object

        # Добавьте этот блок для получения ID товаров в сравнении
        comparison_product_ids = set()

        if self.request.user.is_authenticated:
            comparisons = Comparison.objects.filter(user=self.request.user)
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.create()
                session_key = self.request.session.session_key
            comparisons = Comparison.objects.filter(session_key=session_key)

        for comparison in comparisons:
            comparison_product_ids.update(
                comparison.items.values_list('product_id', flat=True)
            )

        context['comparison_product_ids'] = comparison_product_ids
        return context

    def get_object(self):
        return _get_or_create_cart(self.request)


@require_POST
def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id, is_active=True, stock__gt=0)
        cart = _get_or_create_cart(request)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return JsonResponse({
            'status': 'success',
            'cart_count': cart.items.count()
        })

    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Товар недоступен'}, status=400)


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(
        CartItem,
        id=cart_item_id,
        cart=_get_or_create_cart(request)  # Добавьте эту проверку
    )
    cart_item.delete()
    return redirect("cart:detail")
