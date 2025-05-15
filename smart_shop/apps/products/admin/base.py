from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from apps.products.models import Category
from apps.products.models import Product
from apps.products.models import ProductImage

# Если используется MPTT для древовидных категорий:
from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from apps.products.models import Category


@admin.register(Category)
class CategoryMPTTAdmin(DraggableMPTTAdmin):
    list_display = (
        'tree_actions',  # Добавляет иконки для управления деревом
        'indented_title',  # Отображает название с отступами
        'slug',
        'product_count'
    )
    list_display_links = ('indented_title',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}

    # Настройки для drag-and-drop
    mptt_level_indent = 20
    expand_tree_by_default = True  # Автоматически раскрывать дерево
    change_list_template = 'admin/mptt_change_list.html'  # Шаблон с поддержкой DnD

    def product_count(self, obj):
        return obj.get_product_count()

    product_count.short_description = "Товаров (включая подкатегории)"

    def indented_title(self, instance):
        return super().indented_title(instance)

    indented_title.short_description = "Категория"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "image", "is_main")
    list_editable = ("is_main",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "description", "price", "sku", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "sku", "category__name")
    prepopulated_fields = {"slug": ("name", "sku")}
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Основное", {
            "fields": ("category", "name", "description", "slug", "sku", "is_active")
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
