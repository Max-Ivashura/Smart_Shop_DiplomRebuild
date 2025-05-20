from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import BuildComponent


@receiver(post_save, sender=BuildComponent)
def update_build_price_on_save(sender, instance, **kwargs):
    instance.build.total_price = sum(
        component.product.price * component.quantity
        for component in instance.build.buildcomponent_set.all()
    )
    instance.build.save()


@receiver(post_delete, sender=BuildComponent)
def update_build_price_on_delete(sender, instance, **kwargs):
    instance.build.total_price = sum(
        component.product.price * component.quantity
        for component in instance.build.buildcomponent_set.all()
    )
    instance.build.save()
