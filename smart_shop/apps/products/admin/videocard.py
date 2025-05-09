from django.contrib import admin
from ..models.specs.videocard import VideoCardSpecs


@admin.register(VideoCardSpecs)
class VideoCardSpecsAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "gpu_model",
        "vram_size",
        "vram_type",
        "base_clock",
        "tdp",
        "mining_support",
        "ray_tracing"
    )
    list_filter = (
        "color",
        "mining_support",
        "lhr",
        "vram_type",
        "pcie_version",
        "cooling_type",
        "liquid_cooling"
    )
    search_fields = (
        "product__name",
        "gpu_model",
        "architecture",
        "vram_type",
        "cooling_type"
    )
    raw_id_fields = ("product",)
    fieldsets = (
        ("Общие параметры", {
            "fields": (
                "product",
                "color",
                "mining_support",
                "lhr"
            )
        }),
        ("Графический процессор", {
            "fields": (
                "gpu_model",
                "architecture",
                "lithography",
                "alu_units",
                "ray_tracing"
            )
        }),
        ("Частоты", {
            "fields": (
                "base_clock",
                "boost_clock",
            )
        }),
        ("Видеопамять", {
            "fields": (
                "vram_size",
                "vram_type",
                "memory_bus",
                "memory_bandwidth",
                "memory_freq"
            )
        }),
        ("Вывод изображения", {
            "fields": (
                "video_outputs",
                "max_resolution",
                "monitors_support"
            )
        }),
        ("Подключение", {
            "fields": (
                "pcie_version",
                "power_connectors",
                "recommended_psu",
                "tdp"
            )
        }),
        ("Охлаждение", {
            "fields": (
                "cooling_type",
                "fans",
                "liquid_cooling"
            )
        }),
        ("Конструкция", {
            "fields": (
                "slots_occupied",
                "dimensions"
            )
        }),
        ("Дополнительно", {
            "fields": (
                "rgb_lighting",
                "bios_switch",
                "features"
            )
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("product")