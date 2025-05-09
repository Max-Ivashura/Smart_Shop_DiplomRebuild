from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.accounts.models import CustomUser, Wishlist


@receiver(post_save, sender=CustomUser)
def create_user_related_objects(sender, instance, created, **kwargs):
    """Создает Wishlist при регистрации пользователя"""
    if created:
        Wishlist.objects.create(user=instance)


@receiver(post_delete, sender=CustomUser)
def delete_related_objects(sender, instance, **kwargs):
    """Удаляет связанные объекты при удалении пользователя"""
    # Удаляем Wishlist (каскадно удалятся все WishlistItem)
    if hasattr(instance, 'wishlist'):
        instance.wishlist.delete()

    # Удаление корзины (если есть связанное приложение cart)
    # if hasattr(instance, 'cart'):
    #     instance.cart.delete()