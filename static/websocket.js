const dashboardId = window.location.pathname.split('/').pop(); // Предполагается, что ID доски в URL
const socket = new WebSocket(`ws://${window.location.host}/ws/dashboard/${dashboardId}`);

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type === 'update') {
        penStrokes = data.penStrokes || [];
        shapes = data.shapes || [];
        redraw(); // Предполагается, что у вас есть функция redraw для перерисовки
    } else if (data.type === 'userList') {
        const userList = document.getElementById('userList');
        userList.innerHTML = '';
        data.users.forEach(user => {
            const li = document.createElement('li');
            li.textContent = `${user.name} ${user.surname}`;
            userList.appendChild(li);
        });
    }
};