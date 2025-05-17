from collections import defaultdict
from django.db.models import Q
from apps.products.models import Category
from apps.compare.models import Comparison


def get_comparison_data(products, category=None):
    """
    Возвращает структурированные данные для сравнения с группировкой по категориям
    """
    # Фильтрация товаров по категории если указана
    if category:
        products = [p for p in products if p.category == category]

    # Собираем все характеристики для выбранной категории
    specs_tree = defaultdict(lambda: defaultdict(set))

    for product in products:
        for group_name, group_specs in product.specs.items():
            for param_name, param_value in group_specs.items():
                key = f"{group_name}||{param_name}"
                specs_tree[group_name][param_name].add(str(param_value))

    # Преобразуем в структуру для шаблона
    grouped_specs = []
    for group, params in specs_tree.items():
        group_data = {
            'name': group,
            'params': []
        }
        for param, values in params.items():
            group_data['params'].append({
                'name': param,
                'values': list(values),
                'is_diff': len(values) > 1
            })
        grouped_specs.append(group_data)

    return {
        'category': category,
        'products': products,
        'specs': grouped_specs,
        'common_params': [p for p in grouped_specs if any(item['is_diff'] for item in p['params'])]
    }


def get_user_comparison(request):
    """
    Возвращает объект сравнения с группировкой по категориям
    """
    comparison = None
    if request.user.is_authenticated:
        comparison = Comparison.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if session_key:
            comparison = Comparison.objects.filter(session_key=session_key).first()

    if comparison:
        # Группируем товары по категориям
        categories_data = {}
        for category in comparison.categories.all():
            items = comparison.items.filter(category=category)
            categories_data[category] = {
                'products': [item.product for item in items],
                'count': items.count()
            }
        comparison.grouped_data = categories_data

    return comparison
