from django.contrib import admin
from ..models.specs.hdd import HardDriveSpecs


@admin.register(HardDriveSpecs)
class HardDriveSpecsAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "capacity",
        "interface",
        "spindle_speed",
        "cache_size",
        "raid_support",
        "recording_tech",
        "helium"
    )
    list_filter = (
        "interface",
        "raid_support",
        "recording_tech",
        "helium",
        "spindle_speed"
    )
    search_fields = (
        "product__name",
        "interface",
        "recording_tech",
        "cache_size"
    )
    raw_id_fields = ("product",)
    fieldsets = (
        ("Основные параметры", {
            "fields": (
                "product",
                "capacity",
                "cache_size",
                "spindle_speed"
            )
        }),
        ("Интерфейс", {
            "fields": (
                "interface",
                "interface_speed",
                "raid_support",
            )
        }),
        ("Надежность и механика", {
            "fields": (
                "recording_tech",
                "shock_resistance",
                "workload",
                "helium",
            )
        }),
        ("Шумовые характеристики", {
            "fields": (
                "noise_operating",
                "noise_idle",
            )
        }),
        ("Производительность", {
            "fields": (
                "transfer_rate",
                "latency",
            )
        }),
        ("Энергопотребление", {
            "fields": (
                "max_power",
                "idle_power",
                "max_temp",
            )
        }),
        ("Габариты", {
            "fields": (
                "width",
                "length",
                "thickness",
                "weight",
            )
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("product")