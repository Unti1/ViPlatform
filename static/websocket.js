const dashboardId = window.location.pathname.split('/').pop();
console.log('Connecting to WebSocket with dashboardId:', dashboardId);
const socket = new WebSocket(`ws://${window.location.host}/ws/dashboard/${dashboardId}`);

socket.onopen = function() {
    console.log('WebSocket connection established');
};

socket.onmessage = function(event) {
    console.log('Received message:', event.data);
    const data = JSON.parse(event.data);
    if (data.type === 'update') {
        penStrokes = data.penStrokes || [];
        shapes = data.shapes || [];
        redraw();
    } else if (data.type === 'userList') {
        const userList = document.getElementById('userList');
        userList.innerHTML = '';
        data.users.forEach(user => {
            const li = document.createElement('li');
            li.textContent = `${user.name} ${user.surname}`;
            userList.appendChild(li);
        });
    } else if (data.type === 'error') {
        console.error('Server error:', data.message);
    }
};

socket.onerror = function(error) {
    console.error('WebSocket error:', error);
};

socket.onclose = function(event) {
    console.log('WebSocket closed with code:', event.code, 'reason:', event.reason);
};