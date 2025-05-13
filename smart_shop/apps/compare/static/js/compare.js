document.querySelectorAll('.compare-toggle').forEach(button => {
    button.addEventListener('click', async (e) => {
        const productId = e.currentTarget.dataset.productId;
        const response = await fetch(`/compare/toggle/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();
        if (data.status === 'success') {
            // Обновляем интерфейс
            const textSpan = e.currentTarget.querySelector('.compare-text');
            textSpan.textContent = data.action === 'added' ? 'В сравнении' : 'Сравнить';

            // Обновляем счетчик
            const countSpan = document.querySelector('.compare-count');
            countSpan.textContent = data.count > 0 ? `(${data.count})` : '';
        }
    });
});

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