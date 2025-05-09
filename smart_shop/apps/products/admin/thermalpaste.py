from django.contrib import admin
from ..models.specs.thermalpaste import ThermalPasteSpecs


@admin.register(ThermalPasteSpecs)
class ThermalPasteSpecsAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "weight",
        "thermal_conductivity",
        "packaging",
        "temperature_range"
    )
    list_filter = (
        "packaging",
    )
    search_fields = (
        "product__name",
        "packaging",
        "thermal_conductivity"
    )
    raw_id_fields = ("product",)
    fieldsets = (
        ("Общие параметры", {
            "fields": (
                "product",
                "weight",
                "packaging"
            )
        }),
        ("Тепловые характеристики", {
            "fields": (
                "thermal_conductivity",
                "min_temp",
                "max_temp",
            )
        }),
    )

    def temperature_range(self, obj):
        return f"{obj.min_temp}°C ~ {obj.max_temp}°C"
    temperature_range.short_description = "Рабочий диапазон"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("product")