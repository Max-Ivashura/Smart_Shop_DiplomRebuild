document.addEventListener('DOMContentLoaded', function () {
    // Динамическое обновление кнопок корзины
    const handleCartAction = async (button) => {
        const productId = button.dataset.productId;
        button.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"></div>';

        try {
            const response = await fetch(`{% url 'cart:add' 0 %}`.replace('0', productId), {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': '{{ csrf_token }}'
                }
            });

            if (response.ok) {
                button.innerHTML = '<i class="bi bi-check2"></i> В корзине';
                button.classList.remove('btn-primary');
                button.classList.add('btn-success');
                button.disabled = true;

                // Обновление счетчика в шапке
                const cartBadge = document.querySelector('.cart-count');
                if (cartBadge) {
                    cartBadge.textContent = parseInt(cartBadge.textContent) + 1;
                }
            }
        } catch (error) {
            button.innerHTML = '<i class="bi bi-x-circle"></i> Ошибка';
            button.classList.add('btn-danger');
            console.error('Ошибка:', error);
        }
    };

    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            if (!button.disabled) handleCartAction(button);
        });
    });

    // Сохранение параметров сортировки при пагинации
    document.getElementById('sortSelect').addEventListener('change', function () {
        const url = new URL(window.location.href);
        url.searchParams.set('sort', this.value);
        window.location.href = url.toString();
    });
});