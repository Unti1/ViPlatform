let questions = [{ id: 0, type: 'text' }];


// Обновление типа ответа
function updateAnswerType(id) {
    const type = document.getElementById(`answer-type-${id}`).value;
    const contentDiv = document.getElementById(`answer-content-${id}`);
    contentDiv.innerHTML = '';
    if (type === 'text') {
        contentDiv.innerHTML = `<textarea id="answer-text-${id}" class="tinymce"></textarea>`;
        tinymce.init({ selector: `#answer-text-${id}` });
    } else if (type === 'choices') {
        contentDiv.innerHTML = `
            <div class="choices-container" id="choices-${id}">
                <div class="choice">
                    <input type="text" id="choice-${id}-0" placeholder="Вариант 1">
                </div>
            </div>
            <button class="add-choice-btn" onclick="addChoice(${id})">+</button>
        `;
    }
    questions.find(q => q.id === id).type = type;
}

// Добавление нового варианта ответа
function addChoice(questionId) {
    const choicesContainer = document.getElementById(`choices-${questionId}`);
    const choiceCount = choicesContainer.children.length;
    const newChoice = document.createElement('div');
    newChoice.className = 'choice';
    newChoice.innerHTML = `<input type="text" id="choice-${questionId}-${choiceCount}" placeholder="Вариант ${choiceCount + 1}">`;
    choicesContainer.appendChild(newChoice);
}

// Добавление нового вопроса
function addNewQuestion() {
    const newId = questions.length;
    questions.push({ id: newId, type: 'text' });
    const container = document.getElementById('questions-container');
    const newBlock = document.createElement('div');
    newBlock.className = 'question-block';
    newBlock.dataset.id = newId;
    newBlock.innerHTML = `
        <label>Вопрос:</label>
        <textarea id="question-editor-${newId}" class="tinymce"></textarea>
        <div class="answer-type">
            <label>Тип ответа:</label>
            <select id="answer-type-${newId}" onchange="updateAnswerType(${newId})">
                <option value="text">Текст</option>
                <option value="choices">Варианты выбора</option>
            </select>
        </div>
        <div id="answer-content-${newId}">
            <textarea id="answer-text-${newId}" class="tinymce"></textarea>
        </div>
    `;
    container.appendChild(newBlock);
    tinymce.init({ selector: `#question-editor-${newId}, #answer-text-${newId}` });
}

// Сохранение теста
async function saveQuiz() {
    const quizData = {
        user_id: 1, // Замените на реальный user_id из вашей системы аутентификации
        title: document.getElementById('quiz-title').value,
        description: tinymce.get('quiz-description').getContent(),
        quiz_description: questions.map(q => tinymce.get(`question-editor-${q.id}`).getContent()),
        quiz_answers: questions.map(q => {
            if (q.type === 'text') {
                return tinymce.get(`answer-text-${q.id}`).getContent();
            } else {
                const choices = [];
                const container = document.getElementById(`choices-${q.id}`);
                for (let i = 0; i < container.children.length; i++) {
                    choices.push(document.getElementById(`choice-${q.id}-${i}`).value);
                }
                return choices;
            }
        })
    };

    try {
        const response = await fetch('/quizzes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(quizData)
        });
        if (response.ok) {
            alert('Тест успешно сохранен!');
        } else {
            alert('Ошибка при сохранении теста');
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при сохранении');
    }
}

// Обработчики событий
document.getElementById('add-question-btn').addEventListener('click', addNewQuestion);
document.getElementById('save-btn').addEventListener('click', saveQuiz);
