# apps/core/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def delivery(request):
    return render(request, 'core/delivery.html')

def contacts(request):
    return render(request, 'core/contacts.html')