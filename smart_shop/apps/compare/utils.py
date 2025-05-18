from collections import defaultdict, OrderedDict
from django.db.models import Q
from apps.products.models import Category
from apps.compare.models import Comparison


def get_comparison_data(products, category=None):
    # Фильтрация товаров по категории если указана
    if category:
        products = [p for p in products if p.category == category]

    # Собираем группы и параметры в порядке их появления
    ordered_groups = OrderedDict()  # Группы в порядке первого появления
    group_param_order = defaultdict(OrderedDict)  # Порядок параметров внутри групп

    for product in products:
        for group_name, group_specs in product.specs.items():
            # Добавляем группу, если ее еще нет
            if group_name not in ordered_groups:
                ordered_groups[group_name] = OrderedDict()

            # Добавляем параметры группы в порядке их появления
            for param_name in group_specs.keys():
                if param_name not in ordered_groups[group_name]:
                    ordered_groups[group_name][param_name] = []

        # Заполняем значения для каждого товара
    for product in products:
        product_specs = product.specs
        for group_name in ordered_groups:
            for param_name in ordered_groups[group_name]:
                value = product_specs.get(group_name, {}).get(param_name, "—")
                ordered_groups[group_name][param_name].append(str(value))

        # Формируем структуру для шаблона (исключаем "Основные параметры")
    grouped_specs = []
    for group_name, params in ordered_groups.items():
        if group_name == "Основные параметры":
            continue

        group_data = {
            'name': group_name,
            'params': []
        }
        for param_name, values in params.items():
            is_diff = len(set(values)) > 1
            group_data['params'].append({
                'name': param_name,
                'values': values,
                'is_diff': is_diff
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
