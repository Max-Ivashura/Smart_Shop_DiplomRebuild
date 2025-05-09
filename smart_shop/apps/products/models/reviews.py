from django.db import models
from apps.accounts.models import CustomUser
from .base import Product


class Review(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Пользователь"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Товар"
    )
    text = models.TextField("Текст отзыва", max_length=1000)
    rating = models.PositiveSmallIntegerField(
        "Оценка",
        choices=[(i, str(i)) for i in range(1, 6)],  # Оценка от 1 до 5
        default=5
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]
        unique_together = [["user", "product"]]  # Один отзыв на товар

    def __str__(self):
        return f"Отзыв от {self.user} на {self.product}"
