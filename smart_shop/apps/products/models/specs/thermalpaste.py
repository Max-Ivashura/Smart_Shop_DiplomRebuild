from django.db import models
from ..mixins import BaseSpecs
from ..base import Product


class ThermalPasteSpecs(BaseSpecs):
    CATEGORY_SLUG = 'thermalpastes'

    # Общие параметры
    weight = models.FloatField(
        "Вес (г)",
        default=0.0,  # Добавлено
        help_text="Общий вес термопасты в упаковке"
    )

    # Характеристики термоинтерфейса
    thermal_conductivity = models.FloatField(
        "Теплопроводность (Вт/м·К)",
        default=0.0,  # Добавлено
        help_text="Коэффициент теплопроводности"
    )
    packaging = models.CharField(
        "Упаковка",
        max_length=50,
        choices=[
            ('syringe', 'Шприц'),
            ('tube', 'Тюбик'),
            ('packet', 'Пакетик')
        ],
        default='syringe'  # Добавлено
    )
    max_temp = models.IntegerField(
        "Макс. температура (°C)",
        default=0  # Добавлено
    )
    min_temp = models.IntegerField(
        "Мин. температура (°C)",
        default=0  # Добавлено
    )

    class Meta:
        verbose_name = "Характеристики термопасты"
        verbose_name_plural = "Характеристики термопаст"
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                name="unique_thermalpaste_specs"
            )
        ]

    def get_grouped_specs(self):
        return {
            **self.product.get_base_specs(),
            "Основные параметры": {
                "Вес": f"{self.weight} г" if self.weight else "—",  # Обновлено
                "Упаковка": self.get_packaging_display()
            },
            "Тепловые характеристики": {
                "Теплопроводность": (
                    f"{self.thermal_conductivity} Вт/м·К"
                    if self.thermal_conductivity
                    else "—"  # Обновлено
                ),
                "Рабочий диапазон": (
                    f"{self.min_temp}°C ~ {self.max_temp}°C"
                    if self.min_temp or self.max_temp
                    else "—"  # Обновлено
                )
            }
        }