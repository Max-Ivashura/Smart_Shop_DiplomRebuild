from django.urls import path
from .views import (
    CartDetailView,
    add_to_cart,
    remove_from_cart,
    update_quantity
)

app_name = "cart"

urlpatterns = [
    path("", CartDetailView.as_view(), name="detail"),
    path("add/<int:product_id>/", add_to_cart, name="add"),
    path("remove/<int:cart_item_id>/", remove_from_cart, name="remove"),
    path("update/<int:cart_item_id>/", update_quantity, name="update"),
]