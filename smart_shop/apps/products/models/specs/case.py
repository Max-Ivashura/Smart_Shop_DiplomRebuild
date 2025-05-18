from django.db import models
from ..mixins import BaseSpecs
from ..base import Product


class CaseSpecs(BaseSpecs):
    CATEGORY_SLUG = 'case'

    # Форм-фактор и габариты
    case_type = models.CharField(
        "Типоразмер",
        max_length=50,
        default="—",  # Добавлено
        help_text="Например: Mid-Tower"
    )
    dimensions = models.CharField(
        "Габариты (ДxШxВ)",
        max_length=100,
        default="—",  # Добавлено
        help_text="Например: 415x300x400 мм"
    )
    motherboard_orientation = models.CharField(
        "Ориентация платы",
        max_length=20,
        default="вертикально"
    )

    # Внешний вид
    color = models.CharField(
        "Цвет",
        max_length=50,
        default="черный"
    )
    material = models.TextField(
        "Материалы",
        default="—",  # Добавлено
        help_text="Например: сталь, стекло"
    )
    window = models.BooleanField(
        "Боковое окно",
        default=False
    )
    window_material = models.CharField(
        "Материал окна",
        max_length=50,
        blank=True
    )

    # Подсветка
    rgb_type = models.CharField(
        "Тип подсветки",
        max_length=50,
        blank=True
    )
    rgb_control = models.CharField(
        "Управление подсветкой",
        max_length=100,
        blank=True
    )

    # Совместимость
    motherboard_form_factors = models.CharField(
        "Форм-факторы плат",
        max_length=200,
        default="—",  # Добавлено
        help_text="Например: ATX, Micro-ATX"
    )
    psu_location = models.CharField(
        "Размещение БП",
        max_length=50,
        default="нижнее"
    )
    max_gpu_length = models.PositiveIntegerField(
        "Макс. длина видеокарты (мм)",
        default=0  # Добавлено
    )
    max_cooler_height = models.PositiveIntegerField(
        "Макс. высота кулера (мм)",
        default=0  # Добавлено
    )

    # Накопители
    drive_bays = models.TextField(
        "Отсеки для накопителей",
        default="—",  # Добавлено
        help_text="2.5\", 3.5\", 5.25\""
    )

    # Охлаждение
    included_fans = models.TextField(
        "Вентиляторы в комплекте",
        default="—"  # Добавлено
    )
    fan_support = models.TextField(
        "Поддержка вентиляторов",
        default="—",  # Добавлено
        help_text="Размещение и размеры"
    )
    radiator_support = models.TextField(
        "Поддержка СЖО",
        default="—",  # Добавлено
        help_text="Размеры радиаторов"
    )

    # Интерфейсы
    front_io = models.TextField(
        "Разъемы на панели",
        default="—",  # Добавлено
        help_text="USB, аудио и т.д."
    )

    # Конструкция
    cable_management = models.BooleanField(
        "Прокладка кабелей",
        default=True
    )
    dust_filters = models.BooleanField(
        "Пылевые фильтры",
        default=False
    )
    tool_free = models.BooleanField(
        "Безвинтовое крепление",
        default=False
    )

    class Meta:
        verbose_name = "Характеристики корпуса"
        verbose_name_plural = "Характеристики корпусов"
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                name="unique_case_specs"
            )
        ]

    def get_grouped_specs(self):
        return {
            **self.product.get_base_specs(),
            "Конструкция": {
                "Типоразмер": self.case_type,
                "Габариты": self.dimensions,
                "Ориентация платы": self.motherboard_orientation,
                "Материалы": self.material,
                "Боковое окно": "Да" if self.window else "Нет"
            },
            "Совместимость": {
                "Форм-факторы плат": self.motherboard_form_factors,
                "Макс. видеокарта": f"{self.max_gpu_length} мм" if self.max_gpu_length else "—",  # Обновлено
                "Макс. кулер": f"{self.max_cooler_height} мм" if self.max_cooler_height else "—",  # Обновлено
                "Отсеки накопителей": self.drive_bays
            },
            "Охлаждение": {
                "Вентиляторы в комплекте": self.included_fans,
                "Поддержка вентиляторов": self.fan_support,
                "Поддержка СЖО": self.radiator_support
            },
            "Интерфейсы": {
                "Передняя панель": self.front_io
            },
            "Особенности": {
                "Подсветка": self.rgb_type or "—",  # Обновлено
                "Управление подсветкой": self.rgb_control or "—",  # Обновлено
                "Прокладка кабелей": "Да" if self.cable_management else "Нет",
                "Пылевые фильтры": "Да" if self.dust_filters else "Нет"
            }
        }