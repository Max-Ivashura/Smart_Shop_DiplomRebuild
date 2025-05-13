// theme.js

document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement;

    // Определение текущей темы
    const currentTheme = localStorage.getItem('theme') ||
        (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');

    htmlElement.setAttribute('data-bs-theme', currentTheme);
    updateThemeIcon(currentTheme);

    // Обработчик переключения
    themeToggle.addEventListener('click', () => {
        const newTheme = htmlElement.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark';
        htmlElement.setAttribute('data-bs-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });

    // Обновление иконки
    function updateThemeIcon(theme) {
        const icon = theme === 'dark'
            ? '<i class="bi bi-moon-stars-fill"></i>'
            : '<i class="bi bi-brightness-high-fill"></i>';
        themeToggle.innerHTML = icon;
    }

    // Синхронизация с системными настройками
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        const systemTheme = e.matches ? 'dark' : 'light';
        if (!localStorage.getItem('theme')) {
            htmlElement.setAttribute('data-bs-theme', systemTheme);
            updateThemeIcon(systemTheme);
        }
    });
});