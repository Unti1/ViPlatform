let questionCounter = 1;

function addQuestion() {
    const container = document.getElementById('questions-container');
    const questionBlock = document.createElement('div');
    questionBlock.className = 'question-block bg-white p-6 rounded-lg shadow';
    questionBlock.dataset.id = questionCounter;

    questionBlock.innerHTML = `
        <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-semibold">Вопрос ${questionCounter + 1}</h3>
            <button class="delete-question text-red-500 hover:text-red-700" onclick="deleteQuestion(${questionCounter})">
                <i class="fas fa-trash"></i> Удалить
            </button>
        </div>

        <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2">Текст вопроса:</label>
            <textarea id="question-editor-${questionCounter}" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" rows="3"></textarea>
        </div>

        <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2">Тип ответа:</label>
            <select id="answer-type-${questionCounter}" onchange="updateAnswerType(${questionCounter})" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
                <option value="text">Текст</option>
                <option value="choices">Варианты выбора</option>
            </select>
        </div>

        <div id="answer-content-${questionCounter}" class="mt-4">
            <div id="text-answer-${questionCounter}">
                <label class="block text-gray-700 text-sm font-bold mb-2">Правильный ответ:</label>
                <textarea id="answer-text-${questionCounter}" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" rows="3"></textarea>
            </div>
            <div id="choices-answer-${questionCounter}" class="hidden">
                <label class="block text-gray-700 text-sm font-bold mb-2">Варианты ответов:</label>
                <div id="choices-container-${questionCounter}" class="space-y-2">
                    <div class="choice-item flex items-center space-x-2">
                        <input type="radio" name="correct-${questionCounter}" value="0" class="form-radio">
                        <input type="text" class="choice-text shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" placeholder="Вариант ответа">
                    </div>
                </div>
                <button onclick="addChoice(${questionCounter})" class="mt-2 text-blue-500 hover:text-blue-700">
                    <i class="fas fa-plus"></i> Добавить вариант
                </button>
            </div>
        </div>
    `;

    container.appendChild(questionBlock);
    questionCounter++;
}

function deleteQuestion(id) {
    const questionBlock = document.querySelector(`.question-block[data-id="${id}"]`);
    if (questionBlock) {
        questionBlock.remove();
    }
}

function updateAnswerType(id) {
    const type = document.getElementById(`answer-type-${id}`).value;
    const textAnswer = document.getElementById(`text-answer-${id}`);
    const choicesAnswer = document.getElementById(`choices-answer-${id}`);

    if (type === 'text') {
        textAnswer.classList.remove('hidden');
        choicesAnswer.classList.add('hidden');
    } else {
        textAnswer.classList.add('hidden');
        choicesAnswer.classList.remove('hidden');
    }
}

function addChoice(questionId) {
    const container = document.getElementById(`choices-container-${questionId}`);
    const choiceCount = container.children.length;
    
    const choiceItem = document.createElement('div');
    choiceItem.className = 'choice-item flex items-center space-x-2';
    choiceItem.innerHTML = `
        <input type="radio" name="correct-${questionId}" value="${choiceCount}" class="form-radio">
        <input type="text" class="choice-text shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" placeholder="Вариант ответа">
        <button onclick="removeChoice(this)" class="text-red-500 hover:text-red-700">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    container.appendChild(choiceItem);
}

function removeChoice(button) {
    button.parentElement.remove();
}

async function saveQuiz() {
    const title = document.getElementById('quiz-title').value;
    const description = document.getElementById('quiz-description').value;
    const timer = parseInt(document.getElementById('quiz-timer').value) * 60; // конвертируем минуты в секунды
    const deadline = document.getElementById('quiz-deadline').value;
    const maxAttempts = parseInt(document.getElementById('quiz-max-attempts').value);
    const minPercentage = parseFloat(document.getElementById('quiz-min-percentage').value);

    const questions = [];
    const questionBlocks = document.querySelectorAll('.question-block');

    for (const block of questionBlocks) {
        const id = block.dataset.id;
        const questionText = document.getElementById(`question-editor-${id}`).value;
        const answerType = document.getElementById(`answer-type-${id}`).value;
        
        let answer;
        if (answerType === 'text') {
            answer = document.getElementById(`answer-text-${id}`).value;
        } else {
            const choices = Array.from(document.querySelectorAll(`#choices-container-${id} .choice-text`))
                .map(input => input.value);
            const correctIndex = parseInt(document.querySelector(`input[name="correct-${id}"]:checked`).value);
            answer = {
                choices,
                correctIndex
            };
        }

        questions.push({
            text: questionText,
            type: answerType,
            answer
        });
    }

    const quizData = {
        title,
        description,
        timer,
        deadline: deadline ? new Date(deadline).toISOString().slice(0, 19).replace('T', ' ') : null,
        max_attempts: maxAttempts,
        min_pass_percentage: minPercentage,
        quiz_description: {
            questions
        },
        quiz_answers: {
            answers: questions.map(q => q.answer)
        }
    };

    try {
        // Получаем CSRF токен из куки
        const csrfToken = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrf_access_token='))
            ?.split('=')[1];

        const response = await fetch('/quizzes/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': csrfToken
            },
            credentials: 'include', // Важно для отправки куки
            body: JSON.stringify(quizData)
        });

        if (response.ok) {
            const result = await response.json();
            window.location.href = `/quizzes/${result.quiz_id}`;
        } else {
            const error = await response.json();
            alert(`Ошибка: ${error.detail}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Произошла ошибка при сохранении теста');
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Добавляем обработчики событий
    document.getElementById('add-question-btn').addEventListener('click', addQuestion);
    document.getElementById('save-btn').addEventListener('click', saveQuiz);
});
