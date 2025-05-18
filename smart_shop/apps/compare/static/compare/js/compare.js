document.addEventListener('DOMContentLoaded', () => {
    // Обработчик для кнопок сравнения
    document.querySelectorAll('.compare-toggle').forEach(button => {
        button.addEventListener('click', async (e) => {
            const productId = e.currentTarget.dataset.productId;
            await toggleComparison(productId, e.currentTarget);
        });
    });

    // Обработчик для кнопок удаления в таблице
    document.querySelectorAll('.ts-compare-remove-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const productId = e.currentTarget.dataset.productId;
            await toggleComparison(productId, null, true);
        });
    });

    // Обработчик переключения вкладок
    document.querySelectorAll('.ts-compare-tabs .nav-link').forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            switchCategory(this.getAttribute('href').split('=')[1]);
        });
    });
});

async function toggleComparison(productId, button, isTableDelete = false) {
    try {
        const response = await fetch(`/compare/toggle/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();
        if (data.status === 'success') {
            // Обновление кнопок в интерфейсе
            if (button) {
                const textSpan = button.querySelector('.compare-text');
                textSpan.textContent = data.action === 'added' ? 'В сравнении' : 'Сравнить';
            }

            // Полное обновление блока сравнения
            const comparisonHTML = await fetchComparisonContent();
            updateComparisonInterface(comparisonHTML);

            // Обновление счетчиков в хедере
            updateHeaderCounters(data.product_ids.length);
        }
    } catch (error) {
        console.error('Ошибка при обновлении сравнения:', error);
    }
}

async function fetchComparisonContent() {
    const response = await fetch(window.location.href);
    const text = await response.text();
    const parser = new DOMParser();
    return parser.parseFromString(text, 'text/html');
}

function updateComparisonInterface(comparisonHTML) {
    // Обновление основной секции
    const newContent = comparisonHTML.querySelector('.ts-compare-container').innerHTML;
    document.querySelector('.ts-compare-container').innerHTML = newContent;

    // Обновление обработчиков
    document.querySelectorAll('.ts-compare-remove-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const productId = e.currentTarget.dataset.productId;
            await toggleComparison(productId, null, true);
        });
    });

    document.querySelectorAll('.ts-compare-tabs .nav-link').forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            switchCategory(this.getAttribute('href').split('=')[1]);
        });
    });
}

function switchCategory(categoryId) {
    // Переключение активной вкладки
    document.querySelectorAll('.ts-compare-tabs .nav-link').forEach(tab => {
        tab.classList.remove('active');
        if (tab.getAttribute('href').includes(categoryId)) {
            tab.classList.add('active');
        }
    });

    // Переключение контента
    document.querySelectorAll('.ts-compare-category-content').forEach(content => {
        content.classList.add('d-none');
        if (content.dataset.categoryId === categoryId) {
            content.classList.remove('d-none');
        }
    });
}

function updateHeaderCounters(count) {
    // Обновление всех счетчиков сравнения
    document.querySelectorAll('.comparison-count').forEach(span => {
        span.textContent = count > 0 ? `(${count})` : '';
        span.classList.add('updated');
        setTimeout(() => span.classList.remove('updated'), 500);
    });
}

// Вспомогательная функция для CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}