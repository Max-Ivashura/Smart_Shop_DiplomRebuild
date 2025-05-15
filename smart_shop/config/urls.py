from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core import views

urlpatterns = [
    # Core pages
    path('', views.home, name='home'),



    path('about/', views.about, name='about'),
    path('delivery/', views.delivery, name='delivery'),
    path('contacts/', views.contacts, name='contacts'),

    path('payment/', views.about, name='payment'),
    path('returns/', views.delivery, name='returns'),
    path('faq/', views.contacts, name='faq'),

    # Admin
    path('admin/', admin.site.urls),

    # Apps
    path('api/get-counters/', views.get_counters, name='get-counters'),
    path('catalog/', include(('apps.products.urls', 'products'), namespace='products')),
    path('accounts/', include(('apps.accounts.urls', 'accounts'), namespace='accounts')),
    path('cart/', include(('apps.cart.urls', 'cart'), namespace='cart')),
    path('orders/', include(('apps.orders.urls', 'orders'), namespace='orders')),
    path('compare/', include(('apps.compare.urls', 'compare'), namespace='compare')),
    path('configurator/', include(('apps.configurator.urls', 'configurator'), namespace='configurator')),
]

# Static/media for development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
