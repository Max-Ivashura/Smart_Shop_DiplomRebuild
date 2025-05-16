from django.db import models
from rest_framework.exceptions import ValidationError

from apps.accounts.models import CustomUser
from apps.products.models import Product

class Cart(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name="Пользователь",
        null=True,
        blank=True  # Для неавторизованных пользователей
    )
    session_key = models.CharField(
        "Ключ сессии",
        max_length=40,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Корзина ({self.user or 'аноним'})"

    def add_build(self, build):
        """Добавление всей сборки в корзину"""
        for component in build.components.all():
            CartItem.objects.create(
                cart=self,
                product=component,
                quantity=1
            )
        self.save()

    @property
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Корзина"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар",
        limit_choices_to={"is_active": True, "stock__gt": 0}  # Фильтр доступных товаров
    )
    quantity = models.PositiveIntegerField(
        "Количество",
        default=1
    )
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_price(self):
        return self.product.price * self.quantity

    def clean(self):
        if self.quantity > self.product.stock:
            raise ValidationError("Недостаточно товара на складе")
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ("cart", "product")

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

    def clean(self):
        if self.quantity > self.product.stock:
            raise ValidationError("Недостаточно товара на складе")