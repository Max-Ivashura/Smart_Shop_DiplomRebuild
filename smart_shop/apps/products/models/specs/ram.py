from django.db import models
from ..mixins import BaseSpecs
from ..base import Product


class RAMSpecs(BaseSpecs):
    CATEGORY_SLUG = 'rams'

    # Тип и комплектация
    memory_type = models.CharField(
        "Тип памяти",
        max_length=20,
        default="—",  # Добавлено
        help_text="Например: DDR5"
    )
    module_type = models.CharField(
        "Тип модуля",
        max_length=50,
        default="—",  # Добавлено
        help_text="Например: UDIMM"
    )
    kit_quantity = models.PositiveIntegerField(
        "Количество модулей",
        default=1
    )
    total_capacity = models.PositiveIntegerField(
        "Общий объем комплекта (ГБ)",
        default=0  # Добавлено
    )
    module_capacity = models.PositiveIntegerField(
        "Объем одного модуля (ГБ)",
        default=0  # Добавлено
    )

    # Технические характеристики
    frequency = models.PositiveIntegerField(
        "Базовая частота (МГц)",
        default=0  # Добавлено
    )
    expo_profiles = models.TextField(
        "Профили AMD EXPO",
        blank=True,
        help_text="Формат: 5600 МГц (36-38-38)"
    )
    xmp_profiles = models.TextField(
        "Профили Intel XMP",
        blank=True,
        help_text="Формат: 5600 МГц (36-38-38)"
    )
    cas_latency = models.PositiveIntegerField(
        "CL",
        default=0  # Добавлено
    )
    trcd = models.PositiveIntegerField(
        "tRCD",
        default=0  # Добавлено
    )
    trp = models.PositiveIntegerField(
        "tRP",
        default=0  # Добавлено
    )

    # Конструкция
    heatsink = models.BooleanField(
        "Радиатор",
        default=False
    )
    heatsink_color = models.CharField(
        "Цвет радиатора",
        max_length=50,
        blank=True
    )
    height = models.FloatField(
        "Высота (мм)",
        default=0.0  # Добавлено
    )
    low_profile = models.BooleanField(
        "Low Profile",
        default=False
    )

    # Дополнительные параметры
    voltage = models.FloatField(
        "Напряжение (В)",
        default=0.0  # Добавлено
    )
    ecc = models.BooleanField(
        "ECC",
        default=False
    )
    registered = models.BooleanField(
        "Регистровая",
        default=False
    )
    rank = models.CharField(
        "Ранговость",
        max_length=20,
        choices=[('1R', 'Одноранговая'), ('2R', 'Двухранговая')],
        default='1R'  # Добавлено
    )
    on_die_ecc = models.BooleanField(
        "On-Die ECC",
        default=False
    )

    class Meta:
        verbose_name = "Характеристики оперативной памяти"
        verbose_name_plural = "Характеристики оперативной памяти"
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                name="unique_ram_specs"
            )
        ]

    def get_grouped_specs(self):
        return {
            **self.product.get_base_specs(),
            "Комплектация": {
                "Тип памяти": self.memory_type,
                "Тип модуля": self.module_type,
                "Количество модулей": self.kit_quantity,
                "Общий объем": f"{self.total_capacity} ГБ" if self.total_capacity else "—",  # Обновлено
                "Объем модуля": f"{self.module_capacity} ГБ" if self.module_capacity else "—"  # Обновлено
            },
            "Быстродействие": {
                "Базовая частота": f"{self.frequency} МГц" if self.frequency else "—",  # Обновлено
                "EXPO профили": self.expo_profiles or "—",
                "XMP профили": self.xmp_profiles or "—"
            },
            "Тайминги": {
                "CL": self.cas_latency if self.cas_latency else "—",  # Обновлено
                "tRCD": self.trcd if self.trcd else "—",  # Обновлено
                "tRP": self.trp if self.trp else "—"  # Обновлено
            },
            "Конструкция": {
                "Радиатор": "Да" if self.heatsink else "Нет",
                "Цвет радиатора": self.heatsink_color or "—",
                "Высота": f"{self.height} мм" if self.height else "—",  # Обновлено
                "Low Profile": "Да" if self.low_profile else "Нет"
            },
            "Дополнительно": {
                "Напряжение": f"{self.voltage} В" if self.voltage else "—",  # Обновлено
                "ECC": "Да" if self.ecc else "Нет",
                "Регистровая": "Да" if self.registered else "Нет",
                "Ранговость": self.get_rank_display(),
                "On-Die ECC": "Да" if self.on_die_ecc else "Нет"
            }
        }