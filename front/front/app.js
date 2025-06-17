async function fetchRooms() {
  const table = document.getElementById('roomsTable');
  const tbody = table.querySelector('tbody');
  tbody.innerHTML = '';
  table.style.display = 'table';

  try {
    const response = await fetch('http://ec2-44-211-61-87.compute-1.amazonaws.com:3000/rooms');
    const rooms = await response.json();

    if (rooms.length === 0) {
      tbody.innerHTML = '<tr><td colspan="2">No rooms found.</td></tr>';
      return;
    }

    rooms.forEach(room => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${room.id}</td>
        <td>Last update: ${room.datetime}</td>
        <td style="color:${room.roomIsEmpty === true ? 'green' : 'red'};">
          ${room.roomIsEmpty === true ? 'EMPTY' : 'BUSY'}
        </td>
      `;
      tbody.appendChild(row);
    });
  } catch (err) {
    tbody.innerHTML = '<tr><td colspan="2">Error loading rooms.</td></tr>';
  }
}
