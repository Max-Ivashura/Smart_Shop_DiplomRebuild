from django.db import models
from django.core.exceptions import ValidationError
from apps.accounts.models import CustomUser
from apps.products.models import Product, Category


class Comparison(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Пользователь"
    )
    session_key = models.CharField(
        "Ключ сессии",
        max_length=40,
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def get_product_ids(self):
        return list(self.items.values_list('product_id', flat=True))

    class Meta:
        verbose_name = "Сравнение"
        verbose_name_plural = "Сравнения"
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'category'],
                name='unique_user_category_comparison',
                condition=models.Q(user__isnull=False)
            ),
            models.UniqueConstraint(
                fields=['session_key', 'category'],
                name='unique_session_category_comparison',
                condition=models.Q(user__isnull=True)
            )
        ]

    def __str__(self):
        return f"Сравнение {self.category} ({self.user or 'аноним'})"

    def clean(self):
        # Проверка при добавлении товаров
        if self.items.count() >= 4:
            raise ValidationError("Максимум 4 товара в сравнении")


class ComparisonItem(models.Model):
    comparison = models.ForeignKey(
        Comparison,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Сравнение"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Элемент сравнения"
        verbose_name_plural = "Элементы сравнения"
        ordering = ['-added_at']
        constraints = [
            models.UniqueConstraint(
                fields=['comparison', 'product'],
                name='unique_comparison_product'
            )
        ]

    def __str__(self):
        return f"{self.product.name} в сравнении"

    def clean(self):
        # Проверка соответствия категорий
        if self.product.category != self.comparison.category:
            raise ValidationError("Товар должен принадлежать категории сравнения")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
