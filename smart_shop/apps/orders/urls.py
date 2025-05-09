from django.urls import path
from .views import OrderListView, OrderDetailView, create_order, cancel_order

app_name = "orders"

urlpatterns = [
    path("", OrderListView.as_view(), name="list"),
    path("create/", create_order, name="create"),
    path("<int:pk>/", OrderDetailView.as_view(), name="detail"),
    path("<int:pk>/cancel/", cancel_order, name="cancel"),
]