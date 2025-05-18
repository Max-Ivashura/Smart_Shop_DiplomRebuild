from django.db import models
from ..mixins import BaseSpecs
from ..base import Product


class CoolerSpecs(BaseSpecs):
    CATEGORY_SLUG = 'cooler'

    # Общие параметры
    socket_support = models.TextField(
        "Поддерживаемые сокеты",
        default="—",  # Добавлено
        help_text="Перечислите через запятую"
    )
    tdp = models.PositiveIntegerField(
        "Рассеиваемая мощность (Вт)",
        default=0  # Добавлено
    )
    construction_type = models.CharField(
        "Тип конструкции",
        max_length=50,
        choices=[
            ('tower', 'Башенный'),
            ('low_profile', 'Низкопрофильный'),
            ('top_flow', 'Верхний обдув')
        ],
        default='tower'  # Добавлено
    )

    # Радиатор
    base_material = models.CharField(
        "Материал основания",
        max_length=50,
        default="—"  # Добавлено
    )
    heatsink_material = models.CharField(
        "Материал радиатора",
        max_length=50,
        default="—"  # Добавлено
    )
    heat_pipes = models.PositiveIntegerField(
        "Тепловые трубки",
        default=0  # Добавлено
    )
    pipe_diameter = models.FloatField(
        "Диаметр трубок (мм)",
        default=0.0  # Добавлено
    )
    nickel_plating = models.TextField(
        "Никелированное покрытие",
        blank=True
    )
    heatsink_color = models.CharField(
        "Цвет радиатора",
        max_length=50,
        default="—"  # Добавлено
    )

    # Вентилятор
    included_fans = models.PositiveIntegerField(
        "Вентиляторы в комплекте",
        default=0  # Добавлено
    )
    fan_size = models.CharField(
        "Размер вентиляторов",
        max_length=50,
        default="—",  # Добавлено
        help_text="Например: 120x120 мм"
    )
    fan_connector = models.CharField(
        "Разъем питания",
        max_length=20,
        default="4 pin"
    )
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
        help_text="Например: 67.88 CFM"
    )
    noise_level = models.FloatField(
        "Уровень шума (дБ)",
        default=0.0  # Добавлено
    )
    bearing_type = models.CharField(
        "Тип подшипника",
        max_length=50,
        default="—"  # Добавлено
    )

    # Дополнительно
    thermal_paste = models.BooleanField(
        "Термопаста в комплекте",
        default=False
    )
    rgb_lighting = models.BooleanField(
        "Подсветка",
        default=False
    )

    # Габариты
    height = models.PositiveIntegerField(
        "Высота (мм)",
        default=0  # Добавлено
    )
    width = models.PositiveIntegerField(
        "Ширина (мм)",
        default=0  # Добавлено
    )
    length = models.PositiveIntegerField(
        "Длина (мм)",
        default=0  # Добавлено
    )
    weight = models.PositiveIntegerField(
        "Вес (г)",
        default=0  # Добавлено
    )

    class Meta:
        verbose_name = "Характеристики кулера"
        verbose_name_plural = "Характеристики кулеров"
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                name="unique_cooler_specs"
            )
        ]

    def get_grouped_specs(self):
        return {
            **self.product.get_base_specs(),
            "Конструкция": {
                "Тип": self.get_construction_type_display(),
                "Сокеты": self.socket_support,
                "TDP": f"{self.tdp} Вт" if self.tdp else "—"  # Обновлено
            },
            "Радиатор": {
                "Материал основания": self.base_material,
                "Материал радиатора": self.heatsink_material,
                "Тепловые трубки": f"{self.heat_pipes} шт" if self.heat_pipes else "—",  # Обновлено
                "Диаметр трубок": f"{self.pipe_diameter} мм" if self.pipe_diameter else "—",  # Обновлено
                "Покрытие": self.nickel_plating or "—",
                "Цвет": self.heatsink_color
            },
            "Вентилятор": {
                "Количество": self.included_fans if self.included_fans else "—",  # Обновлено
                "Размер": self.fan_size,
                "Разъем": self.fan_connector,
                "Скорость": (
                    f"{self.min_rpm}-{self.max_rpm} об/мин"
                    if self.min_rpm or self.max_rpm
                    else "—"
                ),
                "Воздушный поток": self.airflow,
                "Шум": f"{self.noise_level} дБ" if self.noise_level else "—",  # Обновлено
                "Подшипник": self.bearing_type
            },
            "Габариты": {
                "Высота": f"{self.height} мм" if self.height else "—",  # Обновлено
                "Ширина": f"{self.width} мм" if self.width else "—",  # Обновлено
                "Длина": f"{self.length} мм" if self.length else "—",  # Обновлено
                "Вес": f"{self.weight} г" if self.weight else "—"  # Обновлено
            },
            "Дополнительно": {
                "Термопаста": "Да" if self.thermal_paste else "Нет",
                "Подсветка": "Да" if self.rgb_lighting else "Нет"
            }
        }