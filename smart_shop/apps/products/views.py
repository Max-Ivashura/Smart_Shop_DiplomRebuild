from django.db.models import Q, Case, When, Value, IntegerField
from django.views.generic import ListView, DetailView

from apps.compare.models import Comparison
from .models import Product, Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Product, Review
from apps.compare.utils import get_user_comparison


# apps/products/views.py
class ProductListView(ListView):
    template_name = "products/catalog.html"
    context_object_name = "products"
    paginate_by = 25
    ordering = "created_at"

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related("category")
        self.category = None

        # Фильтрация по категории
        if category_slug := self.kwargs.get("category_slug"):
            self.category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(
                Q(category=self.category) | Q(category__in=self.category.get_descendants())
            )

        # Фильтрация по цене
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        if min_price and min_price.isdigit():
            queryset = queryset.filter(price__gte=int(min_price))
        if max_price and max_price.isdigit():
            queryset = queryset.filter(price__lte=int(max_price))

        # Сортировка
        sort = self.request.GET.get("sort", "newest")
        if sort == "price_asc":
            queryset = queryset.order_by("price")
        elif sort == "price_desc":
            queryset = queryset.order_by("-price")
        elif sort == "newest":
            queryset = queryset.order_by("-created_at")
        elif sort == "popular":
            queryset = queryset.annotate(
                popularity=Case(
                    When(stock=0, then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField()
                )
            ).order_by("-popularity", "-created_at")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_category'] = self.category or None
        context['categories'] = Category.objects.all()
        context['sort_param'] = self.request.GET.get("sort", "newest")

        # Получаем все ID товаров в сравнениях пользователя
        comparison_product_ids = set()

        # Для авторизованных пользователей
        if self.request.user.is_authenticated:
            comparisons = Comparison.objects.filter(user=self.request.user)
        # Для анонимных пользователей
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.create()
                session_key = self.request.session.session_key
            comparisons = Comparison.objects.filter(session_key=session_key)

        # Собираем все ID товаров из всех сравнений
        for comparison in comparisons:
            comparison_product_ids.update(
                comparison.items.values_list('product_id', flat=True)
            )

        context['comparison_product_ids'] = comparison_product_ids
        return context


class ProductDetailView(DetailView):
    template_name = "products/detail.html"
    context_object_name = "product"
    slug_url_kwarg = "product_slug"  # Явное указание slug-параметра

    def get_object(self, queryset=None):
        """Получаем товар с проверкой активности и категории."""
        return get_object_or_404(
            Product.objects.select_related("category"),
            category__slug=self.kwargs["category_slug"],
            slug=self.kwargs["product_slug"],
            is_active=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        # Хлебные крошки: Категория → Подкатегория → Товар
        context["breadcrumbs"] = [
            *product.category.get_ancestors(include_self=True),
            product
        ]

        # Характеристики товара
        context["specs"] = product.specs  # Используем метод модели

        context['comparison'] = get_user_comparison(self.request)

        context['reviews_count'] = self.object.reviews.count()
        context['average_rating'] = self.object.average_rating

        comparison_product_ids = set()
        if self.request.user.is_authenticated:
            comparisons = Comparison.objects.filter(user=self.request.user)
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.create()
                session_key = self.request.session.session_key
            comparisons = Comparison.objects.filter(session_key=session_key)

        for comparison in comparisons:
            comparison_product_ids.update(
                comparison.items.values_list('product_id', flat=True)
            )

        context['comparison_product_ids'] = comparison_product_ids

        # Связанные товары (4 штуки из той же категории)
        context["related_products"] = Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(pk=product.pk).select_related("category")[:4]

        # Проверка наличия на складе для кнопки "В корзину"
        context["in_stock"] = product.stock > 0

        return context


class ProductSearchView(ListView):
    """
    Поиск товаров по названию и характеристикам
    """
    template_name = "products/search.html"
    paginate_by = 25

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        if not query:  # Если запрос пустой, возвращаем все товары (или пустой список)
            return Product.objects.none()
        return Product.objects.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query),  # Поиск по артикулу
            is_active=True
        ).select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        text = request.POST.get("text")
        rating = request.POST.get("rating", 5)

        # Проверка, не оставлял ли пользователь отзыв ранее
        if Review.objects.filter(user=request.user, product=product).exists():
            messages.error(request, "Вы уже оставляли отзыв на этот товар")
            return redirect(product.get_absolute_url())

        Review.objects.create(
            user=request.user,
            product=product,
            text=text,
            rating=rating
        )
        messages.success(request, "Ваш отзыв успешно добавлен!")
    return redirect(product.get_absolute_url())


def categories(request):
    return {
        'categories': Category.objects.filter(parent__isnull=True)
    }
