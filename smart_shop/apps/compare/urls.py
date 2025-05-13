from django.urls import path
from .views import ComparisonDetailView, toggle_comparison

app_name = 'compare'

urlpatterns = [
    path('', ComparisonDetailView.as_view(), name='comparison'),
    path('toggle/<int:product_id>/', toggle_comparison, name='toggle_comparison'),
    path('category/<int:category_id>/', ComparisonDetailView.as_view(), name='category_comparison'),
]