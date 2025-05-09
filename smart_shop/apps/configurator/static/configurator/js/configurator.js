// apps/configurator/static/configurator/js/configurator.js
document.addEventListener('DOMContentLoaded', function () {
    // Динамическое обновление прогресс-бара
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        progressBar.style.width = progressBar.getAttribute('aria-valuenow') + '%';
    }


});

// Динамическое обновление стоимости
function updateTotalPrice() {
    fetch('/configurator/api/build-price/')  // Создайте API-эндпоинт для получения цены
        .then(response => response.json())
        .then(data => {
            document.getElementById('total-price').textContent = data.total_price;
        });
}

// Вызывать при загрузке и после добавления компонента
document.addEventListener('DOMContentLoaded', updateTotalPrice);