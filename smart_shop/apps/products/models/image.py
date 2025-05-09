from django.db import models
from .base import Product


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Товар"
    )
    image = models.ImageField(
        "Изображение",
        upload_to="products/%Y/%m/%d/",
        help_text="Рекомендуемый размер: 800x800px"
    )
    is_main = models.BooleanField(
        "Главное изображение",
        default=False,
        help_text="Отображать первым в галерее"
    )

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"

    def __str__(self):
        return f"Изображение {self.product.name}"
