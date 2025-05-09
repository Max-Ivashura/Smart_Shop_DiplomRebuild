from django.db import models
from ..mixins import BaseSpecs
from ..base import Product


class HardDriveSpecs(BaseSpecs):
    CATEGORY_SLUG = 'hdds'

    # Основные параметры
    capacity = models.PositiveIntegerField(
        "Объем накопителя (ТБ)",
        default=0  # Добавлено
    )
    cache_size = models.PositiveIntegerField(
        "Кэш-память (МБ)",
        default=0  # Добавлено
    )
    spindle_speed = models.PositiveIntegerField(
        "Скорость вращения (об/мин)",
        default=0  # Добавлено
    )

    # Интерфейс
    interface = models.CharField(
        "Интерфейс",
        max_length=50,
        default="SATA III"
    )
    interface_speed = models.CharField(
        "Пропускная способность",
        max_length=50,
        default="6 Гбит/с"
    )
    raid_support = models.BooleanField(
        "Поддержка RAID",
        default=False
    )

    # Механика и надежность
    recording_tech = models.CharField(
        "Технология записи",
        max_length=3,
        choices=[('CMR', 'CMR'), ('SMR', 'SMR')],
        default='CMR'  # Добавлено
    )
    shock_resistance = models.PositiveIntegerField(
        "Ударостойкость (G)",
        default=0  # Добавлено
    )
    workload = models.PositiveIntegerField(
        "Циклов парковки (тыс.)",
        default=0,  # Добавлено
        help_text="В тысячах циклов"
    )
    helium = models.BooleanField(
        "Гелиевое наполнение",
        default=False
    )

    # Шум
    noise_operating = models.PositiveIntegerField(
        "Шум при работе (дБ)",
        default=0  # Добавлено
    )
    noise_idle = models.PositiveIntegerField(
        "Шум в простое (дБ)",
        default=0  # Добавлено
    )

    # Производительность
    transfer_rate = models.PositiveIntegerField(
        "Макс. скорость передачи (МБ/с)",
        default=0  # Добавлено
    )
    latency = models.FloatField(
        "Задержка (мс)",
        default=0.0  # Добавлено
    )

    # Энергопотребление
    max_power = models.FloatField(
        "Макс. энергопотребление (Вт)",
        default=0.0  # Добавлено
    )
    idle_power = models.FloatField(
        "Энергопотребление в простое (Вт)",
        default=0.0  # Добавлено
    )
    max_temp = models.PositiveIntegerField(
        "Макс. температура (°C)",
        default=0  # Добавлено
    )

    # Габариты
    width = models.FloatField(
        "Ширина (мм)",
        default=0.0  # Добавлено
    )
    length = models.FloatField(
        "Длина (мм)",
        default=0.0  # Добавлено
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
        verbose_name = "Характеристики HDD"
        verbose_name_plural = "Характеристики жестких дисков"
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                name="unique_hdd_specs"
            )
        ]

    def get_grouped_specs(self):
        return {
            **self.product.get_base_specs(),
            "Основные параметры": {
                "Объем": f"{self.capacity} ТБ" if self.capacity else "—",  # Обновлено
                "Кэш-память": f"{self.cache_size} МБ" if self.cache_size else "—",  # Обновлено
                "Скорость вращения": f"{self.spindle_speed} об/мин" if self.spindle_speed else "—"  # Обновлено
            },
            "Интерфейс": {
                "Тип": self.interface,
                "Скорость": self.interface_speed,
                "RAID поддержка": "Да" if self.raid_support else "Нет"
            },
            "Надежность": {
                "Технология записи": self.get_recording_tech_display(),
                "Ударостойкость": f"{self.shock_resistance} G" if self.shock_resistance else "—",  # Обновлено
                "Циклов парковки": f"{self.workload * 1000}" if self.workload else "—",  # Обновлено
                "Гелий": "Да" if self.helium else "Нет"
            },
            "Шумовые характеристики": {
                "Работа": f"{self.noise_operating} дБ" if self.noise_operating else "—",  # Обновлено
                "Покой": f"{self.noise_idle} дБ" if self.noise_idle else "—"  # Обновлено
            },
            "Производительность": {
                "Скорость передачи": f"{self.transfer_rate} МБ/с" if self.transfer_rate else "—",  # Обновлено
                "Задержка": f"{self.latency} мс" if self.latency else "—"  # Обновлено
            },
            "Энергопотребление": {
                "Максимальное": f"{self.max_power} Вт" if self.max_power else "—",  # Обновлено
                "Режим ожидания": f"{self.idle_power} Вт" if self.idle_power else "—",  # Обновлено
                "Макс. температура": f"{self.max_temp}°C" if self.max_temp else "—"  # Обновлено
            },
            "Габариты": {
                "Размеры": (
                    f"{self.width}x{self.length}x{self.thickness} мм"
                    if self.width or self.length or self.thickness
                    else "—"
                ),
                "Вес": f"{self.weight} г" if self.weight else "—"  # Обновлено
            }
        }