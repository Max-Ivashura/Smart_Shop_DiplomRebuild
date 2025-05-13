document.addEventListener('DOMContentLoaded', function () {
            // Переключение главного изображения
            document.querySelectorAll('.thumbnails img').forEach(thumb => {
                thumb.addEventListener('click', function () {
                    document.querySelector('#mainImage').src = this.dataset.mainSrc
                    document.querySelectorAll('.thumbnails img').forEach(t => t.classList.remove('active'))
                    this.classList.add('active')
                })
            })

            // Динамическое обновление избранного
            document.querySelectorAll('[data-wishlist-action]').forEach(button => {
                button.addEventListener('click', async (e) => {
                    e.preventDefault()
                    const response = await fetch(button.dataset.wishlistAction, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': '{{ csrf_token }}'
                        }
                    })
                    if (response.ok) location.reload()
                })
            })
        })