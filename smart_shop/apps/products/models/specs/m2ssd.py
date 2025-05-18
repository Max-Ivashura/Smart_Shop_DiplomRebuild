from django.db import models
from ..mixins import BaseSpecs
from ..base import Product


class M2SSDSpecs(BaseSpecs):
    CATEGORY_SLUG = 'm2ssd'

    # Основные характеристики
    capacity = models.PositiveIntegerField(
        "Объем накопителя (ГБ)",
        default=0  # Добавлено
    )
    form_factor = models.CharField(
        "Форм-фактор",
        max_length=50,
        default="2280"
    )
    interface = models.CharField(
        "Интерфейс",
        max_length=50,
        default="—",  # Добавлено
        help_text="Например: PCIe 3.0 x4"
    )
    m2_key = models.CharField(
        "Ключ разъема",
        max_length=5,
        default="M"
    )
    nvme = models.BooleanField(
        "NVMe",
        default=True
    )

    # Конфигурация
    controller = models.CharField(
        "Контроллер",
        max_length=100,
        default="—"  # Добавлено
    )
    cell_type = models.CharField(
        "Тип ячеек",
        max_length=50,
        default="—",  # Добавлено
        help_text="Например: 3 бит TLC"
    )
    memory_structure = models.CharField(
        "Структура памяти",
        max_length=50,
        default="3D NAND"
    )
    dram_buffer = models.BooleanField(
        "DRAM буфер",
        default=True
    )
    dram_size = models.PositiveIntegerField(
        "Объем DRAM (МБ)",
        null=True,
        default=0  # Добавлено
    )

    # Производительность
    read_speed = models.PositiveIntegerField(
        "Скорость чтения (МБ/с)",
        default=0  # Добавлено
    )
    write_speed = models.PositiveIntegerField(
        "Скорость записи (МБ/с)",
        default=0  # Добавлено
    )

    # Надежность
    tbw = models.PositiveIntegerField(
        "TBW",
        default=0,  # Добавлено
        help_text="Максимальный ресурс записи в ТБ"
    )
    dwpd = models.FloatField(
        "DWPD",
        default=0.0,  # Добавлено
        help_text="Daily Write Probability"
    )

    # Дополнительно
    heatsink = models.BooleanField(
        "Радиатор в комплекте",
        default=False
    )
    power_consumption = models.FloatField(
        "Энергопотребление (Вт)",
        default=0.0  # Добавлено
    )

    # Габариты
    length = models.PositiveIntegerField(
        "Длина (мм)",
        default=0  # Добавлено
    )
    width = models.PositiveIntegerField(
        "Ширина (мм)",
        default=22
    )
    thickness = models.FloatField(
        "Толщина (мм)",
        default=0.0  # Добавлено
    )
    weight = models.PositiveIntegerField(
        "Вес (г)",
        default=0  # Добавлено
    )

    class Meta:
        verbose_name = "Характеристики M.2 NVMe"
        verbose_name_plural = "Характеристики M.2 NVMe"
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                name="unique_m2ssd_specs"
            )
        ]

    def get_grouped_specs(self):
        return {
            **self.product.get_base_specs(),
            "Основные параметры": {
                "Объем": f"{self.capacity} ГБ" if self.capacity else "—",  # Обновлено
                "Форм-фактор": self.form_factor,
                "Интерфейс": self.interface,
                "Ключ": self.m2_key,
                "NVMe": "Да" if self.nvme else "Нет"
            },
            "Конфигурация": {
                "Контроллер": self.controller,
                "Тип ячеек": self.cell_type,
                "Структура памяти": self.memory_structure,
                "DRAM буфер": (
                    f"{self.dram_size} МБ"
                    if self.dram_buffer and self.dram_size
                    else "Нет"
                )
            },
            "Производительность": {
                "Чтение": f"{self.read_speed} МБ/с" if self.read_speed else "—",  # Обновлено
                "Запись": f"{self.write_speed} МБ/с" if self.write_speed else "—"  # Обновлено
            },
            "Надежность": {
                "TBW": f"{self.tbw} ТБ" if self.tbw else "—",  # Обновлено
                "DWPD": f"{self.dwpd}" if self.dwpd else "—"  # Обновлено
            },
            "Дополнительно": {
                "Радиатор": "Да" if self.heatsink else "Нет",
                "Энергопотребление": (
                    f"{self.power_consumption} Вт"
                    if self.power_consumption
                    else "—"
                ),
                "Габариты": (
                    f"{self.length}x{self.width}x{self.thickness} мм"
                    if self.length or self.width or self.thickness
                    else "—"
                ),
                "Вес": f"{self.weight} г" if self.weight else "—"  # Обновлено
            }
        }