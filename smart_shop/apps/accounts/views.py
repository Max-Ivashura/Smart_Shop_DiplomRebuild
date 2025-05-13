from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect, render

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
    items = WishlistItem.objects.filter(wishlist=wishlist).prefetch_related('content_type')

    # Загружаем реальные объекты продуктов
    products = []
    for item in items:
        product = item.product
        if hasattr(product, 'main_image'):
            product.main_image = product.images.first()  # Пример для модели Product
        products.append(product)

    return render(request, 'accounts/wishlist.html', {
        'wishlist_items': items,
        'products': products
    })


@login_required
def add_to_wishlist(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        content_type = ContentType.objects.get_for_model(product)
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        WishlistItem.objects.get_or_create(
            wishlist=wishlist,
            content_type=content_type,
            object_id=product.id
        )
        messages.success(request, "Товар добавлен в список желаний!")
        return redirect('products:detail', category_slug=product.category.slug, product_slug=product.slug)
    except Product.DoesNotExist:
        messages.error(request, "Товар не найден.")
        return redirect('home')


@login_required
def remove_from_wishlist(request, product_id):
    try:
        item = WishlistItem.objects.get(
            wishlist=request.user.wishlist,
            object_id=product_id
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
