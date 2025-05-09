from django.db import models
from django.core.exceptions import ValidationError
from apps.accounts.models import CustomUser
from apps.products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидает подтверждения"),
        ("processing", "В обработке"),
        ("completed", "Завершен"),
        ("canceled", "Отменен"),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Пользователь"
    )
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    address = models.CharField(
        "Адрес доставки",
        max_length=255,
        blank=True
    )
    comment = models.TextField("Комментарий", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Заказ #{self.id}"

    @property
    def total_price(self):
        return sum(item.price_at_order * item.quantity for item in self.items.all())

    @property
    def status_color(self):
        return {
            "pending": "warning",
            "processing": "info",
            "completed": "success",
            "canceled": "danger"
        }.get(self.status, "secondary")

    def cancel(self):
        """Отмена заказа и возврат товаров на склад"""
        if self.status == "pending":
            for item in self.items.all():
                item.product.stock += item.quantity
                item.product.save()
            self.status = "canceled"
            self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Заказ"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField("Количество")
    price_at_order = models.DecimalField(
        "Цена на момент заказа",
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product.name if self.product else '[Товар удален]'} x{self.quantity}"

    @property
    def total_price(self):
        return self.price_at_order * self.quantity
