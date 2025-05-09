document.addEventListener('DOMContentLoaded', function () {
    // Динамическое обновление количества
    document.querySelectorAll('.quantity-input').forEach(input => {
        input.addEventListener('change', function () {
            this.closest('form').submit();
        });
    });

    // Кнопки +/-
    document.querySelectorAll('.plus-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const input = this.parentElement.querySelector('.quantity-input');
            input.value = parseInt(input.value) + 1;
            input.dispatchEvent(new Event('change'));
        });
    });

    document.querySelectorAll('.minus-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const input = this.parentElement.querySelector('.quantity-input');
            if (input.value > 1) {
                input.value = parseInt(input.value) - 1;
                input.dispatchEvent(new Event('change'));
            }
        });
    });

    // Обновление счетчика в шапке
    function updateCartBadge(count) {
        document.querySelectorAll('.cart-count').forEach(badge => {
            badge.textContent = count;
        });
    }

    // Пример использования (реализовать через AJAX в реальном проекте):
    // updateCartBadge(5);
});