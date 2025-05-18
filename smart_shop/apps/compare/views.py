from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView

from apps.products.models import Category
from .models import Comparison, ComparisonItem
from apps.products.models import Product
from .utils import get_comparison_data


class ComparisonDetailView(DetailView):
    model = Comparison
    template_name = 'compare/comparison.html'
    context_object_name = 'comparison'

    def get_object(self):
        # Исправлено session_id → session_key
        if self.request.user.is_authenticated:
            comparison, _ = Comparison.objects.get_or_create(user=self.request.user)
            return comparison

        session_key = self.request.session.session_key
        if not session_key:
            self.request.session.create()
            session_key = self.request.session.session_key

        # Исправлено здесь: session_id → session_key
        comparison, _ = Comparison.objects.get_or_create(session_key=session_key)
        return comparison

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comparison = self.object

        categories_data = {}
        for category in comparison.categories.all():
            products = [item.product for item in comparison.items.filter(category=category)]
            if products:
                comparison_data = get_comparison_data(products, category)
                categories_data[category] = {
                    'products': products,
                    'specs': comparison_data['specs'],
                    'common_params': comparison_data['common_params']
                }

        active_category_id = self.request.GET.get('category')
        active_category = None

        # Проверка на число и существование категории
        if active_category_id and active_category_id.isdigit():
            try:
                active_category = Category.objects.get(id=int(active_category_id))
            except (Category.DoesNotExist, ValueError):
                pass  # Категория не найдена или ID некорректен

        context.update({
            'categories_data': categories_data,
            'active_category': active_category,
            'all_categories': comparison.categories.all()
        })
        return context


@require_POST
def toggle_comparison(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        category = product.category

        if request.user.is_authenticated:
            comparison, _ = Comparison.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            comparison, _ = Comparison.objects.get_or_create(session_key=session_key)

        # Добавляем категорию в список категорий сравнения
        if not comparison.categories.filter(id=category.id).exists():
            comparison.categories.add(category)

        item, created = ComparisonItem.objects.get_or_create(
            comparison=comparison,
            product=product,
            category=category
        )

        if not created:
            item.delete()
            action = 'removed'
            # Удаляем категорию если нет товаров
            if not comparison.items.filter(category=category).exists():
                comparison.categories.remove(category)
        else:
            action = 'added'

        return JsonResponse({
            'status': 'success',
            'action': action,
            'category_id': category.id,
            'category_name': category.name,
            'product_ids': list(comparison.items.values_list('product_id', flat=True))
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
