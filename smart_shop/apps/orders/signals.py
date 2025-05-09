from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Order

@receiver(post_save, sender=Order)
def send_order_status_email(sender, instance, **kwargs):
    if instance.tracker.has_changed("status"):
        subject = f"Статус заказа #{instance.id} изменен"
        message = (
            f"Ваш заказ #{instance.id} получил новый статус: "
            f"{instance.get_status_display()}.\n"
            f"Подробности: https://ваш-сайт/orders/{instance.id}/"
        )
        send_mail(
            subject,
            message,
            "noreply@example.com",
            [instance.user.email],
            fail_silently=False,
        )