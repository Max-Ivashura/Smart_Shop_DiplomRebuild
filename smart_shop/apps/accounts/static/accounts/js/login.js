// accounts/static/accounts/js/login.js

document.addEventListener('DOMContentLoaded', () => {
    // Переключение видимости пароля
    const passwordToggle = document.querySelector('.password-toggle');
    const passwordInput = document.getElementById('id_password');
    
    if (passwordToggle && passwordInput) {
        passwordToggle.addEventListener('click', () => {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            passwordToggle.querySelector('i').classList.toggle('bi-eye-slash');
            passwordToggle.querySelector('i').classList.toggle('bi-eye');
        });
    }
});