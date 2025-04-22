
// Получаем элементы
const openPopupBtn = document.getElementById('openPopup');
const popup = document.getElementById('create-dash-popup');
const closePopupBtn = document.getElementById('closePopup');
const form = document.getElementById('DashCreateForm');

// Открытие popup при клике на кнопку
openPopupBtn.addEventListener('click', () => {
    popup.style.display = 'flex';
});

// Закрытие popup при клике на крестик
closePopupBtn.addEventListener('click', () => {
    popup.style.display = 'none';
});

// Закрытие popup при клике вне формы
window.addEventListener('click', (event) => {
    if (event.target === popup) {
        popup.style.display = 'none';
    }
});

// // Обработка отправки формы
// form.addEventListener('submit', (event) => {
//     event.preventDefault(); // Предотвращаем перезагрузку страницы
//     const title = document.getElementById('title').value;
//     const group = document.getElementById('group').value;
//     console.log('Название:', title, 'Для группы:', group); // Выводим данные в консоль
//     popup.style.display = 'none'; // Закрываем popup после отправки
//     form.reset(); // Очищаем форму
// });