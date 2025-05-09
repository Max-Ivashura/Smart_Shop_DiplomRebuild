from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "session_key", "total_price", "created_at")
    list_filter = ("user",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("product", "cart", "quantity", "total_price")
    list_filter = ("cart__user",)

    def total_price(self, obj):
        return obj.product.price * obj.quantity

    total_price.short_description = "Сумма"
