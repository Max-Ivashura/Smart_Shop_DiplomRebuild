from django.contrib import admin
from ..models.specs.ssd import SSDSpecs


@admin.register(SSDSpecs)
class SSDSpecsAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "capacity",
        "interface",
        "nvme",
        "read_speed",
        "write_speed",
        "dram_buffer",
        "tbw"
    )
    list_filter = (
        "interface",
        "nvme",
        "dram_buffer",
        "memory_structure"
    )
    search_fields = (
        "product__name",
        "interface",
        "controller",
        "cell_type"
    )
    raw_id_fields = ("product",)
    fieldsets = (
        ("Основные параметры", {
            "fields": (
                "product",
                "capacity",
                "interface",
                "nvme"
            )
        }),
        ("Конфигурация", {
            "fields": (
                "controller",
                "cell_type",
                "memory_structure",
                "dram_buffer"
            )
        }),
        ("Производительность", {
            "fields": (
                "read_speed",
                "write_speed",
            )
        }),
        ("Надежность", {
            "fields": (
                "tbw",
                "dwpd",
                "shock_resistance"
            )
        }),
        ("Энергопотребление", {
            "fields": (
                "power_consumption",
            )
        }),
        ("Габариты", {
            "fields": (
                "width",
                "length",
                "thickness",
                "weight"
            )
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("product")