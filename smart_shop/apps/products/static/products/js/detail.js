document.addEventListener('DOMContentLoaded', function () {
    const thumbs = document.querySelectorAll('.ts-thumb-wrap');
    const mainImage = document.querySelector('#mainImage');

    thumbs.forEach(thumb => {
        thumb.addEventListener('click', function () {
            // Удаляем активный класс у всех превью
            thumbs.forEach(t => t.classList.remove('active'));

            // Добавляем активный класс текущему превью
            this.classList.add('active');

            // Обновляем основное изображение
            const newSrc = this.dataset.image;
            mainImage.src = newSrc;

            // Плавное обновление
            mainImage.style.opacity = 0;
            setTimeout(() => {
                mainImage.style.opacity = 1;
            }, 150);
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('reviewForm');
    const showBtn = document.getElementById('showReviewForm');
    const cancelBtn = document.getElementById('cancelReview');
    const stars = document.querySelectorAll('.star-btn');

    // Сброс звезд при открытии формы
    const resetStars = () => {
        stars.forEach(star => {
            star.classList.remove('active');
            star.querySelector('.bi').classList.remove('bi-star-fill');
            star.querySelector('.bi').classList.add('bi-star');
        });
        document.getElementById('id_rating').value = 5;
        stars[4].click(); // Устанавливаем 5 звезд по умолчанию
    };

    // Показать форму
    showBtn?.addEventListener('click', (e) => {
        e.preventDefault();
        form.style.display = 'block';
        resetStars();
        window.scrollTo({top: form.offsetTop - 100, behavior: 'smooth'});
    });

    // Скрыть форму
    cancelBtn?.addEventListener('click', () => {
        form.style.display = 'none';
        resetStars();
    });

    // Обработка звезд
    stars.forEach((star, index) => {
        star.addEventListener('click', function () {
            const value = index + 1;

            // Обновляем все звезды
            stars.forEach((s, i) => {
                const icon = s.querySelector('.bi');
                if (i <= index) {
                    icon.classList.add('bi-star-fill');
                    icon.classList.remove('bi-star');
                } else {
                    icon.classList.add('bi-star');
                    icon.classList.remove('bi-star-fill');
                }
            });

            document.getElementById('id_rating').value = value;
        });
    });
});



document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('.stars');
    stars.forEach(star => {
        const rating = parseFloat(star.dataset.rating).toFixed(1); // Берем точное значение
        star.style.setProperty('--rating', rating);
    });
});