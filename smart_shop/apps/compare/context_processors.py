# apps/compare/context_processors.py
from .models import Comparison


def comparison(request):
    comparison_count = 0

    if request.user.is_authenticated:
        # Получаем все сравнения пользователя и суммируем товары
        user_comparisons = Comparison.objects.filter(user=request.user)
        for comp in user_comparisons:
            comparison_count += comp.items.count()
    else:
        # Для анонимных пользователей используем session_key
        session_key = request.session.session_key
        if session_key:
            session_comparisons = Comparison.objects.filter(session_key=session_key)
            for comp in session_comparisons:
                comparison_count += comp.items.count()

    return {'comparison_count': comparison_count}