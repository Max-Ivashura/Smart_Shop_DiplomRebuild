from django.contrib import admin
from ..models.specs.watercooling import WaterCoolingSpecs


@admin.register(WaterCoolingSpecs)
class WaterCoolingSpecsAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "cooling_type",
        "serviceable",
        "radiator_size",
        "tdp",
        "fan_quantity",
        "pump_speed",
        "thermal_paste"
    )
    list_filter = (
        "cooling_type",
        "serviceable",
        "fan_size",
        "tube_material",
        "transparent_tubes"
    )
    search_fields = (
        "product__name",
        "socket_support",
        "radiator_size",
        "fan_size",
        "tube_material"
    )
    raw_id_fields = ("product",)
    fieldsets = (
        ("Основные параметры", {
            "fields": (
                "product",
                "cooling_type",
                "serviceable"
            )
        }),
        ("Внешний вид", {
            "fields": (
                "color",
                "rgb_type",
                "rgb_components"
            )
        }),
        ("Водоблок", {
            "fields": (
                "socket_support",
                "block_material",
                "block_dimensions"
            )
        }),
        ("Радиатор", {
            "fields": (
                "radiator_size",
                "tdp",
                "radiator_material",
                "radiator_dimensions"
            )
        }),
        ("Вентиляторы", {
            "fields": (
                "fan_quantity",
                "fan_size",
                "fan_rpm",
                "fan_noise",
                "fan_airflow"
            )
        }),
        ("Помпа", {
            "fields": (
                "pump_noise",
                "pump_speed"
            )
        }),
        ("Трубки", {
            "fields": (
                "tube_material",
                "transparent_tubes"
            )
        }),
        ("Дополнительно", {
            "fields": (
                "thermal_paste",
                "included_accessories"
            )
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("product")