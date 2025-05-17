# models.py
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
    categories = models.ManyToManyField(  # Изменено на M2M
        Category,
        verbose_name="Категории сравнения",
        related_name='comparisons'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Сравнение"
        verbose_name_plural = "Сравнения"
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                name='unique_user_comparison',
                condition=models.Q(user__isnull=False)
            ),
            models.UniqueConstraint(
                fields=['session_key'],  # Исправлено session_id → session_key
                name='unique_session_comparison',
                condition=models.Q(user__isnull=True)
            )
        ]

    def __str__(self):
        return f"Сравнение #{self.id}"


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
    category = models.ForeignKey(  # Новая связь с категорией
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория товара"
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

    def clean(self):
        # Проверка соответствия категории товара
        if self.product.category != self.category:
            raise ValidationError("Категория товара не совпадает")

        # Проверка лимита товаров в категории
        category_items = self.comparison.items.filter(category=self.category)
        if category_items.count() >= 4:
            raise ValidationError("Максимум 4 товара в категории")

    def save(self, *args, **kwargs):
        self.category = self.product.category  # Автоматическое назначение категории
        super().save(*args, **kwargs)
