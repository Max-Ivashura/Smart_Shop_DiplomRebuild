from typing import Dict, List
from apps.products.models import Product


class CompatibilityChecker:
    """Класс для проверки совместимости компонентов сборки."""

    def __init__(self, components: List[Product]):
        self.components = components
        self.errors = {}
        self._init_components()

    def _init_components(self):
        """Инициализировать компоненты по категориям."""
        self.cpu = next((c for c in self.components if c.category.slug == "processor"), None)
        self.motherboard = next((c for c in self.components if c.category.slug == "motherboard"), None)
        self.ram = [c for c in self.components if c.category.slug == "ram"]
        self.gpu = next((c for c in self.components if c.category.slug == "videocard"), None)
        self.psu = next((c for c in self.components if c.category.slug == "psu"), None)
        self.case = next((c for c in self.components if c.category.slug == "case"), None)
        self.cooler = next((c for c in self.components if c.category.slug == "cooler"), None)
        self.storage = [c for c in self.components if c.category.slug in ["ssd", "hdd", "m2ssd"]]

    def _safe_float(self, value: str) -> float:
        """Преобразует строку в float, игнорируя нечисловые символы."""
        if not value:
            return 0.0
        try:
            # Удаляем все нецифровые символы, кроме точки и запятой
            cleaned = ''.join(filter(lambda x: x.isdigit() or x in {'.', ','}, str(value)))
            # Заменяем запятую на точку для корректного преобразования
            cleaned = cleaned.replace(',', '.')
            return float(cleaned)
        except ValueError:
            return 0.0

    def _get_spec_value(self, product: Product, spec_name: str):
        if not product:
            return None
        category_slug = product.category.slug
        specs = getattr(product, f"{category_slug}specs_specs", None)
        return getattr(specs, spec_name, None) if specs else None

    def _check_cpu_motherboard_socket(self):
        if self.cpu and self.motherboard:
            cpu_socket = self._get_spec_value(self.cpu, "socket")
            mb_socket = self._get_spec_value(self.motherboard, "socket")

            if not cpu_socket or not mb_socket:
                self.errors["cpu"] = "Не указан сокет процессора/материнской платы."
            elif cpu_socket != mb_socket:
                self.errors["cpu"] = f"Сокет процессора ({cpu_socket}) не совместим с материнской платой ({mb_socket})."

    def _check_ram_motherboard(self):
        """Тип/частота ОЗУ ↔ материнская плата."""
        if self.ram and self.motherboard:
            ram_type = self._get_spec_value(self.ram[0], "memory_type")
            mb_ram_type = self._get_spec_value(self.motherboard, "memory_type")

            if not ram_type or not mb_ram_type:
                self.errors["ram"] = "Не указан тип памяти (ОЗУ/материнская плата)."
            elif ram_type != mb_ram_type:
                self.errors["ram"] = f"Тип памяти {ram_type} не поддерживается материнской платой ({mb_ram_type})."

    def _check_case_motherboard_form_factor(self):
        """Форм-фактор корпуса ↔ материнская плата."""
        if self.motherboard and self.case:
            mb_form_factor = self._get_spec_value(self.motherboard, "form_factor")
            case_supported = self._get_spec_value(self.case, "motherboard_form_factors")

            if not mb_form_factor or not case_supported:
                self.errors["case"] = "Не указан форм-фактор (материнская плата/корпус)."
            elif mb_form_factor.lower() not in case_supported.lower():
                self.errors["case"] = f"Корпус не поддерживает форм-фактор {mb_form_factor}."

    def _check_gpu_case_length(self):
        """Длина видеокарты ↔ корпус."""
        if self.gpu and self.case:
            gpu_length = self._safe_float(self._get_spec_value(self.gpu, "length"))
            case_max_gpu = self._safe_float(self._get_spec_value(self.case, "max_gpu_length"))

            if gpu_length is None:
                self.errors["gpu"] = "Не указана длина видеокарты."
                return
            if case_max_gpu is None:
                self.errors["case"] = "Не указана максимальная длина видеокарты для корпуса."
                return

            if gpu_length > case_max_gpu:
                self.errors[
                    "gpu"] = f"Длина видеокарты ({gpu_length} мм) превышает допустимую для корпуса ({case_max_gpu} мм)."

    def _check_psu_wattage(self):
        """Мощность БП ↔ потребление компонентов."""
        if self.psu:
            psu_wattage = self._safe_float(self._get_spec_value(self.psu, "wattage")) or 0
            cpu_tdp = self._safe_float(self._get_spec_value(self.cpu, "tdp")) or 0 if self.cpu else 0
            gpu_tdp = self._safe_float(self._get_spec_value(self.gpu, "tdp")) or 0 if self.gpu else 0
            total_power = cpu_tdp + gpu_tdp + 100  # Запас

            if psu_wattage < total_power * 1.2:
                self.errors["psu"] = f"БП {psu_wattage} Вт недостаточен (рекомендуется от {total_power * 1.2} Вт)."

    def _check_cooler_socket(self):
        """Совместимость кулера ↔ сокет процессора."""
        if self.cooler and self.cpu:
            cooler_sockets = self._get_spec_value(self.cooler, "socket_support")
            cpu_socket = self._get_spec_value(self.cpu, "socket")

            if not cooler_sockets:
                self.errors["cooler"] = "Не указаны поддерживаемые сокеты для кулера."
                return
            if not cpu_socket:
                self.errors["cpu"] = "Не указан сокет процессора."
                return

            if cpu_socket.lower() not in cooler_sockets.lower():
                self.errors["cooler"] = f"Кулер не поддерживает сокет {cpu_socket}."

    def _check_m2_slots(self):
        """Количество M.2 слотов ↔ материнская плата."""
        m2_drives = [c for c in self.storage if c.category.slug == "m2ssds"]
        if self.motherboard and m2_drives:
            m2_slots = self._get_spec_value(self.motherboard, "m2_slots")
            if m2_slots is None:
                self.errors["storage"] = "Не указано количество M.2 слотов на материнской плате."
            elif len(m2_drives) > m2_slots:
                self.errors["storage"] = f"Недостаточно M.2 слотов (нужно {len(m2_drives)}, доступно {m2_slots})."

    def _check_required_components(self):
        required = {
            "cpu": ("Процессор", self.cpu),
            "motherboard": ("Материнская плата", self.motherboard),
            "ram": ("ОЗУ", self.ram),
            "psu": ("Блок питания", self.psu),
            "case": ("Корпус", self.case),
            "storage": ("Накопитель", self.storage),
            "cooler": ("Охлаждение", self.cooler)
        }

        for key, (name, component) in required.items():
            if key == "ram":
                if not component or len(component) == 0:
                    self.errors[key] = "Добавьте хотя бы один модуль ОЗУ."
            elif key == "storage":
                if not component or len(component) == 0:
                    self.errors[key] = "Добавьте накопитель (SSD/HDD)."
            elif not component:
                self.errors[key] = f"Не выбран обязательный компонент: {name}."

    def _check_ram_frequency(self):
        """Совместимость частоты ОЗУ ↔ материнская плата."""
        if self.ram and self.motherboard:
            # Получаем частоту материнской платы
            max_supported = (
                    self._get_spec_value(self.motherboard, "oc_memory_freq") or
                    self._get_spec_value(self.motherboard, "base_memory_freq")
            )

            if not max_supported:
                self.errors["ram"] = "Не указана поддерживаемая частота памяти (материнская плата)."
                return

            try:
                # Очищаем строку от нецифровых символов (например, "3200 МГц" → "3200")
                max_supported_clean = "".join(filter(str.isdigit, str(max_supported)))
                # Разбиваем на отдельные значения и преобразуем в числа
                max_supported_values = [int(freq.strip()) for freq in max_supported_clean.split(",")]
                max_supported = max(max_supported_values)
            except (ValueError, AttributeError):
                self.errors["ram"] = "Некорректный формат частоты памяти (материнская плата)."
                return

            # Проверяем каждую планку ОЗУ
            for ram in self.ram:
                ram_freq = self._get_spec_value(ram, "frequency")
                if not ram_freq:
                    continue

                # Очищаем частоту ОЗУ
                ram_freq_clean = int("".join(filter(str.isdigit, str(ram_freq))))
                if ram_freq_clean > max_supported:
                    self.errors["ram"] = f"ОЗУ {ram_freq_clean} МГц превышает поддерживаемую ({max_supported} МГц)."

    def _check_psu_connectors(self):
        if not self.psu:
            return

        # Основной 24-pin
        main_connector = self._get_spec_value(self.psu, "main_connector")
        if not main_connector:
            self.errors["psu"] = "БП не имеет основного 24-pin разъема."

        # CPU 8-pin
        cpu_connectors = self._get_spec_value(self.psu, "cpu_connectors")
        if cpu_connectors is None:
            self.errors["psu"] = "Не указано количество CPU 8-pin разъемов БП."
        elif cpu_connectors < 1:
            self.errors["psu"] = "БП должен иметь минимум 1 CPU 8-pin разъем."



    def _check_cooler_height(self):
        """Совместимость высоты кулера ↔ корпус."""
        if self.cooler and self.case:
            cooler_height = self._get_spec_value(self.cooler, "height")
            case_max_height = self._get_spec_value(self.case, "max_cooler_height")

            if cooler_height is None:
                self.errors["cooler"] = "Не указана высота кулера."
                return
            if case_max_height is None:
                self.errors["case"] = "Не указана максимальная высота кулера для корпуса."
                return

            if cooler_height > case_max_height:
                self.errors[
                    "cooler"] = f"Высота кулера ({cooler_height} мм) превышает допустимую ({case_max_height} мм)."

    def _check_pcie_versions(self):
        if not self.motherboard:
            return

        mb_pcie_version = self._safe_float(self._get_spec_value(self.motherboard, "pcie_version"))
        if not mb_pcie_version:
            self.errors["system"] = "Не указана версия PCIe материнской платы."
            return

        try:
            mb_pcie_version = float(mb_pcie_version)
        except (TypeError, ValueError):
            self.errors["system"] = "Некорректный формат версии PCIe материнской платы."
            return

        # Проверка для видеокарты
        if self.gpu:
            gpu_pcie = self._safe_float(self._get_spec_value(self.gpu, "pcie_version"))
            if gpu_pcie and float(gpu_pcie) > mb_pcie_version:
                self.errors["gpu"] = (
                    f"Видеокарта требует PCIe {gpu_pcie}, "
                    f"материнская плата поддерживает {mb_pcie_version}."
                )

        # Проверка для M.2 SSD
        for m2 in filter(lambda s: s.category.slug == "m2ssds", self.storage):
            m2_interface = self._safe_float(self._get_spec_value(m2, "interface")) or ""
            if "PCIe" not in m2_interface:
                continue

            try:
                m2_pcie = float(m2_interface.split(" ")[1])  # "PCIe 4.0 x4" -> 4.0
                if m2_pcie > mb_pcie_version:
                    self.errors["storage"] = (
                        f"NVMe SSD требует PCIe {m2_pcie}, "
                        f"материнская плата поддерживает {mb_pcie_version}."
                    )
            except (IndexError, ValueError):
                pass

    def _check_gpu_requirements(self):
        if not self.gpu:
            cpu_has_graphics = self._get_spec_value(self.cpu, "integrated_gpu")
            if not cpu_has_graphics:
                self.errors["gpu"] = "Не выбрана видеокарта, а процессор не имеет встроенной графики."

    def validate(self) -> Dict[str, str]:
        """Запустить все проверки."""
        checks = [
            self._check_required_components,
            self._check_cpu_motherboard_socket,
            self._check_ram_motherboard,
            self._check_ram_frequency,
            self._check_case_motherboard_form_factor,
            self._check_gpu_case_length,
            self._check_psu_wattage,
            self._check_psu_connectors,
            self._check_cooler_socket,
            self._check_cooler_height,
            self._check_m2_slots,
            self._check_pcie_versions,
            self._check_gpu_requirements,
        ]
        for check in checks:
            check()
        return self.errors
