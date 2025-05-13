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

def payment(request):
    return render(request, 'core/payment.html')

def returns(request):
    return render(request, 'core/returns.html')

def faq(request):
    return render(request, 'core/faq.html')