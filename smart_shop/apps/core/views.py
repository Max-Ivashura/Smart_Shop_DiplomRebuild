# apps/core/views.py
from django.http import JsonResponse
from django.shortcuts import render

from apps.cart.context_processors import cart_count
from apps.compare.context_processors import comparison
from apps.accounts.context_processors import wishlist


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


def get_counters(request):
    return JsonResponse({
        'cart_count': cart_count(request)['cart_count'],
        'comparison_count': comparison(request)['comparison_count'],
        'wishlist_count': wishlist(request)['wishlist_count'],
    })
