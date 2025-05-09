from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.accounts.models import CustomUser, Wishlist, WishlistItem


# --- Кастомная админка для пользователя ---
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 'birth_date', 'avatar')
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    list_display = (
        'username',
        'email',
        'phone',
        'is_staff',
        'is_adult_display'
    )

    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'phone', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined', 'is_adult_display')
    ordering = ('-date_joined',)

    def is_adult_display(self, obj):
        return "Да" if obj.is_adult else "Нет"

    is_adult_display.short_description = "Совершеннолетний"


# --- Админка для Wishlist ---
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'total_products')
    list_select_related = ('user',)
    search_fields = ('user__username', 'user__email')

    def total_products(self, obj):
        return obj.wishlistitem_set.count()

    total_products.short_description = "Товаров"


# --- Админка для WishlistItem ---
@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'added_at')
    list_select_related = ('content_type', 'wishlist__user')

    def user(self, obj):
        return obj.wishlist.user