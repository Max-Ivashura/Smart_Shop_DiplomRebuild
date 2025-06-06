# Generated by Django 5.2 on 2025-05-17 03:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comparison',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(blank=True, max_length=40, null=True, verbose_name='Ключ сессии')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('categories', models.ManyToManyField(related_name='comparisons', to='products.category', verbose_name='Категории сравнения')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Сравнение',
                'verbose_name_plural': 'Сравнения',
            },
        ),
        migrations.CreateModel(
            name='ComparisonItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.category', verbose_name='Категория товара')),
                ('comparison', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='compare.comparison', verbose_name='Сравнение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Элемент сравнения',
                'verbose_name_plural': 'Элементы сравнения',
                'ordering': ['-added_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='comparison',
            constraint=models.UniqueConstraint(condition=models.Q(('user__isnull', False)), fields=('user',), name='unique_user_comparison'),
        ),
        migrations.AddConstraint(
            model_name='comparison',
            constraint=models.UniqueConstraint(condition=models.Q(('user__isnull', True)), fields=('session_key',), name='unique_session_comparison'),
        ),
        migrations.AddConstraint(
            model_name='comparisonitem',
            constraint=models.UniqueConstraint(fields=('comparison', 'product'), name='unique_comparison_product'),
        ),
    ]
