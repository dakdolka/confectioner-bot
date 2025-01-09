const form = document.getElementById('reg');

form.addEventListener('submit', function(event) {
    event.preventDefault(); // Отменяем стандартное поведение формы
    const formData = new FormData(form);
    fetch(form.action, {
    method: form.method,
    body: formData
    })
    .then(response => {
    if (response.ok) {
        // Если ответ успешный, выполняем редирект на другую страницу, гпт помог
        window.location.href = './auth.html'; // TODO заменить на нужный URL
    } else {
        console.error('Ошибка при отправке данных');
    }
    })
    .catch(error => console.error('Ошибка при отправке:', error));
});

const form_1 = document.getElementById('enter');

form_1.addEventListener('submit', function(event) {
    event.preventDefault(); // Отменяем стандартное поведение формы
    const formData = new FormData(form);
    fetch(form.action, {
    method: form.method,
    body: formData
    })
    .then(response => {
    if (response.ok) {
        // Если ответ успешный, выполняем редирект на другую страницу, гпт помог
        window.location.href = './auth.html'; // TODO заменить на нужный URL
    } else {
        console.error('Ошибка при отправке данных');
    }
    })
    .catch(error => console.error('Ошибка при отправке:', error));
});
