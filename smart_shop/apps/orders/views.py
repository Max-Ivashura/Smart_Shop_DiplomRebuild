from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib import messages

from apps.cart.views import _get_or_create_cart
from .models import Order, OrderItem


class OrderListView(ListView):
    model = Order
    template_name = "orders/list.html"

    def get_queryset(self):
        return self.request.user.orders.all()


# apps/orders/views.py
class OrderDetailView(DetailView):
    model = Order
    template_name = "orders/detail.html"  # Правильный путь
    context_object_name = "order"


def create_order(request):
    cart = _get_or_create_cart(request)  # Используем функцию из cart/views.py

    if not cart.items.exists():
        messages.error(request, "Корзина пуста!")
        return redirect("cart:detail")

    # Проверка доступности товаров
    errors = []
    for item in cart.items.all():
        if item.product.stock < item.quantity:
            errors.append(f"Недостаточно товара: {item.product.name}")

    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect("cart:detail")

    # Создание заказа
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        address=request.POST.get("address", "")
    )

    # Перенос товаров из корзины в заказ
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price_at_order=item.product.price
        )
        item.product.stock -= item.quantity
        item.product.save()

    cart.items.all().delete()  # Очистка корзины
    return redirect("orders:detail", pk=order.pk)


def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if order.status == "pending":
        order.cancel()
        messages.success(request, "Заказ отменен. Товары возвращены на склад.")
    else:
        messages.error(request, "Невозможно отменить заказ в текущем статусе.")
    return redirect("orders:detail", pk=pk)