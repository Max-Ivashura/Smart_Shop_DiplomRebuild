from apps.accounts.models import Wishlist


def wishlist(request):
    wishlist_count = 0
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
        wishlist_count = wishlist.products.count() if wishlist else 0
    return {'wishlist_count': wishlist_count}