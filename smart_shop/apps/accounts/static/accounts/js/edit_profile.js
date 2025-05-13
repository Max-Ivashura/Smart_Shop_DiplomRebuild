$(document).ready(function () {
            // Маска для телефона
            $('#id_phone').inputmask({
                mask: '+7 (999) 999-99-99',
                placeholder: ' ',
                showMaskOnHover: true,
                clearIncomplete: true,  // Разрешает частичный ввод
                greedy: false,
                onBeforePaste: function (pastedValue) {
                    // Автоматически добавляем +7 при вставке
                    pastedValue = pastedValue.replace(/\D/g, '');
                    if (pastedValue.startsWith('7') || pastedValue.startsWith('8') || pastedValue.startsWith('9')) {
                        return '+7' + pastedValue.slice(-10);
                    }
                    return pastedValue;
                }
            });

            // Предпросмотр аватарки
            $('#id_avatar').on('change', function (e) {
                const file = e.target.files[0];
                const reader = new FileReader();

                reader.onload = function (e) {
                    $('.avatar-preview img').attr('src', e.target.result);
                };

                if (file) {
                    reader.readAsDataURL(file);
                }
            });
        });