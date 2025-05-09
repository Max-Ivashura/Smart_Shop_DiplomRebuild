from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from apps.products.models import Category
from apps.products.models import Product
from apps.products.models import ProductImage


# Если используется MPTT для древовидных категорий:
@admin.register(Category)
class CategoryMPTTAdmin(MPTTModelAdmin):
    list_display = ("name", "slug", "product_count")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    mptt_level_indent = 20  # Отступ для дерева

    def product_count(self, obj):
        return obj.products.count()

    product_count.short_description = "Товаров в категории"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "image", "is_main")
    list_editable = ("is_main",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "sku", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "sku", "category__name")
    prepopulated_fields = {"slug": ("name", "sku")}
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Основное", {
            "fields": ("category", "name", "slug", "sku", "is_active")
        }),
        ("Цена и наличие", {
            "fields": ("price", "stock")
        }),
        ("Дополнительно", {
            "fields": ("warranty", "country")
        }),
        ("Даты", {
            "fields": ("created_at", "updated_at")
        }),
    )
