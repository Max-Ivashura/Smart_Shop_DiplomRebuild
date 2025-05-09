from django.db import models
from ..mixins import BaseSpecs
from ..base import Product


class CaseFanSpecs(BaseSpecs):
    CATEGORY_SLUG = 'casefans'

    # Общие параметры
    fan_quantity = models.PositiveIntegerField(
        "Количество в комплекте",
        default=1
    )

    # Внешний вид
    frame_color = models.CharField(
        "Цвет каркаса",
        max_length=50,
        default="черный"
    )
    blade_color = models.CharField(
        "Цвет крыльчатки",
        max_length=50,
        default="—"  # Добавлено
    )
    rgb_type = models.CharField(
        "Тип подсветки",
        max_length=50,
        blank=True
    )
    rgb_source = models.CharField(
        "Источник подсветки",
        max_length=100,
        blank=True
    )

    # Конструкция
    size = models.CharField(
        "Размер",
        max_length=50,
        default="—",  # Добавлено
        help_text="Например: 120x120 мм"
    )
    thickness = models.PositiveIntegerField(
        "Толщина (мм)",
        default=0  # Добавлено
    )
    bearing_type = models.CharField(
        "Тип подшипника",
        max_length=100,
        default="—"  # Добавлено
    )
    anti_vibration = models.BooleanField(
        "Антивибрационные прокладки",
        default=False
    )

    # Технические характеристики
    max_rpm = models.PositiveIntegerField(
        "Макс. скорость (об/мин)",
        default=0  # Добавлено
    )
    min_rpm = models.PositiveIntegerField(
        "Мин. скорость (об/мин)",
        default=0  # Добавлено
    )
    airflow = models.CharField(
        "Воздушный поток",
        max_length=50,
        default="—",  # Добавлено
        help_text="Например: 68.2 CFM"
    )
    static_pressure = models.CharField(
        "Статическое давление",
        max_length=50,
        default="—",  # Добавлено
        help_text="Например: 18.3 Па"
    )
    max_noise = models.FloatField(
        "Макс. шум (дБ)",
        default=0.0  # Добавлено
    )
    min_noise = models.FloatField(
        "Мин. шум (дБ)",
        default=0.0  # Добавлено
    )

    # Питание
    connector_type = models.CharField(
        "Разъем питания",
        max_length=100,
        default="—"  # Добавлено
    )
    pwm_control = models.BooleanField(
        "PWM управление",
        default=True
    )
    voltage = models.FloatField(
        "Напряжение (В)",
        default=0.0  # Добавлено
    )
    current = models.FloatField(
        "Ток (мА)",
        default=0.0  # Добавлено
    )

    # Подсветка
    rgb_connector = models.CharField(
        "Разъем подсветки",
        max_length=50,
        blank=True
    )
    controller_included = models.BooleanField(
        "Контроллер в комплекте",
        default=False
    )
    remote_control = models.BooleanField(
        "ПДУ в комплекте",
        default=False
    )

    class Meta:
        verbose_name = "Характеристики вентилятора"
        verbose_name_plural = "Характеристики вентиляторов"
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                name="unique_casefan_specs"
            )
        ]

    def get_grouped_specs(self):
        return {
            **self.product.get_base_specs(),
            "Конструкция": {
                "Размер": self.size,
                "Толщина": f"{self.thickness} мм" if self.thickness else "—",  # Обновлено
                "Подшипник": self.bearing_type,
                "Антивибрация": "Да" if self.anti_vibration else "Нет"
            },
            "Характеристики": {
                "Скорость": (
                    f"{self.min_rpm}-{self.max_rpm} об/мин"
                    if self.min_rpm or self.max_rpm
                    else "—"
                ),
                "Воздушный поток": self.airflow,
                "Давление": self.static_pressure,
                "Шум": (
                    f"{self.min_noise}-{self.max_noise} дБ"
                    if self.min_noise or self.max_noise
                    else "—"
                )
            },
            "Питание": {
                "Разъем": self.connector_type,
                "Управление": "PWM" if self.pwm_control else "DC",
                "Напряжение": f"{self.voltage} В" if self.voltage else "—",  # Обновлено
                "Ток": f"{self.current} мА" if self.current else "—"  # Обновлено
            },
            "Подсветка": {
                "Тип": self.rgb_type or "—",  # Обновлено
                "Источник": self.rgb_source or "—",  # Обновлено
                "Разъем": self.rgb_connector or "—",  # Обновлено
                "Контроллер": "Да" if self.controller_included else "Нет",
                "ПДУ": "Да" if self.remote_control else "Нет"
            },
            "Внешний вид": {
                "Цвет каркаса": self.frame_color,
                "Цвет крыльчатки": self.blade_color
            }
        }