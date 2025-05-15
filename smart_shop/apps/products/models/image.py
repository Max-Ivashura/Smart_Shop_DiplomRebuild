from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill
from .base import Product


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Товар"
    )

    image = models.ImageField(
        verbose_name="Изображение",
        upload_to="products/%Y/%m/%d/",
        help_text="Рекомендуемый размер: 800x800px"
    )

    thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(200, 200)],
        format='JPEG',
        options={'quality': 85}
    )

    is_main = models.BooleanField(
        verbose_name="Главное изображение",
        default=False,
        help_text="Отображать первым в галерее"
    )

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"
        ordering = ['-is_main']

    def __str__(self):
        return f"Изображение {self.product.name}"

    def save(self, *args, **kwargs):
        if not self.thumbnail:
            self.thumbnail = self.image
        super().save(*args, **kwargs)
