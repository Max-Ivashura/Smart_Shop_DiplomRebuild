from django.db import models
from django.contrib.contenttypes.models import ContentType
from ..mixins import BaseSpecs
from ..base import Product


class ProcessorSpecs(BaseSpecs):
    CATEGORY_SLUG = 'processor'

    # Общие параметры
    includes_cooler = models.BooleanField(
        "Кулер в комплекте",
        default=False,
        help_text="Отметьте, если процессор включает кулер"
    )
    thermal_interface = models.BooleanField(
        "Термоинтерфейс в комплекте",
        default=False
    )

    # Ядро и архитектура
    socket = models.CharField(
        "Сокет",
        max_length=50,
        default="—",  # Прочерк для пустых значений
        help_text="Например: AM5"
    )
    cores = models.PositiveIntegerField(
        "Общее количество ядер",
        default=0,  # Значение по умолчанию
        help_text="Физические ядра"
    )
    performance_cores = models.PositiveIntegerField(
        "Производительные ядра",
        default=0
    )
    efficiency_cores = models.PositiveIntegerField(
        "Энергоэффективные ядра",
        default=0
    )
    threads = models.PositiveIntegerField(
        "Максимальное число потоков",
        default=0  # Значение по умолчанию
    )
    l2_cache = models.CharField(
        "Кэш L2",
        max_length=20,
        default="—",
        help_text="Например: 6 МБ"
    )
    l3_cache = models.CharField(
        "Кэш L3",
        max_length=20,
        default="—",
        help_text="Например: 32 МБ"
    )
    lithography = models.CharField(
        "Техпроцесс",
        max_length=50,
        default="—",
        help_text="Например: TSMC 5nm FinFET"
    )
    core_name = models.CharField(
        "Архитектура ядра",
        max_length=50,
        default="—",
        help_text="Например: AMD Raphael"
    )

    # Частота и разгон
    base_freq = models.FloatField(
        "Базовая частота (ГГц)",
        default=0.0  # Значение по умолчанию
    )
    max_turbo_freq = models.FloatField(
        "Макс. турбо-частота (ГГц)",
        default=0.0
    )
    efficiency_base_freq = models.FloatField(
        "Базовая частота эн. ядер",
        default=0.0
    )
    efficiency_turbo_freq = models.FloatField(
        "Турбо-частота эн. ядер",
        default=0.0
    )
    multiplier_unlocked = models.BooleanField(
        "Разблокированный множитель",
        default=False
    )

    # Память
    memory_type = models.CharField(
        "Тип памяти",
        max_length=50,
        default="—",
        help_text="Например: DDR5"
    )
    max_memory = models.PositiveIntegerField(
        "Макс. объем памяти (ГБ)",
        default=0
    )
    memory_channels = models.PositiveIntegerField(
        "Количество каналов",
        default=2
    )
    memory_frequency = models.CharField(
        "Частота памяти",
        max_length=20,
        default="—",
        help_text="Например: DDR5-5200"
    )
    ecc_support = models.BooleanField(
        "Поддержка ECC",
        default=False
    )

    # Тепловые характеристики
    tdp = models.PositiveIntegerField(
        "TDP (Вт)",
        default=0
    )
    base_tdp = models.PositiveIntegerField(
        "Базовое тепловыделение",
        default=65
    )
    max_temp = models.PositiveIntegerField(
        "Макс. температура (°C)",
        default=0
    )

    # Графика
    integrated_gpu = models.BooleanField(
        "Интегрированная графика",
        default=False
    )

    # Шина
    pcie_version = models.CharField(
        "Версия PCI Express",
        max_length=50,
        default="—"
    )
    pcie_lanes = models.PositiveIntegerField(
        "Число линий PCIe",
        default=24
    )

    # Дополнительно
    virtualization = models.BooleanField(
        "Виртуализация",
        default=True
    )
    features = models.TextField(
        "Особенности",
        blank=True,
        default="—",  # Значение по умолчанию для TextField
        help_text="Например: поддержка AMD EXPO"
    )

    class Meta:
        verbose_name = "Характеристики процессора"
        verbose_name_plural = "Характеристики процессоров"
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                name="unique_processor_specs"
            )
        ]

    def get_grouped_specs(self):
        return {
            **self.product.get_base_specs(),
            "Ядро и архитектура": {
                "Сокет": self.socket,
                "Общие ядра": self.cores,
                "Производительные ядра": self.performance_cores,
                "Энергоэффективные ядра": self.efficiency_cores,
                "Потоки": self.threads,
                "Кэш L2": self.l2_cache,
                "Кэш L3": self.l3_cache,
                "Техпроцесс": self.lithography,
                "Архитектура ядра": self.core_name
            },
            "Частота и разгон": {
                "Базовая частота": f"{self.base_freq} ГГц",
                "Макс. турбо-частота": f"{self.max_turbo_freq} ГГц",
                "Частота эн. ядер": f"{self.efficiency_base_freq} ГГц",
                "Турбо эн. ядер": f"{self.efficiency_turbo_freq} ГГц",
                "Разблокированный множитель": "Да" if self.multiplier_unlocked else "Нет"
            },
            "Память": {
                "Тип памяти": self.memory_type,
                "Макс. объем": f"{self.max_memory} ГБ",
                "Каналы": self.memory_channels,
                "Частота": self.memory_frequency,
                "ECC": "Да" if self.ecc_support else "Нет"
            },
            "Тепловые характеристики": {
                "TDP": f"{self.tdp} Вт",
                "Базовое TDP": f"{self.base_tdp} Вт",
                "Макс. температура": f"{self.max_temp} °C"
            },
            "Графика": {
                "Интегрированная графика": "Да" if self.integrated_gpu else "Нет"
            },
            "Шина": {
                "PCI Express": self.pcie_version,
                "Линии PCIe": self.pcie_lanes
            },
            "Дополнительно": {
                "Виртуализация": "Да" if self.virtualization else "Нет",
                "Особенности": self.features or "—"
            }
        }
