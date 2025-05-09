from django.contrib import admin
from ..models.specs.cooler import CoolerSpecs


@admin.register(CoolerSpecs)
class CoolerSpecsAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "construction_type",
        "tdp",
        "included_fans",
        "heat_pipes",
        "noise_level",
        "thermal_paste",
        "rgb_lighting"
    )
    list_filter = (
        "construction_type",
        "thermal_paste",
        "rgb_lighting",
        "bearing_type",
        "heatsink_material"
    )
    search_fields = (
        "product__name",
        "socket_support",
        "construction_type",
        "heatsink_material",
        "fan_size"
    )
    raw_id_fields = ("product",)
    fieldsets = (
        ("Основное", {
            "fields": (
                "product",
                "socket_support",
                "tdp",
                "construction_type"
            )
        }),
        ("Радиатор", {
            "fields": (
                "base_material",
                "heatsink_material",
                "heat_pipes",
                "pipe_diameter",
                "nickel_plating",
                "heatsink_color"
            )
        }),
        ("Вентилятор", {
            "fields": (
                "included_fans",
                "fan_size",
                "fan_connector",
                "max_rpm",
                "min_rpm",
                "airflow",
                "noise_level",
                "bearing_type"
            )
        }),
        ("Габариты", {
            "fields": (
                "height",
                "width",
                "length",
                "weight"
            )
        }),
        ("Дополнительно", {
            "fields": (
                "thermal_paste",
                "rgb_lighting"
            )
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("product")