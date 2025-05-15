from collections import defaultdict

from apps.compare.models import Comparison


def get_comparison_data(products):
    specs = []
    common_specs = defaultdict(set)

    # Собираем все характеристики
    for product in products:
        for group, params in product.specs.items():
            for param, value in params.items():
                common_specs[f"{group}__{param}"].add(str(value))

    # Формируем структуру для таблицы
    grouped_specs = defaultdict(dict)
    for key in common_specs:
        group, param = key.split('__')
        grouped_specs[group][param] = list(common_specs[key])

    return {
        'products': products,
        'specs': dict(grouped_specs),
        'categories': {p.category.name for p in products}
    }


def get_user_comparison(request):
    if request.user.is_authenticated:
        return Comparison.objects.filter(user=request.user).first()
    else:
        if not request.session.session_key:
            request.session.create()
        return Comparison.objects.filter(session_key=request.session.session_key).first()
