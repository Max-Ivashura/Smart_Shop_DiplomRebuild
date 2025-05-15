from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey  # Если используется django-mptt

from apps.products.models import Product


class Category(MPTTModel):  # Для древовидной структуры (рекомендуется)
    name = models.CharField(
        "Название",
        max_length=100,
        unique=True,
        help_text="Например: Процессоры, Видеокарты"
    )
    slug = models.SlugField(
        "URL-адрес",
        max_length=100,
        unique=True,
        help_text="Автоматически генерируется из названия"
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="Родительская категория"
    )
    image = models.ImageField(
        "Изображение",
        upload_to='categories/',
        blank=True,
        help_text="Рекомендуемый размер: 300x300px"
    )
    description = models.TextField(
        "Описание",
        blank=True,
        help_text="Краткое описание для SEO"
    )

    class MPTTMeta:
        order_insertion_by = ['name']
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        indexes = [
            models.Index(fields=['slug']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:category", kwargs={"slug": self.slug})

    def get_product_count(self):
        """Считает товары во всех подкатегориях"""
        descendants = self.get_descendants(include_self=True)
        return Product.objects.filter(
            category__in=descendants,
            is_active=True
        ).count()
