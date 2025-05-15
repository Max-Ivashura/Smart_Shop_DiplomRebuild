from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from apps.accounts.forms import CustomUserCreationForm, CustomUserForm, LoginForm
from apps.accounts.models import Wishlist, WishlistItem
from apps.products.models import Product


# --- Аутентификация ---
def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Добро пожаловать, {user.username}!")
                return redirect('accounts:profile')

        messages.error(request, "Неверные учетные данные")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def custom_logout(request):
    logout(request)
    messages.info(request, "Вы успешно вышли из системы")
    return redirect('home')


# --- Регистрация ---
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Исправьте ошибки в форме")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


# --- Профиль ---
@login_required
def profile(request):
    context = {
        'orders': request.user.orders.all(),
        'reviews': request.user.reviews.all(),
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserForm(
            request.POST,
            request.FILES,
            instance=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлен")
            return redirect('accounts:profile')
    else:
        form = CustomUserForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Пароль успешно изменен")
            return redirect('accounts:profile')
        else:
            # Добавляем сообщения об ошибках
            for field, errors in form.errors.items():
                for error in errors:
                    # Замените messages.error на messages.add_message
                    messages.add_message(request, messages.ERROR,
                                         f"Ошибка в поле '{field}': {error}")  # Тег "ERROR" → класс "alert-danger"
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})


# --- Вишлист ---
@login_required
def wishlist_view(request):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    items = WishlistItem.objects.filter(wishlist=wishlist).select_related('product')

    return render(request, 'accounts/wishlist.html', {
        'wishlist_items': items  # Убираем 'products'
    })


@require_POST
@login_required
def add_to_wishlist(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)

        # Проверяем, есть ли товар в избранном
        if wishlist.products.filter(id=product.id).exists():
            wishlist.products.remove(product)
            action = 'removed'
        else:
            wishlist.products.add(product)
            action = 'added'

        return JsonResponse({'status': 'success', 'action': action})

    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Товар не найден'}, status=404)


@login_required
def remove_from_wishlist(request, product_id):
    try:
        item = WishlistItem.objects.get(
            wishlist=request.user.wishlist,
            product_id=product_id  # Используем product_id вместо object_id
        )
        item.delete()
        messages.success(request, "Товар удален из избранного")
    except WishlistItem.DoesNotExist:
        messages.error(request, "Товар не найден")
    return redirect('accounts:wishlist')

# # --- Сборки ---
# @login_required
# def user_builds(request):
#     builds = Build.objects.filter(user=request.user).prefetch_related('components')
#     return render(request, 'accounts/user_builds.html', {'builds': builds})
