from django.contrib import admin
from ..models.specs.psu import PSUSpecs


@admin.register(PSUSpecs)
class PSUSpecsAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "wattage",
        "form_factor",
        "modularity",
        "efficiency_cert",
        "fan_size",
        "rgb_lighting",
        "zero_rpm"
    )
    list_filter = (
        "form_factor",
        "modularity",
        "efficiency_cert",
        "pfc_type",
        "fan_control",
        "zero_rpm"
    )
    search_fields = (
        "product__name",
        "form_factor",
        "psu_standard",
        "protections"
    )
    raw_id_fields = ("product",)
    fieldsets = (
        ("Основные параметры", {
            "fields": (
                "product",
                "wattage",
                "form_factor",
                "color",
                "modularity",
                "cable_sleeving",
                "rgb_lighting"
            )
        }),
        ("Разъемы", {
            "fields": (
                "main_connector",
                "cpu_connectors",
                "pcie_connectors",
                "sata_connectors",
                "molex_connectors",
            )
        }),
        ("Электрические параметры", {
            "fields": (
                "psu_standard",
                "efficiency_cert",
                "pfc_type",
                "protections",
            )
        }),
        ("Охлаждение", {
            "fields": (
                "fan_size",
                "fan_control",
                "zero_rpm",
            )
        }),
        ("Габариты", {
            "fields": (
                "dimensions",
                "weight",
            )
        }),
        ("Длины кабелей", {
            "fields": (
                "main_cable_length",
                "cpu_cable_length",
                "pcie_cable_length",
            )
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("product")