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
        self.cpu = next((c for c in self.components if c.category.slug == "processors"), None)
        self.motherboard = next((c for c in self.components if c.category.slug == "motherboards"), None)
        self.ram = [c for c in self.components if c.category.slug == "rams"]
        self.gpu = next((c for c in self.components if c.category.slug == "videocards"), None)
        self.psu = next((c for c in self.components if c.category.slug == "psus"), None)
        self.case = next((c for c in self.components if c.category.slug == "cases"), None)
        self.cooler = next((c for c in self.components if c.category.slug == "coolers"), None)
        self.storage = [c for c in self.components if c.category.slug in ["ssds", "hdds", "m2ssds"]]

    def _get_spec_value(self, product: Product, spec_name: str):
        """Получить значение характеристики из спецификаций продукта."""
        category_slug = product.category.slug
        specs = getattr(product, f"{category_slug}specs_specs", None)
        return getattr(specs, spec_name, None) if specs else None

    def _check_cpu_motherboard_socket(self):
        """Сокет процессора ↔ материнская плата."""
        if self.cpu and self.motherboard:
            cpu_socket = self._get_spec_value(self.cpu, "socket")
            mb_socket = self._get_spec_value(self.motherboard, "socket")
            if cpu_socket != mb_socket:
                self.errors["cpu"] = f"Сокет процессора ({cpu_socket}) не совместим с материнской платой ({mb_socket})."

    def _check_ram_motherboard(self):
        """Тип/частота ОЗУ ↔ материнская плата."""
        if self.ram and self.motherboard:
            ram_type = self._get_spec_value(self.ram[0], "memory_type")
            mb_ram_type = self._get_spec_value(self.motherboard, "memory_type")
            if ram_type != mb_ram_type:
                self.errors["ram"] = f"Тип памяти {ram_type} не поддерживается материнской платой ({mb_ram_type})."

    def _check_case_motherboard_form_factor(self):
        """Форм-фактор корпуса ↔ материнская плата."""
        if self.motherboard and self.case:
            mb_form_factor = self._get_spec_value(self.motherboard, "form_factor").lower()
            case_supported = self._get_spec_value(self.case, "motherboard_form_factors").lower()
            if mb_form_factor not in case_supported:
                self.errors["case"] = f"Корпус не поддерживает форм-фактор {mb_form_factor}."

    def _check_gpu_case_length(self):
        """Длина видеокарты ↔ корпус."""
        if self.gpu and self.case:
            gpu_length = self._get_spec_value(self.gpu, "length") or 0
            case_max_gpu = self._get_spec_value(self.case, "max_gpu_length") or 0
            if gpu_length > case_max_gpu:
                self.errors[
                    "gpu"] = f"Длина видеокарты ({gpu_length} мм) превышает допустимую для корпуса ({case_max_gpu} мм)."

    def _check_psu_wattage(self):
        """Мощность БП ↔ потребление компонентов."""
        if self.psu:
            psu_wattage = self._get_spec_value(self.psu, "wattage") or 0
            total_power = (
                    (self._get_spec_value(self.cpu, "tdp") or 0)
                    + (self._get_spec_value(self.gpu, "tdp") or 0)
                    + 100  # Пример: запас на остальные компоненты
            )
            if psu_wattage < total_power * 1.2:
                self.errors[
                    "psu"] = f"Блок питания {psu_wattage} Вт недостаточен (рекомендуется от {total_power * 1.2} Вт)."

    def _check_cooler_socket(self):
        """Совместимость кулера ↔ сокет процессора."""
        if self.cooler and self.cpu:
            cooler_sockets = self._get_spec_value(self.cooler, "socket_support") or ""
            cpu_socket = self._get_spec_value(self.cpu, "socket") or ""
            if cpu_socket.lower() not in cooler_sockets.lower():
                self.errors["cooler"] = f"Кулер не поддерживает сокет {cpu_socket}."

    def _check_m2_slots(self):
        """Количество M.2 слотов ↔ материнская плата."""
        m2_drives = [c for c in self.storage if c.category.slug == "m2ssds"]
        if self.motherboard and m2_drives:
            m2_slots = self._get_spec_value(self.motherboard, "m2_slots") or 0
            if len(m2_drives) > m2_slots:
                self.errors["storage"] = f"Недостаточно M.2 слотов (нужно {len(m2_drives)}, доступно {m2_slots})."

    def _check_required_components(self):
        """Проверка наличия обязательных компонентов."""
        required = {
            "cpu": ("Процессор", self.cpu),
            "motherboard": ("Материнская плата", self.motherboard),
            "ram": ("ОЗУ", self.ram),
            "psu": ("Блок питания", self.psu),
            "case": ("Корпус", self.case)
        }
        for key, (name, component) in required.items():
            if not component:
                self.errors[key] = f"Не выбран обязательный компонент: {name}."
            elif key == "ram" and len(component) == 0:
                self.errors[key] = "Добавьте хотя бы один модуль ОЗУ."

    def _check_ram_frequency(self):
        """Совместимость частоты ОЗУ ↔ материнская плата."""
        if self.ram and self.motherboard:
            max_supported = (
                    self._get_spec_value(self.motherboard, "oc_memory_freq") or
                    self._get_spec_value(self.motherboard, "base_memory_freq")
            )
            if not max_supported:
                return

            try:
                max_supported = max([int(freq.strip()) for freq in max_supported.split(",")])
            except:
                return

            for ram in self.ram:
                ram_freq = self._get_spec_value(ram, "frequency") or 0
                if ram_freq > max_supported:
                    self.errors["ram"] = (
                        f"ОЗУ {ram_freq} МГц превышает поддерживаемую "
                        f"материнской платой ({max_supported} МГц)."
                    )

    def _check_psu_connectors(self):
        """Проверка разъемов БП."""
        if self.psu and self.motherboard and self.gpu:
            # Проверка основного 24-pin разъема
            if not self._get_spec_value(self.psu, "main_connector"):
                self.errors["psu"] = "БП не имеет основного 24-pin разъема."

            # Проверка CPU 8-pin
            cpu_connectors = self._get_spec_value(self.psu, "cpu_connectors") or 0
            if cpu_connectors < 1:
                self.errors["psu"] = "БП должен иметь минимум 1 CPU 8-pin разъем."

            # Проверка PCI-E для видеокарты
            required_pcie = self._get_spec_value(self.gpu, "power_connectors_count") or 1
            available_pcie = self._get_spec_value(self.psu, "pcie_connectors") or 0
            if available_pcie < required_pcie:
                self.errors["psu"] = (
                    f"Видеокарте требуется {required_pcie} PCI-E разъемов, "
                    f"доступно {available_pcie}."
                )

    def _check_cooler_height(self):
        """Совместимость высоты кулера ↔ корпус."""
        if self.cooler and self.case:
            cooler_height = self._get_spec_value(self.cooler, "height") or 0
            case_max_height = self._get_spec_value(self.case, "max_cooler_height") or 0
            if cooler_height > case_max_height:
                self.errors["cooler"] = (
                    f"Высота кулера ({cooler_height} мм) "
                    f"превышает допустимую для корпуса ({case_max_height} мм)."
                )

    def _check_pcie_versions(self):
        """Совместимость версий PCIe."""
        if self.motherboard and (self.gpu or any(s.category.slug == "m2ssds" for s in self.storage)):
            mb_pcie_version = self._get_spec_value(self.motherboard, "pcie_version")

            if self.gpu:
                gpu_pcie = self._get_spec_value(self.gpu, "pcie_version")
                if gpu_pcie > mb_pcie_version:
                    self.errors["gpu"] = (
                        f"Видеокарта требует PCIe {gpu_pcie}, "
                        f"материнская плата поддерживает {mb_pcie_version}."
                    )

            for m2 in filter(lambda s: s.category.slug == "m2ssds", self.storage):
                m2_pcie = self._get_spec_value(m2, "interface").split(" ")[1]  # Пример: "PCIe 4.0 x4"
                if float(m2_pcie) > float(mb_pcie_version):
                    self.errors["storage"] = (
                        f"NVMe SSD требует PCIe {m2_pcie}, "
                        f"материнская плата поддерживает {mb_pcie_version}."
                    )

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
            self._check_pcie_versions
        ]
        for check in checks:
            check()
        return self.errors
