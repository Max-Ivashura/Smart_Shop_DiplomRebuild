from django.db import models
from apps.accounts.models import CustomUser
from apps.products.models import Product
from apps.configurator.utils.compatibility import CompatibilityChecker


class PCBuild(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='builds',
        verbose_name='Пользователь'
    )
    components = models.ManyToManyField(
        Product,
        through='BuildComponent',
        verbose_name='Компоненты',
        limit_choices_to={'is_active': True}
    )
    total_price = models.DecimalField(
        'Сумма сборки',
        max_digits=12,
        decimal_places=2,
        default=0
    )
    is_public = models.BooleanField('Публичная сборка', default=False)
    is_verified = models.BooleanField('Проверена', default=False)
    compatibility_errors = models.JSONField(
        'Ошибки совместимости',
        default=dict,
        blank=True
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    def check_compatibility(self):
        """Проверить совместимость компонентов и обновить поле ошибок."""
        checker = CompatibilityChecker(self.components.all())
        self.compatibility_errors = checker.validate()
        self.save()

    class Meta:
        verbose_name = 'Сборка ПК'
        verbose_name_plural = 'Сборки ПК'

    def __str__(self):
        return f'Сборка #{self.id} ({self.user})'


class BuildComponent(models.Model):
    build = models.ForeignKey(PCBuild, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Количество', default=1)

    class Meta:
        unique_together = ('build', 'product')
