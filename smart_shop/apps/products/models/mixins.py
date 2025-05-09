from django.db import models
from django.core.exceptions import ValidationError


class BaseSpecs(models.Model):
    """
    Абстрактная модель для характеристик товаров.
    Все спецификации должны наследоваться от этого класса.
    """
    CATEGORY_SLUG = None
    product = models.OneToOneField(
        'Product',
        on_delete=models.CASCADE,
        related_name='%(class)s_specs',  # Динамический related_name
        verbose_name="Товар"
    )

    class Meta:
        abstract = True  # Важно: модель не создается в БД

    def get_grouped_specs(self):
        """
        Возвращает характеристики в формате:
        {
            "Группа характеристик": {
                "Параметр": "Значение",
                ...
            },
            ...
        }
        """
        raise NotImplementedError("Метод должен быть переопределен в дочернем классе!")

    def clean(self):
        """
        Валидация: товар должен принадлежать правильной категории.
        Например, ProcessorSpecs можно привязать только к товару с category.slug='processor'
        """
        if not self.CATEGORY_SLUG:
            raise ValidationError("CATEGORY_SLUG не задан для класса спецификации!")

        if self.product.category.slug != self.CATEGORY_SLUG:
            raise ValidationError(
                f"Товар должен принадлежать категории '{self.CATEGORY_SLUG}'!"
            )

    def __str__(self):
        return f"Характеристики {self.product.name}"
