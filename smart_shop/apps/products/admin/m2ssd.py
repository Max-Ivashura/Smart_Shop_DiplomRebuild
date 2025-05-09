from django.contrib import admin
from ..models.specs.m2ssd import M2SSDSpecs


@admin.register(M2SSDSpecs)
class M2SSDSpecsAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "capacity",
        "form_factor",
        "interface",
        "nvme",
        "read_speed",
        "write_speed",
        "heatsink"
    )
    list_filter = (
        "interface",
        "nvme",
        "form_factor",
        "m2_key",
        "dram_buffer",
        "heatsink"
    )
    search_fields = (
        "product__name",
        "interface",
        "controller",
        "cell_type",
        "memory_structure"
    )
    raw_id_fields = ("product",)
    fieldsets = (
        ("Основные параметры", {
            "fields": (
                "product",
                "capacity",
                "form_factor",
                "interface",
                "m2_key",
                "nvme"
            )
        }),
        ("Конфигурация", {
            "fields": (
                "controller",
                "cell_type",
                "memory_structure",
                "dram_buffer",
                "dram_size"
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
            )
        }),
        ("Дополнительно", {
            "fields": (
                "heatsink",
                "power_consumption",
            )
        }),
        ("Габариты", {
            "fields": (
                "length",
                "width",
                "thickness",
                "weight",
            )
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("product")