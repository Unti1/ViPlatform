const canvas = document.getElementById('whiteboard');
const context = canvas.getContext('2d');
let isDrawing = false;
let lastX = 0;
let lastY = 0;
let tool = 'pen';
let previousTool = 'pen';
let shapes = [];
let penStrokes = []; // Массив для хранения штрихов ручки
let currentStroke = []; // Текущий штрих ручки
let drag = false;
let dragStartX, dragStartY;
let currentColor = 'black'; // Текущий цвет ручки

const toolButtons = document.querySelectorAll('.toolBtn');
const cursorIcon = document.getElementById('cursorIcon');

// Установка инструмента и обновление UI
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

    if (newTool === 'pen') {
        document.getElementById('colorContainer').classList.remove('hidden');
    } else {
        document.getElementById('colorContainer').classList.add('hidden');
    }
    
    updateCursorIcon(newTool);
}

// Обновление иконки курсора
function updateCursorIcon(tool) {
    let svg = '';
    switch (tool) {
        case 'pen':
            svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"></path><path d="M16.5 3.5l4 4L7 21H3v-4L16.5 3.5z"></path></svg>';
            break;
        case 'line':
            svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="5" x2="19" y2="19"></line></svg>';
            break;
        case 'rectangle':
            svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect></svg>';
            break;
        case 'circle':
            svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle></svg>';
            break;
        case 'text':
            svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3H7v18h10V3z"></path><path d="M11 7h2"></path><path d="M11 11h2"></path><path d="M11 15h2"></path></svg>';
            break;
        case 'eraser':
            svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 4H8l-7 8 7 8h13a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2z"></path><line x1="18" y1="9" x2="12" y2="15"></line><line x1="12" y1="9" x2="18" y2="15"></line></svg>';
            break;
    }
    cursorIcon.innerHTML = svg;
}

// Перерисовка всех элементов
function redraw() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    // Рисуем штрихи ручки
    penStrokes.forEach(stroke => {
        context.beginPath();
        context.strokeStyle = stroke.color;
        context.moveTo(stroke.points[0].x, stroke.points[0].y);
        for (let i = 1; i < stroke.points.length; i++) {
            context.lineTo(stroke.points[i].x, stroke.points[i].y);
        }
        context.stroke();
    });
    // Рисуем фигуры
    shapes.forEach(shape => {
        context.beginPath();
        context.strokeStyle = '#000';
        if (shape.type === 'line') {
            context.moveTo(shape.startX, shape.startY);
            context.lineTo(shape.endX, shape.endY);
        } else if (shape.type === 'rectangle') {
            context.rect(shape.startX, shape.startY, shape.endX - shape.startX, shape.endY - shape.startY);
        } else if (shape.type === 'circle') {
            context.arc(shape.startX, shape.startY, shape.radius, 0, Math.PI * 2);
        }
        context.stroke();
    });
}

canvas.addEventListener('mousedown', (e) => {
    isDrawing = true;
    lastX = e.offsetX;
    lastY = e.offsetY;
    if (tool === 'pen') {
        currentStroke = [{ x: lastX, y: lastY }];
        context.beginPath();
        context.moveTo(lastX, lastY);
        context.strokeStyle = currentColor;
    } else if (tool === 'line' || tool === 'rectangle' || tool === 'circle') {
        drag = true;
        dragStartX = e.offsetX;
        dragStartY = e.offsetY;
    }
});

canvas.addEventListener('mousemove', (e) => {
    const { offsetX, offsetY } = e;
    // Обновляем позицию иконки курсора
    cursorIcon.style.left = `${e.clientX}px`;
    cursorIcon.style.top = `${e.clientY}px`;

    if (tool === 'pen' && isDrawing) {
        currentStroke.push({ x: offsetX, y: offsetY });
        context.lineTo(offsetX, offsetY);
        context.stroke();
        lastX = offsetX;
        lastY = offsetY;
    } else if (tool === 'line' || tool === 'rectangle' || tool === 'circle') {
        if (!drag) return;
        redraw(); // Перерисовываем все элементы
        context.beginPath();
        context.strokeStyle = '#000';
        if (tool === 'line') {
            context.moveTo(lastX, lastY);
            context.lineTo(offsetX, offsetY);
        } else if (tool === 'rectangle') {
            context.rect(lastX, lastY, offsetX - lastX, offsetY - lastY);
        } else if (tool === 'circle') {
            const radius = Math.sqrt(Math.pow(offsetX - lastX, 2) + Math.pow(offsetY - lastY, 2));
            context.arc(lastX, lastY, radius, 0, Math.PI * 2);
        }
        context.stroke();
    } else if (tool === 'eraser' && isDrawing) {
        context.clearRect(offsetX - 5, offsetY - 5, 10, 10);
        penStrokes = penStrokes.filter(stroke => {
            return !stroke.points.some(point => Math.abs(point.x - offsetX) < 5 && Math.abs(point.y - offsetY) < 5);
        });
        shapes = shapes.filter(shape => {
            if (shape.type === 'line') {
                return !(Math.abs(shape.startX - offsetX) < 5 && Math.abs(shape.startY - offsetY) < 5 ||
                         Math.abs(shape.endX - offsetX) < 5 && Math.abs(shape.endY - offsetY) < 5);
            } else if (shape.type === 'rectangle') {
                return !(offsetX > shape.startX && offsetX < shape.endX && offsetY > shape.startY && offsetY < shape.endY);
            } else if (shape.type === 'circle') {
                const dist = Math.sqrt(Math.pow(offsetX - shape.startX, 2) + Math.pow(offsetY - shape.startY, 2));
                return dist > shape.radius;
            }
            return true;
        });
        redraw();
    }
});

canvas.addEventListener('mouseup', (e) => {
    isDrawing = false;
    if (tool === 'pen') {
        penStrokes.push({ points: currentStroke, color: currentColor });
        currentStroke = [];
    } else if (tool === 'line' || tool === 'rectangle' || tool === 'circle') {
        shapes.push({
            type: tool,
            startX: dragStartX,
            startY: dragStartY,
            endX: e.offsetX,
            endY: e.offsetY,
            radius: Math.sqrt(Math.pow(e.offsetX - dragStartX, 2) + Math.pow(e.offsetY - dragStartY, 2))
        });
        redraw();
    }
    drag = false;
});

document.getElementById('clearBtn').addEventListener('click', () => {
    context.clearRect(0, 0, canvas.width, canvas.height);
    shapes = [];
    penStrokes = [];
});

document.getElementById('eraserBtn').addEventListener('click', () => {
    if (tool !== 'eraser') {
        previousTool = tool;
        tool = 'eraser';
        toolButtons.forEach(btn => btn.classList.remove('active'));
        updateCursorIcon('eraser');
    }
});

canvas.addEventListener('contextmenu', (e) => {
    if (tool === 'eraser') {
        e.preventDefault();
        setTool(previousTool);
    }
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && tool === 'eraser') {
        setTool(previousTool);
    }
});

toolButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        setTool(btn.dataset.tool);
    });
});

document.getElementById('colorSelect').addEventListener('change', (e) => {
    currentColor = e.target.value;
});

setTool('pen');

function resizeCanvas() {
    const container = canvas.parentElement;
    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;
    redraw();
}

window.addEventListener('resize', resizeCanvas);
resizeCanvas();