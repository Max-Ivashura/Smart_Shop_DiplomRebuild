import time
from datetime import date

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.files.storage import default_storage

from apps.products.models import Product


class CustomUser(AbstractUser):
    # Переопределяем email как обязательное уникальное поле
    email = models.EmailField(
        "Email",
        unique=True,
        error_messages={
            'unique': "Пользователь с таким email уже существует.",
        }
    )

    # Переносим поля из UserProfile
    phone = models.CharField(
        "Телефон",
        max_length=20,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+7\d{10}$',
                message="Номер должен быть в формате +7XXXXXXXXXX"
            )
        ]
    )

    address = models.CharField("Адрес", max_length=255, blank=True)
    birth_date = models.DateField(
        "Дата рождения",
        null=True,
        blank=True,
        # format='%d.%m.%Y'  # Необязательно, зависит от настроек проекта
    )

    def user_directory_path(instance, filename):
        ext = filename.split('.')[-1]
        return f'avatars/{instance.id}_{int(time.time())}.{ext}'

    avatar = models.ImageField(
        "Аватар",
        upload_to=user_directory_path,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

    def save(self, *args, **kwargs):
        # Удаление старой аватарки при обновлении
        if self.pk:
            old_instance = CustomUser.objects.get(pk=self.pk)
            if old_instance.avatar and old_instance.avatar != self.avatar:
                if default_storage.exists(old_instance.avatar.name):
                    default_storage.delete(old_instance.avatar.name)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Удаление аватарки при удалении пользователя
        if self.avatar:
            if default_storage.exists(self.avatar.name):
                default_storage.delete(self.avatar.name)
        super().delete(*args, **kwargs)

    @property
    def is_adult(self):
        """Проверка совершеннолетия"""
        if self.birth_date:
            today = date.today()
            age = today.year - self.birth_date.year - (
                    (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
            return age >= 18
        return False

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.username})

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Wishlist(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='wishlist'
    )
    products = models.ManyToManyField(
        Product,
        through='WishlistItem',
        related_name='wishlists'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wishlist пользователя {self.user.username}"

    def add_product(self, product):
        self.products.add(product)

    def remove_product(self, product):
        self.products.remove(product)

    def has_product(self, product):
        return self.products.filter(id=product.id).exists()


class WishlistItem(models.Model):
    wishlist = models.ForeignKey("Wishlist", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Корректное поле
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('wishlist', 'product')  # Уникальность связки
