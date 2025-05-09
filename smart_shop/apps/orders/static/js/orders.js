// Модальное окно отмены заказа
document.addEventListener('DOMContentLoaded', function () {
    const cancelModal = document.getElementById('cancelOrderModal');
    if (cancelModal) {
        cancelModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const orderId = button.getAttribute('data-order-id');
        });
    }

    // Динамическое обновление статуса (пример)
    function updateOrderStatus(orderId, newStatus) {
        fetch(`/orders/${orderId}/update_status/`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({status: newStatus})
        }).then(response => {
            if (response.ok) {
                window.location.reload();
            }
        });
    }
});