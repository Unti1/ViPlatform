let questionIndex = 1;

function addQuestion() {
    const container = document.getElementById('questions');
    questionIndex++;
    
    const html = `
        <div id="question-${questionIndex}">
            <hr>
            <h4>Вопрос ${questionIndex}</h4>
            <textarea name="quiz_description[]" placeholder="Введите описание вопроса (можно использовать HTML для изображений)"></textarea>
            <textarea name="quiz_answers[]" placeholder="Введите ответ"></textarea>
            <button type="button" onclick="removeQuestion(${questionIndex})">Удалить</button>
        </div>
    `;
    container.insertAdjacentHTML('beforeend', html);
}

function removeQuestion(index) {
    document.getElementById(`question-${index}`).remove();
}