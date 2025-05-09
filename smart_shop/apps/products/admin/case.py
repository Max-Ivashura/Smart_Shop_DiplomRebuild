from django.contrib import admin
from ..models.specs.case import CaseSpecs


@admin.register(CaseSpecs)
class CaseSpecsAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "case_type",
        "dimensions",
        "motherboard_form_factors",
        "max_gpu_length",
        "max_cooler_height",
        "color",
        "window"
    )
    list_filter = (
        "case_type",
        "color",
        "window",
        "psu_location",
        "dust_filters"
    )
    search_fields = (
        "product__name",
        "case_type",
        "color",
        "motherboard_form_factors"
    )
    raw_id_fields = ("product",)
    fieldsets = (
        ("Основное", {
            "fields": (
                "product",
                "case_type",
                "dimensions",
                "motherboard_orientation",
            )
        }),
        ("Внешний вид", {
            "fields": (
                "color",
                "material",
                "window",
                "window_material",
            )
        }),
        ("Подсветка", {
            "fields": (
                "rgb_type",
                "rgb_control",
            )
        }),
        ("Совместимость", {
            "fields": (
                "motherboard_form_factors",
                "psu_location",
                "max_gpu_length",
                "max_cooler_height",
                "drive_bays",
            )
        }),
        ("Охлаждение", {
            "fields": (
                "included_fans",
                "fan_support",
                "radiator_support",
            )
        }),
        ("Интерфейсы и конструкция", {
            "fields": (
                "front_io",
                "cable_management",
                "dust_filters",
                "tool_free",
            )
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("product")