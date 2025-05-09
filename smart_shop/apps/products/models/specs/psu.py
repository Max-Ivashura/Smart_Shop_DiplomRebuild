from django.db import models
from ..mixins import BaseSpecs
from ..base import Product


class PSUSpecs(BaseSpecs):
    CATEGORY_SLUG = 'psus'

    # Общие параметры
    wattage = models.PositiveIntegerField(
        "Номинальная мощность (Вт)",
        default=0  # Добавлено
    )
    form_factor = models.CharField(
        "Форм-фактор",
        max_length=50,
        default="ATX"
    )
    color = models.CharField(
        "Цвет",
        max_length=50,
        default="черный"
    )
    modularity = models.CharField(
        "Модульность",
        max_length=20,
        choices=[
            ('full', 'Полностью модульный'),
            ('semi', 'Частично модульный'),
            ('non', 'Немодульный')
        ],
        default='non'  # Добавлено
    )
    cable_sleeving = models.BooleanField(
        "Оплетка кабелей",
        default=False
    )
    rgb_lighting = models.BooleanField(
        "Подсветка",
        default=False
    )

    # Разъемы
    main_connector = models.CharField(
        "Основной разъем",
        max_length=50,
        default="20+4 pin"
    )
    cpu_connectors = models.PositiveIntegerField(
        "Разъемы CPU (4+4 pin)",
        default=0  # Добавлено
    )
    pcie_connectors = models.PositiveIntegerField(
        "Разъемы PCI-E (6+2 pin)",
        default=0  # Добавлено
    )
    sata_connectors = models.PositiveIntegerField(
        "Разъемы SATA",
        default=0  # Добавлено
    )
    molex_connectors = models.PositiveIntegerField(
        "Разъемы Molex",
        default=0  # Добавлено
    )

    # Длины кабелей
    main_cable_length = models.PositiveIntegerField(
        "Длина основного кабеля (мм)",
        default=0  # Добавлено
    )
    cpu_cable_length = models.PositiveIntegerField(
        "Длина кабеля CPU (мм)",
        default=0  # Добавлено
    )
    pcie_cable_length = models.PositiveIntegerField(
        "Длина кабеля PCI-E (мм)",
        default=0  # Добавлено
    )

    # Электрические параметры
    psu_standard = models.CharField(
        "Стандарт",
        max_length=50,
        default="—",  # Добавлено
        help_text="Например: ATX 12V 2.31"
    )
    efficiency_cert = models.CharField(
        "Сертификат 80 PLUS",
        max_length=20,
        choices=[
            ('none', 'Нет'),
            ('bronze', 'Bronze'),
            ('silver', 'Silver'),
            ('gold', 'Gold'),
            ('platinum', 'Platinum'),
            ('titanium', 'Titanium')
        ],
        default='none'  # Добавлено
    )
    pfc_type = models.CharField(
        "PFC",
        max_length=20,
        choices=[('active', 'Активный'), ('passive', 'Пассивный')],
        default='active'  # Добавлено
    )
    protections = models.TextField(
        "Защиты",
        default="—",  # Добавлено
        help_text="Например: OCP, OVP, SCP"
    )

    # Охлаждение
    fan_size = models.CharField(
        "Вентилятор",
        max_length=50,
        default="—",  # Добавлено
        help_text="Например: 120 мм"
    )
    fan_control = models.BooleanField(
        "Регулировка оборотов",
        default=True
    )
    zero_rpm = models.BooleanField(
        "Режим 0 дБ",
        default=False
    )

    # Габариты
    dimensions = models.CharField(
        "Размеры (ДxШxВ)",
        max_length=100,
        default="—",  # Добавлено
        help_text="Например: 160x150x86 мм"
    )
    weight = models.FloatField(
        "Вес (кг)",
        default=0.0  # Добавлено
    )

    class Meta:
        verbose_name = "Характеристики БП"
        verbose_name_plural = "Характеристики БП"
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                name="unique_psu_specs"
            )
        ]

    def get_grouped_specs(self):
        return {
            **self.product.get_base_specs(),
            "Общие": {
                "Мощность": f"{self.wattage} Вт" if self.wattage else "—",  # Обновлено
                "Форм-фактор": self.form_factor,
                "Цвет": self.color,
                "Модульность": self.get_modularity_display(),
                "Оплетка": "Да" if self.cable_sleeving else "Нет"
            },
            "Разъемы": {
                "Основной": self.main_connector,
                "CPU": f"{self.cpu_connectors} шт" if self.cpu_connectors else "—",  # Обновлено
                "PCI-E": f"{self.pcie_connectors} шт" if self.pcie_connectors else "—",  # Обновлено
                "SATA": f"{self.sata_connectors} шт" if self.sata_connectors else "—",  # Обновлено
                "Molex": f"{self.molex_connectors} шт" if self.molex_connectors else "—"  # Обновлено
            },
            "Электрика": {
                "Стандарт": self.psu_standard,
                "Сертификат": self.get_efficiency_cert_display(),
                "PFC": self.get_pfc_type_display(),
                "Защиты": self.protections
            },
            "Охлаждение": {
                "Вентилятор": self.fan_size,
                "Регулировка": "Да" if self.fan_control else "Нет",
                "Режим 0 дБ": "Да" if self.zero_rpm else "Нет"
            },
            "Конструкция": {
                "Размеры": self.dimensions,
                "Вес": f"{self.weight} кг" if self.weight else "—"  # Обновлено
            }
        }