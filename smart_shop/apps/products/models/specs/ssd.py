from django.db import models
from ..mixins import BaseSpecs
from ..base import Product


class SSDSpecs(BaseSpecs):
    CATEGORY_SLUG = 'ssds'

    # Основные характеристики
    capacity = models.PositiveIntegerField(
        "Объем накопителя (ГБ)",
        default=0  # Добавлено
    )
    interface = models.CharField(
        "Интерфейс",
        max_length=50,
        default="SATA"
    )
    nvme = models.BooleanField(
        "NVMe",
        default=False
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
        default="—",  # Добавлено
        help_text="Например: 3D NAND"
    )
    dram_buffer = models.BooleanField(
        "DRAM буфер",
        default=False
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
    shock_resistance = models.PositiveIntegerField(
        "Ударопрочность",
        default=0,  # Добавлено
        help_text="G-сила"
    )

    # Энергопотребление
    power_consumption = models.FloatField(
        "Энергопотребление (Вт)",
        default=0.0  # Добавлено
    )

    # Габариты
    width = models.PositiveIntegerField(
        "Ширина (мм)",
        default=0  # Добавлено
    )
    length = models.PositiveIntegerField(
        "Длина (мм)",
        default=0  # Добавлено
    )
    thickness = models.PositiveIntegerField(
        "Толщина (мм)",
        default=0  # Добавлено
    )
    weight = models.PositiveIntegerField(
        "Вес (г)",
        default=0  # Добавлено
    )

    class Meta:
        verbose_name = "Характеристики SSD"
        verbose_name_plural = "Характеристики SSD"
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                name="unique_ssd_specs"
            )
        ]

    def get_grouped_specs(self):
        return {
            **self.product.get_base_specs(),
            "Основные параметры": {
                "Объем": f"{self.capacity} ГБ" if self.capacity else "—",  # Обновлено
                "Интерфейс": self.interface,
                "NVMe": "Да" if self.nvme else "Нет"
            },
            "Конфигурация": {
                "Контроллер": self.controller,
                "Тип ячеек": self.cell_type,
                "Структура памяти": self.memory_structure,
                "DRAM буфер": "Да" if self.dram_buffer else "Нет"
            },
            "Производительность": {
                "Чтение": f"{self.read_speed} МБ/с" if self.read_speed else "—",  # Обновлено
                "Запись": f"{self.write_speed} МБ/с" if self.write_speed else "—"  # Обновлено
            },
            "Надежность": {
                "TBW": f"{self.tbw} ТБ" if self.tbw else "—",  # Обновлено
                "DWPD": f"{self.dwpd}" if self.dwpd else "—",  # Обновлено
                "Ударопрочность": f"{self.shock_resistance} G" if self.shock_resistance else "—"  # Обновлено
            },
            "Дополнительно": {
                "Энергопотребление": f"{self.power_consumption} Вт" if self.power_consumption else "—",  # Обновлено
                "Габариты": (
                    f"{self.width}x{self.length}x{self.thickness} мм"
                    if self.width or self.length or self.thickness
                    else "—"
                ),
                "Вес": f"{self.weight} г" if self.weight else "—"  # Обновлено
            }
        }