from django.db import models
from apps.accounts.models import CustomUser
from apps.configurator.models import PCBuild

class BuildComment(models.Model):
    build = models.ForeignKey(
        PCBuild,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField("Текст комментария", max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField("Одобрен", default=False)

    class Meta:
        ordering = ['-created_at']

class BuildRating(models.Model):
    build = models.ForeignKey(
        PCBuild,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(
        "Оценка",
        choices=[(i, str(i)) for i in range(1, 6)]  # Оценка от 1 до 5
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('build', 'user')  # Одна оценка от пользователя