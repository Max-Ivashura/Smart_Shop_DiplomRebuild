from django.contrib import admin
from ..models.specs.processor import ProcessorSpecs


@admin.register(ProcessorSpecs)
class ProcessorSpecsAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "socket",
        "cores",
        "performance_cores",
        "efficiency_cores",
        "threads",
        "base_freq",
        "tdp"
    )
    list_filter = (
        "socket",
        "cores",
        "memory_type",
        "multiplier_unlocked"
    )
    search_fields = (
        "product__name",
        "socket",
        "lithography",
        "core_name"
    )
    raw_id_fields = ("product",)
    fieldsets = (
        ("Основное", {
            "fields": (
                "product",
                "includes_cooler",
                "thermal_interface"
            )
        }),
        ("Ядро и архитектура", {
            "fields": (
                "socket",
                "cores",
                "performance_cores",
                "efficiency_cores",
                "threads",
                "l2_cache",
                "l3_cache",
                "lithography",
                "core_name"
            )
        }),
        ("Частота и разгон", {
            "fields": (
                "base_freq",
                "max_turbo_freq",
                "multiplier_unlocked",
                "efficiency_base_freq",
                "efficiency_turbo_freq"
            )
        }),
        ("Память", {
            "fields": (
                "memory_type",
                "max_memory",
                "memory_channels",
                "memory_frequency",
                "ecc_support"
            )
        }),
        ("Расширенные параметры", {
            "fields": (
                "pcie_version",
                "tdp",
                "max_temp",
                "integrated_gpu"
            )
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("product")
