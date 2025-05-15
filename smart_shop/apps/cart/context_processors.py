# apps/cart/context_processors.py
from .models import CartItem

def cart_count(request):
    if request.user.is_authenticated:
        count = CartItem.objects.filter(cart__user=request.user).count()
    else:
        session_key = request.session.session_key
        count = CartItem.objects.filter(cart__session_key=session_key).count() if session_key else 0
    return {'cart_count': count}