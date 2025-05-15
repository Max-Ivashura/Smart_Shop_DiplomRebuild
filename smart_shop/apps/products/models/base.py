from django.db import models
from django.db.models import Avg
from django.urls import reverse
from django.utils.text import slugify
from mptt.fields import TreeForeignKey

from apps.core.models import TimeStampedModel
from django.utils import timezone


class Product(TimeStampedModel):
    category = TreeForeignKey(
        'Category',  # Используем строковую ссылку
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name="Категория",
        help_text="Выберите категорию товара"
    )
    name = models.CharField(
        "Название",
        max_length=200,
        help_text="Например: Intel Core i9-13900K"
    )
    description = models.TextField("Описание товара", blank=True)
    price = models.DecimalField(
        "Цена (руб)",
        max_digits=10,
        decimal_places=2,
        help_text="Максимум 10 знаков"
    )
    sku = models.CharField(
        "Артикул",
        max_length=50,
        unique=True,
        help_text="Уникальный идентификатор"
    )
    is_active = models.BooleanField(
        "Активен",
        default=True,
        help_text="Отображать товар на сайте"
    )
    slug = models.SlugField(
        "URL-адрес",
        max_length=200,
        unique=True,
        blank=True,
        help_text="Автоматически генерируется"
    )
    warranty = models.CharField(
        "Гарантия",
        max_length=50,
        blank=True,
        help_text="Например: 3 года"
    )
    country = models.CharField(
        "Страна",
        max_length=100,
        blank=True,
        help_text="Например: США"
    )
    stock = models.PositiveIntegerField(
        "Остаток",
        default=0,
        help_text="Количество на складе"
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["sku"]),
            models.Index(fields=["slug"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.sku}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def get_first_image(self):
        return self.images.first()

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def average_rating(self):
        return self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    @property
    def is_new(self):
        return (timezone.now() - self.created_at).days < 30

    def get_absolute_url(self):
        return reverse(
            "products:detail",
            kwargs={
                "category_slug": self.category.slug,
                "product_slug": self.slug
            }
        )

    def get_base_specs(self):
        return {
            "Основные параметры": {
                "Гарантия": self.warranty,
                "Страна": self.country,
                "Артикул": self.sku,
                "Наличие": f"{self.stock} шт.",
                "Цена": f"{self.price} руб."
            }
        }

    @property
    def specs(self):
        # Получаем slug категории товара
        category_slug = self.category.slug
        # Формируем имя атрибута (например: processorspecs_specs)
        specs_attr = f"{category_slug}specs_specs"
        # Проверяем наличие спецификаций
        if hasattr(self, specs_attr):
            return getattr(self, specs_attr).get_grouped_specs()
        # Возвращаем базовые характеристики, если спецификаций нет
        return self.get_base_specs()
