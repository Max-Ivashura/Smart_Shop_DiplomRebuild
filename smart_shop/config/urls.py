# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core import views  # Импорт views из приложения core

urlpatterns = [
                  # Админ-панель
                  path('admin/', admin.site.urls),

                  # Главная страница
                  path('', views.home, name='home'),

                  # Страницы магазина
                  path('about/', views.about, name='about'),
                  path('delivery/', views.delivery, name='delivery'),
                  path('contacts/', views.contacts, name='contacts'),
                  # path('builds/', views.builds, name='builds'),
                  path("configurator/", include("apps.configurator.urls")),

                  # Приложения
                  path('catalog/', include(('apps.products.urls', 'products'), namespace='products')),
                  path('accounts/', include(('apps.accounts.urls', 'accounts'), namespace='accounts')),
                  # path('cart/', include('apps.cart.urls')),

                  # ... другие приложения при необходимости
                  path("cart/", include("apps.cart.urls")),
                  path("orders/", include("apps.orders.urls")),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Для статических файлов

# Только для разработки: обслуживание медиа-файлов
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
