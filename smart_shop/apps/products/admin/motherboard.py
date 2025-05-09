from django.contrib import admin
from ..models.specs.motherboard import MotherboardSpecs


@admin.register(MotherboardSpecs)
class MotherboardSpecsAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "form_factor",
        "socket",
        "chipset",
        "memory_type",
        "pcie_version",
        "m2_slots",
        "lan_speed",
        "wifi"
    )
    list_filter = (
        "form_factor",
        "socket",
        "chipset",
        "memory_type",
        "pcie_version",
        "m2_slots",
        "lan_speed",
        "wifi"
    )
    search_fields = (
        "product__name",
        "socket",
        "chipset",
        "form_factor",
        "memory_type",
        "pcie_version"
    )
    raw_id_fields = ("product",)
    fieldsets = (
        ("Основные параметры", {
            "fields": (
                "product",
                "color",
                "form_factor",
                "dimensions"
            )
        }),
        ("Процессор и чипсет", {
            "fields": (
                "socket",
                "chipset",
                "compatible_cores"
            )
        }),
        ("Память", {
            "fields": (
                "memory_type",
                "memory_slots",
                "memory_channels",
                "max_memory",
                "base_memory_freq",
                "oc_memory_freq"
            )
        }),
        ("Слоты расширения", {
            "fields": (
                "pcie_version",
                "pcie_x16_slots",
                "multi_gpu_support",
                "pcie_x1_slots"
            )
        }),
        ("Накопители", {
            "fields": (
                "m2_slots",
                "m2_details",
                "sata_ports",
                "nvme_raid"
            )
        }),
        ("Порты и разъемы", {
            "fields": (
                "usb_ports",
                "video_ports",
                "audio_ports",
                "internal_headers"
            )
        }),
        ("Сеть и аудио", {
            "fields": (
                "lan_speed",
                "wifi",
                "bluetooth",
                "audio_chipset"
            )
        }),
        ("Питание", {
            "fields": (
                "power_phases",
                "cooling"
            )
        }),
        ("Дополнительно", {
            "fields": (
                "bios_features",
                "layers",
                "features"
            )
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("product")