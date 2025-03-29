const canvas = document.getElementById('whiteboard');
const context = canvas.getContext('2d');
let isDrawing = false;
let lastX = 0;
let lastY = 0;
let tool = 'pen';
let previousTool = 'pen'; // Для хранения предыдущего инструмента перед "Ластиком"
let shapes = [];
let drag = false;
let dragStartX, dragStartY;

const toolButtons = document.querySelectorAll('.toolBtn');

// Функция для установки инструмента и обновления UI
function setTool(newTool) {
    tool = newTool;
    toolButtons.forEach(btn => {
        if (btn.dataset.tool === newTool) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    if (newTool === 'text') {
        document.getElementById('textInput').classList.remove('hidden');
        document.getElementById('textBox').focus();
    } else {
        document.getElementById('textInput').classList.add('hidden');
    }
}

function draw(e) {
    if (!isDrawing) return;
    const { offsetX, offsetY } = e;
    context.lineWidth = 2;
    context.strokeStyle = '#000';
    context.fillStyle = '#000';
    if (tool === 'pen') {
        context.lineTo(offsetX, offsetY);
        context.stroke();
        lastX = offsetX;
        lastY = offsetY;
    } else if (tool === 'line') {
        context.clearRect(0, 0, canvas.width, canvas.height);
        context.beginPath();
        context.moveTo(lastX, lastY);
        context.lineTo(offsetX, offsetY);
        context.stroke();
    } else if (tool === 'rectangle') {
        context.clearRect(0, 0, canvas.width, canvas.height);
        context.beginPath();
        context.rect(lastX, lastY, offsetX - lastX, offsetY - lastY);
        context.stroke();
    } else if (tool === 'circle') {
        context.clearRect(0, 0, canvas.width, canvas.height);
        const radius = Math.sqrt(Math.pow(offsetX - lastX, 2) + Math.pow(offsetY - lastY, 2));
        context.beginPath();
        context.arc(lastX, lastY, radius, 0, Math.PI * 2);
        context.stroke();
    }
}

canvas.addEventListener('mousedown', (e) => {
    isDrawing = true;
    lastX = e.offsetX;
    lastY = e.offsetY;
    if (tool === 'pen') {
        context.beginPath(); // Начинаем новый путь для "Ручки"
        context.moveTo(lastX, lastY); // Перемещаем курсор в начальную точку
    } else if (tool === 'line' || tool === 'rectangle' || tool === 'circle') {
        drag = true;
        dragStartX = e.offsetX;
        dragStartY = e.offsetY;
    }
});

canvas.addEventListener('mousemove', (e) => {
    if (tool === 'pen' && isDrawing) {
        draw(e);
    } else if (tool === 'line' || tool === 'rectangle' || tool === 'circle') {
        if (!drag) return;
        const { offsetX, offsetY } = e;
        context.clearRect(0, 0, canvas.width, canvas.height);
        shapes.forEach(shape => {
            if (shape.type === 'line') {
                context.beginPath();
                context.moveTo(shape.startX, shape.startY);
                context.lineTo(shape.endX, shape.endY);
                context.stroke();
            } else if (shape.type === 'rectangle') {
                context.beginPath();
                context.rect(shape.startX, shape.startY, shape.endX - shape.startX, shape.endY - shape.startY);
                context.stroke();
            } else if (shape.type === 'circle') {
                context.beginPath();
                context.arc(shape.startX, shape.startY, shape.radius, 0, Math.PI * 2);
                context.stroke();
            }
        });
        if (tool === 'line') {
            context.beginPath();
            context.moveTo(lastX, lastY);
            context.lineTo(offsetX, offsetY);
            context.stroke();
        } else if (tool === 'rectangle') {
            context.beginPath();
            context.rect(lastX, lastY, offsetX - lastX, offsetY - lastY);
            context.stroke();
        } else if (tool === 'circle') {
            const radius = Math.sqrt(Math.pow(offsetX - lastX, 2) + Math.pow(offsetY - lastY, 2));
            context.beginPath();
            context.arc(lastX, lastY, radius, 0, Math.PI * 2);
            context.stroke();
        }
    }
});

canvas.addEventListener('mouseup', (e) => {
    isDrawing = false;
    if (tool === 'line' || tool === 'rectangle' || tool === 'circle') {
        shapes.push({
            type: tool,
            startX: dragStartX,
            startY: dragStartY,
            endX: e.offsetX,
            endY: e.offsetY,
            radius: Math.sqrt(Math.pow(e.offsetX - dragStartX, 2) + Math.pow(e.offsetY - dragStartY, 2))
        });
    }
    drag = false;
});

document.getElementById('clearBtn').addEventListener('click', () => {
    context.clearRect(0, 0, canvas.width, canvas.height);
    shapes = [];
});

document.getElementById('eraserBtn').addEventListener('click', () => {
    if (tool !== 'eraser') {
        previousTool = tool; // Сохраняем текущий инструмент
        tool = 'eraser';
        toolButtons.forEach(btn => btn.classList.remove('active')); // Убираем подсветку с кнопок
    }
});

canvas.addEventListener('mousemove', (e) => {
    if (tool === 'eraser' && isDrawing) {
        const { offsetX, offsetY } = e;
        context.clearRect(offsetX - 5, offsetY - 5, 10, 10); // Стираем область
    }
});

// Отмена "Ластика" через ПКМ
canvas.addEventListener('contextmenu', (e) => {
    if (tool === 'eraser') {
        e.preventDefault(); // Предотвращаем стандартное контекстное меню
        setTool(previousTool); // Возвращаем предыдущий инструмент
    }
});

// Отмена "Ластика" через ESC
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && tool === 'eraser') {
        setTool(previousTool); // Возвращаем предыдущий инструмент
    }
});

// Обработчики кликов на кнопки инструментов
toolButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        setTool(btn.dataset.tool);
    });
});

document.getElementById('textBtn').addEventListener('click', () => {
    const text = document.getElementById('textBox').value;
    context.font = '16px Arial';
    context.fillText(text, lastX, lastY);
    document.getElementById('textInput').classList.add('hidden');
    setTool('pen'); // После добавления текста возвращаемся к "Ручке"
});

document.getElementById('imageBtn').addEventListener('click', () => {
    document.getElementById('imageInput').click();
});

document.getElementById('imageInput').addEventListener('change', (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = () => {
        const img = new Image();
        img.onload = () => {
            context.drawImage(img, 0, 0);
        };
        img.src = reader.result;
    };
    reader.readAsDataURL(file);
});

document.getElementById('saveBtn').addEventListener('click', () => {
    const image = canvas.toDataURL('image/png');
    const link = document.createElement('a');
    link.href = image;
    link.download = 'whiteboard.png';
    link.click();
});

// Устанавливаем начальный инструмент
setTool('pen');