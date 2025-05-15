from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from .models import Comparison, ComparisonItem
from apps.products.models import Product
from .utils import get_comparison_data


class ComparisonDetailView(DetailView):
    model = Comparison
    template_name = 'compare/comparison.html'
    context_object_name = 'comparison'

    def get_object(self):
        if self.request.user.is_authenticated:
            comparison, _ = Comparison.objects.get_or_create(
                user=self.request.user,
                category_id=self.kwargs['category_id']
            )
        else:
            comparison, _ = Comparison.objects.get_or_create(
                session_id=self.request.session.session_key,
                category_id=self.kwargs['category_id']
            )
        return comparison

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = [item.product for item in self.object.items.all()]
        context.update(get_comparison_data(products))
        return context


@require_POST
def toggle_comparison(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)

        if request.user.is_authenticated:
            comparison, created = Comparison.objects.get_or_create(
                user=request.user,
                category=product.category
            )
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key

            comparison, created = Comparison.objects.get_or_create(
                session_id=session_key,
                category=product.category
            )

        item, created = ComparisonItem.objects.get_or_create(
            comparison=comparison,
            product=product
        )

        if not created:
            item.delete()
            action = 'removed'
        else:
            action = 'added'

        return JsonResponse({
            'status': 'success',
            'action': action,
            'count': comparison.items.count(),
            'product_id': product_id
        })
    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Товар не найден'}, status=404)
