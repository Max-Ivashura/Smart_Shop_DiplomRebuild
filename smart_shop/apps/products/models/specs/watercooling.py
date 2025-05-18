from django.db import models
from ..mixins import BaseSpecs
from ..base import Product


class WaterCoolingSpecs(BaseSpecs):
    CATEGORY_SLUG = 'watercooling'

    # Общие параметры
    cooling_type = models.CharField(
        "Тип системы",
        max_length=50,
        default="СЖО"
    )
    serviceable = models.BooleanField(
        "Обслуживаемая",
        default=False
    )

    # Внешний вид
    color = models.CharField(
        "Цвет",
        max_length=50,
        default="черный"
    )
    rgb_type = models.CharField(
        "Тип подсветки",
        max_length=50,
        blank=True
    )
    rgb_components = models.CharField(
        "Источники подсветки",
        max_length=100,
        default="—",  # Добавлено
        help_text="Например: вентилятор, водоблок"
    )

    # Водоблок
    socket_support = models.TextField(
        "Поддерживаемые сокеты",
        default="—"  # Добавлено
    )
    block_material = models.CharField(
        "Материал водоблока",
        max_length=50,
        default="—"  # Добавлено
    )
    block_dimensions = models.CharField(
        "Размеры водоблока (ДxШxВ)",
        max_length=100,
        default="—"  # Добавлено
    )

    # Радиатор
    radiator_size = models.CharField(
        "Размер радиатора",
        max_length=100,
        default="—",  # Добавлено
        help_text="Например: 360 мм"
    )
    tdp = models.PositiveIntegerField(
        "Рассеиваемая мощность (Вт)",
        default=0  # Добавлено
    )
    radiator_material = models.CharField(
        "Материал радиатора",
        max_length=50,
        default="—"  # Добавлено
    )
    radiator_dimensions = models.CharField(
        "Габариты радиатора (ДxШxТ)",
        max_length=100,
        default="—"  # Добавлено
    )

    # Вентиляторы
    fan_quantity = models.PositiveIntegerField(
        "Количество вентиляторов",
        default=0  # Добавлено
    )
    fan_size = models.CharField(
        "Размер вентиляторов",
        max_length=50,
        default="—"  # Добавлено
    )
    fan_rpm = models.CharField(
        "Скорость вращения",
        max_length=50,
        default="—",  # Добавлено
        help_text="Например: 600-1800 об/мин"
    )
    fan_noise = models.CharField(
        "Уровень шума",
        max_length=50,
        default="—",  # Добавлено
        help_text="Например: 11.2-32.5 дБ"
    )
    fan_airflow = models.CharField(
        "Воздушный поток",
        max_length=50,
        default="—"  # Добавлено
    )

    # Помпа
    pump_noise = models.FloatField(
        "Шум помпы (дБ)",
        default=0.0  # Добавлено
    )
    pump_speed = models.PositiveIntegerField(
        "Скорость помпы (об/мин)",
        default=0  # Добавлено
    )

    # Трубки
    tube_material = models.CharField(
        "Материал трубок",
        max_length=50,
        default="—"  # Добавлено
    )
    transparent_tubes = models.BooleanField(
        "Прозрачные трубки",
        default=False
    )

    # Дополнительно
    thermal_paste = models.BooleanField(
        "Термопаста в комплекте",
        default=False
    )
    included_accessories = models.TextField(
        "Комплектация",
        blank=True,
        default="—"  # Добавлено
    )

    class Meta:
        verbose_name = "Характеристики СЖО"
        verbose_name_plural = "Характеристики систем охлаждения"
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                name="unique_watercooling_specs"
            )
        ]

    def get_grouped_specs(self):
        return {
            **self.product.get_base_specs(),
            "Конструкция": {
                "Тип системы": self.cooling_type,
                "Обслуживаемая": "Да" if self.serviceable else "Нет",
                "Цвет": self.color,
                "Подсветка": self.rgb_type or "—"  # Обновлено
            },
            "Водоблок": {
                "Сокеты": self.socket_support,
                "Материал": self.block_material,
                "Размеры": self.block_dimensions
            },
            "Радиатор": {
                "Размер": self.radiator_size,
                "Мощность": f"{self.tdp} Вт" if self.tdp else "—",  # Обновлено
                "Материал": self.radiator_material,
                "Габариты": self.radiator_dimensions
            },
            "Вентиляторы": {
                "Количество": self.fan_quantity if self.fan_quantity else "—",  # Обновлено
                "Размер": self.fan_size,
                "Скорость": self.fan_rpm,
                "Шум": self.fan_noise,
                "Воздушный поток": self.fan_airflow
            },
            "Помпа": {
                "Шум": f"{self.pump_noise} дБ" if self.pump_noise else "—",  # Обновлено
                "Скорость": f"{self.pump_speed} об/мин" if self.pump_speed else "—"  # Обновлено
            },
            "Трубки": {
                "Материал": self.tube_material,
                "Прозрачные": "Да" if self.transparent_tubes else "Нет"
            },
            "Дополнительно": {
                "Термопаста": "Да" if self.thermal_paste else "Нет",
                "Комплектация": self.included_accessories
            }
        }