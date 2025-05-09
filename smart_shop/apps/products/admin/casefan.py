from django.contrib import admin
from ..models.specs.casefan import CaseFanSpecs


@admin.register(CaseFanSpecs)
class CaseFanSpecsAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "fan_quantity",
        "size",
        "max_rpm",
        "airflow",
        "frame_color",
        "pwm_control",
        "anti_vibration"
    )
    list_filter = (
        "fan_quantity",
        "frame_color",
        "bearing_type",
        "anti_vibration",
        "pwm_control",
        "controller_included",
        "remote_control"
    )
    search_fields = (
        "product__name",
        "size",
        "bearing_type",
        "connector_type",
        "rgb_type"
    )
    raw_id_fields = ("product",)
    fieldsets = (
        ("Основное", {
            "fields": (
                "product",
                "fan_quantity",
            )
        }),
        ("Внешний вид", {
            "fields": (
                "frame_color",
                "blade_color",
                "rgb_type",
                "rgb_source",
            )
        }),
        ("Конструкция", {
            "fields": (
                "size",
                "thickness",
                "bearing_type",
                "anti_vibration",
            )
        }),
        ("Технические характеристики", {
            "fields": (
                "max_rpm",
                "min_rpm",
                "airflow",
                "static_pressure",
                "max_noise",
                "min_noise",
            )
        }),
        ("Питание", {
            "fields": (
                "connector_type",
                "pwm_control",
                "voltage",
                "current",
            )
        }),
        ("Подсветка", {
            "fields": (
                "rgb_connector",
                "controller_included",
                "remote_control",
            )
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("product")