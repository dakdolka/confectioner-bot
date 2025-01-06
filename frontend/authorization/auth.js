const form = document.getElementById('reg');
console.log('test');

    // Добавляем обработчик события отправки формы
form.addEventListener('submit', function(event) {
    event.preventDefault(); // Отменяем стандартное поведение формы

    // Отправляем данные на сервер с помощью Fetch API
    const formData = new FormData(form);
    fetch(form.action, {
    method: form.method,
    body: formData
    })
    .then(response => {
    if (response.ok) {
        // Если ответ успешный, выполняем редирект на другую страницу
        window.location.href = './auth.html'; // Замените на нужный URL
    } else {
        console.error('Ошибка при отправке данных');
    }
    })
    .catch(error => console.error('Ошибка при отправке:', error));
});