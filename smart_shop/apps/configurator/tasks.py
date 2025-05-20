from celery import shared_task
from django.utils import timezone
from apps.configurator.models import PCBuild


@shared_task
def cleanup_empty_builds():
    # Удаляем сборки без компонентов, созданные более часа назад
    PCBuild.objects.filter(
        buildcomponent__isnull=True,
        created_at__lt=timezone.now() - timezone.timedelta(hours=1)
    ).delete()
