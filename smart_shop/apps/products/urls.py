from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="catalog"),
    path("search/", views.ProductSearchView.as_view(), name="search"),
    path("<slug:category_slug>/", views.ProductListView.as_view(), name="category"),
    path("<slug:category_slug>/<slug:product_slug>/", views.ProductDetailView.as_view(), name="detail"),
    path("catalog/<int:product_id>/add-review/", views.add_review, name="add_review"),
]
