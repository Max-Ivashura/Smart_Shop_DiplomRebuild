from django.db import models
from ..mixins import BaseSpecs
from ..base import Product


class MotherboardSpecs(BaseSpecs):
    CATEGORY_SLUG = 'motherboards'

    # Общие параметры
    color = models.CharField(
        "Цвет",
        max_length=50,
        default="черный"
    )

    # Форм-фактор и размеры
    form_factor = models.CharField(
        "Форм-фактор",
        max_length=50,
        default="—",  # Добавлено
        help_text="Например: Standard-ATX"
    )
    dimensions = models.CharField(
        "Размеры (ШхВ)",
        max_length=50,
        default="—",  # Добавлено
        help_text="Например: 305x244 мм"
    )

    # Процессор и чипсет
    socket = models.CharField(
        "Сокет",
        max_length=50,
        default="—",  # Добавлено
        help_text="Например: AM5"
    )
    chipset = models.CharField(
        "Чипсет",
        max_length=50,
        default="—",  # Добавлено
        help_text="Например: AMD B650"
    )
    compatible_cores = models.CharField(
        "Совместимые ядра",
        max_length=100,
        blank=True
    )

    # Память
    memory_type = models.CharField(
        "Тип памяти",
        max_length=50,
        default="—",  # Добавлено
        help_text="Например: DDR5"
    )
    memory_slots = models.PositiveIntegerField(
        "Слоты памяти",
        default=0  # Добавлено
    )
    memory_channels = models.PositiveIntegerField(
        "Каналы памяти",
        default=2
    )
    max_memory = models.PositiveIntegerField(
        "Макс. объем памяти (ГБ)",
        default=0  # Добавлено
    )
    base_memory_freq = models.PositiveIntegerField(
        "Базовая частота (МГц)",
        default=0  # Добавлено
    )
    oc_memory_freq = models.CharField(
        "Частота в разгоне",
        max_length=200,
        default="—",  # Добавлено
        help_text="Перечислите через запятую"
    )

    # Слоты расширения
    pcie_version = models.CharField(
        "PCI Express",
        max_length=50,
        default="—"  # Добавлено
    )
    pcie_x16_slots = models.TextField(
        "Слоты PCIe x16",
        default="—"  # Добавлено
    )
    multi_gpu_support = models.CharField(
        "Поддержка Multi-GPU",
        max_length=50,
        blank=True
    )
    pcie_x1_slots = models.PositiveIntegerField(
        "Слоты PCIe x1",
        default=0
    )

    # Накопители
    m2_slots = models.PositiveIntegerField(
        "Разъемы M.2",
        default=0  # Добавлено
    )
    m2_details = models.TextField(
        "Конфигурация M.2",
        blank=True
    )
    sata_ports = models.PositiveIntegerField(
        "Порты SATA",
        default=0  # Добавлено
    )
    nvme_raid = models.CharField(
        "NVMe RAID",
        max_length=50,
        blank=True
    )

    # Порты и разъемы
    usb_ports = models.TextField(
        "Порты USB",
        default="—",  # Добавлено
        help_text="Формат: Type-A: 3x USB 3.2 Gen2"
    )
    video_ports = models.CharField(
        "Видеовыходы",
        max_length=100,
        blank=True
    )
    audio_ports = models.PositiveIntegerField(
        "Аудиоразъемы",
        default=0  # Добавлено
    )
    internal_headers = models.TextField(
        "Внутренние разъемы",
        default="—",  # Добавлено
        help_text="USB/ARGB/RGB/вентиляторы"
    )

    # Сеть и аудио
    lan_speed = models.CharField(
        "Скорость LAN",
        max_length=50,
        default="—"  # Добавлено
    )
    wifi = models.CharField(
        "Wi-Fi",
        max_length=50,
        blank=True
    )
    bluetooth = models.CharField(
        "Bluetooth",
        max_length=50,
        blank=True
    )
    audio_chipset = models.CharField(
        "Звуковой чип",
        max_length=100,
        default="—"  # Добавлено
    )

    # Питание
    power_phases = models.CharField(
        "Фазы питания",
        max_length=50,
        default="—"  # Добавлено
    )
    cooling = models.TextField(
        "Охлаждение",
        default="—",  # Добавлено
        help_text="Пассивное/активное"
    )

    # Дополнительно
    bios_features = models.TextField(
        "BIOS и управление",
        blank=True
    )
    layers = models.PositiveIntegerField(
        "Слои PCB",
        default=6
    )
    features = models.TextField(
        "Особенности",
        default="—",  # Добавлено
        help_text="Например: TPM 2.0, AMD EXPO"
    )

    class Meta:
        verbose_name = "Характеристики материнской платы"
        verbose_name_plural = "Характеристики материнских плат"
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                name="unique_motherboard_specs"
            )
        ]

    def get_grouped_specs(self):
        return {
            **self.product.get_base_specs(),
            "Форм-фактор": {
                "Тип": self.form_factor,
                "Размеры": self.dimensions,
                "Цвет": self.color
            },
            "Процессорная платформа": {
                "Сокет": self.socket,
                "Чипсет": self.chipset,
                "Совместимые ядра": self.compatible_cores or "—"  # Обновлено
            },
            "Память": {
                "Тип": self.memory_type,
                "Слоты": self.memory_slots if self.memory_slots else "—",  # Обновлено
                "Каналы": self.memory_channels,
                "Макс. объем": f"{self.max_memory} ГБ" if self.max_memory else "—",  # Обновлено
                "Базовая частота": f"{self.base_memory_freq} МГц" if self.base_memory_freq else "—",  # Обновлено
                "Разгон": self.oc_memory_freq
            },
            "Расширение": {
                "PCIe версия": self.pcie_version,
                "Слоты x16": self.pcie_x16_slots,
                "Multi-GPU": self.multi_gpu_support or "—",  # Обновлено
                "Слоты x1": self.pcie_x1_slots if self.pcie_x1_slots else "—"  # Обновлено
            },
            "Накопители": {
                "M.2 слоты": self.m2_slots if self.m2_slots else "—",  # Обновлено
                "M.2 конфигурация": self.m2_details or "—",  # Обновлено
                "SATA порты": self.sata_ports if self.sata_ports else "—",  # Обновлено
                "NVMe RAID": self.nvme_raid or "—"  # Обновлено
            },
            "Интерфейсы": {
                "USB порты": self.usb_ports,
                "Видеовыходы": self.video_ports or "—",  # Обновлено
                "Аудио": f"{self.audio_ports} каналов" if self.audio_ports else "—",  # Обновлено
                "Внутренние разъемы": self.internal_headers
            },
            "Связь": {
                "LAN": self.lan_speed,
                "Wi-Fi": self.wifi or "—",  # Обновлено
                "Bluetooth": self.bluetooth or "—",  # Обновлено
                "Звук": self.audio_chipset
            },
            "Питание": {
                "Фазы": self.power_phases,
                "Охлаждение": self.cooling
            },
            "Дополнительно": {
                "BIOS": self.bios_features or "—",  # Обновлено
                "Слои платы": self.layers,
                "Особенности": self.features
            }
        }