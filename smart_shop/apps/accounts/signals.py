from django.contrib.auth import user_logged_in
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.accounts.models import CustomUser, Wishlist
from apps.compare.models import Comparison, ComparisonItem


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


@receiver(user_logged_in)
def merge_comparisons_on_login(sender, user, request, **kwargs):
    """
    Переносит товары из анонимного сравнения (сессии) в сравнение пользователя при входе.
    """
    session_key = request.session.session_key

    if session_key:
        # Получаем все сравнения из сессии
        session_comparisons = Comparison.objects.filter(session_key=session_key)

        for session_comp in session_comparisons:
            # Создаем или получаем сравнение пользователя для той же категории
            user_comp, created = Comparison.objects.get_or_create(
                user=user,
                category=session_comp.category
            )

            # Переносим товары
            for item in session_comp.items.all():
                ComparisonItem.objects.get_or_create(
                    comparison=user_comp,
                    product=item.product
                )

            # Удаляем сессионное сравнение
            session_comp.delete()
