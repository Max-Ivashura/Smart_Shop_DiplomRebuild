from django.contrib import admin
from ..models.specs.ram import RAMSpecs


@admin.register(RAMSpecs)
class RAMSpecsAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "memory_type",
        "total_capacity",
        "module_capacity",
        "frequency",
        "cas_latency",
        "heatsink",
        "ecc"
    )
    list_filter = (
        "memory_type",
        "module_type",
        "heatsink",
        "ecc",
        "registered",
        "rank"
    )
    search_fields = (
        "product__name",
        "memory_type",
        "module_type",
        "expo_profiles",
        "xmp_profiles"
    )
    raw_id_fields = ("product",)
    fieldsets = (
        ("Основные параметры", {
            "fields": (
                "product",
                "memory_type",
                "module_type",
                "kit_quantity",
                "total_capacity",
                "module_capacity"
            )
        }),
        ("Технические характеристики", {
            "fields": (
                "frequency",
                "expo_profiles",
                "xmp_profiles",
                "cas_latency",
                "trcd",
                "trp"
            )
        }),
        ("Конструкция", {
            "fields": (
                "heatsink",
                "heatsink_color",
                "height",
                "low_profile"
            )
        }),
        ("Дополнительные параметры", {
            "fields": (
                "voltage",
                "ecc",
                "registered",
                "rank",
                "on_die_ecc"
            )
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("product")