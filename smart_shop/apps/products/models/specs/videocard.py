from django.db import models
from ..mixins import BaseSpecs
from ..base import Product


class VideoCardSpecs(BaseSpecs):
    CATEGORY_SLUG = 'videocards'

    # Общие параметры
    color = models.CharField(
        "Цвет",
        max_length=50,
        default="черный"
    )
    mining_support = models.BooleanField(
        "Для майнинга",
        default=False
    )
    lhr = models.BooleanField(
        "LHR",
        default=False,
        help_text="Ограничение хеш-рейта"
    )

    # Графический процессор
    gpu_model = models.CharField(
        "Модель GPU",
        max_length=100,
        default="—",  # Добавлено
        help_text="Например: GeForce RTX 5070 Ti"
    )
    architecture = models.CharField(
        "Архитектура",
        max_length=50,
        default="—",  # Добавлено
        help_text="Например: NVIDIA Blackwell"
    )
    lithography = models.CharField(
        "Техпроцесс",
        max_length=20,
        default="—",  # Добавлено
        help_text="Например: 5 нм"
    )
    alu_units = models.PositiveIntegerField(
        "Вычислительные блоки",
        default=0  # Добавлено
    )
    ray_tracing = models.BooleanField(
        "Трассировка лучей",
        default=False
    )

    # Частоты
    base_clock = models.PositiveIntegerField(
        "Базовая частота (МГц)",
        default=0  # Добавлено
    )
    boost_clock = models.PositiveIntegerField(
        "Турбочастота (МГц)",
        default=0  # Добавлено
    )

    # Видеопамять
    vram_size = models.PositiveIntegerField(
        "Объем памяти (ГБ)",
        default=0  # Добавлено
    )
    vram_type = models.CharField(
        "Тип памяти",
        max_length=20,
        default="—",  # Добавлено
        help_text="Например: GDDR7"
    )
    memory_bus = models.PositiveIntegerField(
        "Разрядность шины (бит)",
        default=0  # Добавлено
    )
    memory_bandwidth = models.CharField(
        "Пропускная способность",
        max_length=50,
        default="—",  # Добавлено
        help_text="Например: 896 ГБ/с"
    )
    memory_freq = models.PositiveIntegerField(
        "Эффективная частота (МГц)",
        default=0  # Добавлено
    )

    # Вывод изображения
    video_outputs = models.TextField(
        "Видеоразъемы",
        default="—",  # Добавлено
        help_text="Формат: 3x DisplayPort 2.1b, 1x HDMI 2.1b"
    )
    max_resolution = models.CharField(
        "Макс. разрешение",
        max_length=50,
        default="—",  # Добавлено
        help_text="Например: 7680x4320"
    )
    monitors_support = models.PositiveIntegerField(
        "Подключение мониторов",
        default=0  # Добавлено
    )

    # Подключение
    pcie_version = models.CharField(
        "PCI Express",
        max_length=20,
        default="—",  # Добавлено
        help_text="Например: 5.0"
    )
    power_connectors = models.CharField(
        "Разъемы питания",
        max_length=100,
        default="—",  # Добавлено
        help_text="Например: 16 pin (12V-2x6)"
    )
    recommended_psu = models.PositiveIntegerField(
        "Блок питания (Вт)",
        default=0  # Добавлено
    )
    tdp = models.PositiveIntegerField(
        "Потребление (Вт)",
        default=0  # Добавлено
    )

    # Охлаждение
    cooling_type = models.CharField(
        "Тип охлаждения",
        max_length=50,
        default="—",  # Добавлено
        help_text="Активное/пассивное/гибридное"
    )
    fans = models.PositiveIntegerField(
        "Количество вентиляторов",
        default=0  # Добавлено
    )
    liquid_cooling = models.BooleanField(
        "СЖО",
        default=False
    )

    # Конструкция
    slots_occupied = models.PositiveIntegerField(
        "Занимаемые слоты",
        default=0  # Добавлено
    )
    dimensions = models.CharField(
        "Габариты (ДхШхТ)",
        max_length=100,
        default="—",  # Добавлено
        help_text="Например: 332x127x60 мм"
    )

    # Дополнительно
    rgb_lighting = models.BooleanField(
        "Подсветка",
        default=False
    )
    bios_switch = models.BooleanField(
        "Переключатель BIOS",
        default=False
    )
    features = models.TextField(
        "Особенности",
        blank=True,
        default="—",  # Добавлено
        help_text="Например: режим 0 дБ"
    )

    class Meta:
        verbose_name = "Характеристики видеокарты"
        verbose_name_plural = "Характеристики видеокарт"
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                name="unique_videocard_specs"
            )
        ]

    def get_grouped_specs(self):
        return {
            **self.product.get_base_specs(),
            "Графический процессор": {
                "Модель": self.gpu_model,
                "Архитектура": self.architecture,
                "Техпроцесс": self.lithography,
                "Вычислительные блоки": self.alu_units if self.alu_units else "—",  # Обновлено
                "Трассировка лучей": "Да" if self.ray_tracing else "Нет"
            },
            "Частоты": {
                "Базовая": f"{self.base_clock} МГц" if self.base_clock else "—",  # Обновлено
                "Турбо": f"{self.boost_clock} МГц" if self.boost_clock else "—"  # Обновлено
            },
            "Память": {
                "Объем": f"{self.vram_size} ГБ {self.vram_type}" if self.vram_size else "—",  # Обновлено
                "Шина": f"{self.memory_bus} бит" if self.memory_bus else "—",  # Обновлено
                "Пропускная способность": self.memory_bandwidth,
                "Частота": f"{self.memory_freq} МГц" if self.memory_freq else "—"  # Обновлено
            },
            "Вывод изображения": {
                "Разъемы": self.video_outputs,
                "Макс. разрешение": self.max_resolution,
                "Мониторы": f"{self.monitors_support} шт" if self.monitors_support else "—"  # Обновлено
            },
            "Питание": {
                "Интерфейс": f"PCIe {self.pcie_version}",
                "Разъемы": self.power_connectors,
                "Рекомендуемый БП": f"{self.recommended_psu} Вт" if self.recommended_psu else "—",  # Обновлено
                "Потребление": f"{self.tdp} Вт" if self.tdp else "—"  # Обновлено
            },
            "Охлаждение": {
                "Тип": self.cooling_type,
                "Вентиляторы": self.fans if self.fans else "—",  # Обновлено
                "СЖО": "Да" if self.liquid_cooling else "Нет"
            },
            "Конструкция": {
                "Слоты": self.slots_occupied if self.slots_occupied else "—",  # Обновлено
                "Габариты": self.dimensions
            },
            "Дополнительно": {
                "Подсветка": "Да" if self.rgb_lighting else "Нет",
                "BIOS Switch": "Да" if self.bios_switch else "Нет",
                "Особенности": self.features
            }
        }