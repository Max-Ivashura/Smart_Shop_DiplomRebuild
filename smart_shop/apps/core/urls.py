# apps/core/urls.py
from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("api/get-counters/", views.get_counters, name="get-counters"),  # Эндпоинт для счетчиков
    path("", views.home, name="home"),  # Главная страница
]