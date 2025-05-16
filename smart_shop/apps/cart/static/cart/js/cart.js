document.addEventListener('DOMContentLoaded', function () {
    // Конфигурация
    const config = {
        csrfToken: document.querySelector('meta[name="csrf-token"]').content,
        animationDuration: 300,
        selectors: {
            item: '.ts-cart-item',
            quantityInput: '.ts-cart-quantity-input',
            plusBtn: '.plus-btn',
            minusBtn: '.minus-btn',
            priceTotal: '.item-total',
            cartTotal: '.ts-cart-total-price',
            cartCount: '.cart-count',
            removeBtn: '.ts-cart-remove'
        }
    };

    // Основная функция обновления
    async function updateCart(itemId, newQuantity) {
        try {
            const itemElement = document.querySelector(`${config.selectors.item}[data-item-id="${itemId}"]`);
            if (!itemElement) throw new Error('Элемент корзины не найден');

            const response = await fetch(`/cart/update/${itemId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': config.csrfToken
                },
                body: `quantity=${newQuantity}`
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

            const data = await response.json();

            if (data.status === 'success') {
                // Обновление позиции
                itemElement.querySelector(config.selectors.quantityInput).value = newQuantity;
                const formattedPrice = parseFloat(data.item_total).toFixed(0);
                itemElement.querySelector(config.selectors.priceTotal).textContent = formattedPrice;

                // Глобальные значения
                document.querySelector(config.selectors.cartTotal).textContent = parseFloat(data.cart_total).toFixed(0);
                document.querySelectorAll(config.selectors.cartCount).forEach(el => {
                    el.textContent = data.total_items;
                });

                animateUpdate(itemId);
            } else {
                throw new Error(data.message || 'Неизвестная ошибка');
            }

        } catch (error) {
            console.error('Cart update error:', error);
            showFlashMessage(error.message, 'error');
            reloadQuantities(itemId);
        }
    }

    // Вспомогательные функции
    function animateUpdate(itemId) {
        const item = document.querySelector(`${config.selectors.item}[data-item-id="${itemId}"]`);
        if (!item) return;

        item.style.transform = 'scale(1.02)';
        setTimeout(() => {
            item.style.transform = '';
        }, config.animationDuration);
    }

    function reloadQuantities(itemId) {
        const items = document.querySelectorAll(`${config.selectors.item}[data-item-id="${itemId}"]`);
        items.forEach(item => {
            const input = item.querySelector(config.selectors.quantityInput);
            if (input) input.value = input.dataset.originalValue || input.value;
        });
    }

    function showFlashMessage(text, type) {
        const existingAlerts = document.querySelectorAll('.alert');
        existingAlerts.forEach(alert => alert.remove());

        const message = document.createElement('div');
        message.className = `alert alert-${type} position-fixed top-0 start-50 translate-x mt-3`;
        message.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="bi bi-${type === 'success' ? 'check-circle' : 'exclamation-triangle'} me-2"></i>
                ${text}
            </div>
        `;

        document.body.appendChild(message);
        setTimeout(() => message.remove(), 3000);
    }

    // Обработчики событий
    function handleQuantityChange(itemId, newQuantity) {
        const input = document.querySelector(`${config.selectors.item}[data-item-id="${itemId}"] ${config.selectors.quantityInput}`);
        if (!input) return;

        const max = parseInt(input.max) || Infinity;
        const min = parseInt(input.min) || 1;
        newQuantity = Math.max(min, Math.min(newQuantity, max));

        updateCart(itemId, newQuantity);
    }

    // Инициализация
    function init() {
        // Сохраняем исходные значения
        document.querySelectorAll(config.selectors.quantityInput).forEach(input => {
            input.dataset.originalValue = input.value;
        });

        // Кнопки +/-
        document.querySelectorAll(config.selectors.plusBtn).forEach(btn => {
            btn.addEventListener('click', function () {
                const itemId = this.closest(config.selectors.item)?.dataset.itemId;
                if (!itemId) return;

                const input = this.parentElement.querySelector(config.selectors.quantityInput);
                handleQuantityChange(itemId, parseInt(input.value) + 1);
            });
        });

        document.querySelectorAll(config.selectors.minusBtn).forEach(btn => {
            btn.addEventListener('click', function () {
                const itemId = this.closest(config.selectors.item)?.dataset.itemId;
                if (!itemId) return;

                const input = this.parentElement.querySelector(config.selectors.quantityInput);
                handleQuantityChange(itemId, parseInt(input.value) - 1);
            });
        });

        // Ручной ввод
        document.querySelectorAll(config.selectors.quantityInput).forEach(input => {
            input.addEventListener('change', function () {
                const itemId = this.closest(config.selectors.item)?.dataset.itemId;
                if (itemId) handleQuantityChange(itemId, parseInt(this.value));
            });
        });
    }

    init();
});