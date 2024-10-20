document.addEventListener('DOMContentLoaded', function() {
    fetchUsers();  // Fetch and populate users when the page loads
    fetchGPSData();  // Fetch default GPS data (for the first user) when the page loads
});

// Fetch users from the API and populate the dropdown
function fetchUsers() {
    const userSelect = document.getElementById('user-select');
    const url = `http://localhost:5171/api/users`;  // API endpoint for fetching users

    fetch(url, {
        headers: {
            'Authorization': 'Bearer your_static_token',
        }
    })
    .then(response => response.json())
    .then(users => {
        if (!users || users.length === 0) {
            document.getElementById('error').textContent = 'No users found!';
            return;
        }

        // Populate the dropdown with users
        users.forEach(user => {
            const option = document.createElement('option');
            option.value = user;
            option.textContent = user;
            userSelect.appendChild(option);
        });

        // Trigger fetching data for the first user in the list
        fetchGPSData(userSelect.value);
    })
    .catch(error => {
        console.error('Error fetching users:', error);
        document.getElementById('error').textContent = 'Error fetching users';
    });

    // Add event listener to reload data when the user changes
    userSelect.addEventListener('change', function() {
        fetchGPSData(userSelect.value);
    });
}

// Fetch GPS data for the selected user
function fetchGPSData(selectedUser) {
    const url = `http://localhost:5171/api/gps-data?user=${selectedUser}&time_range=last_7_days`;  // URL with selected user

    fetch(url, {
        headers: {
            'Authorization': 'Bearer your_static_token',
        }
    })
    .then(response => response.json())
    .then(data => {
        const tableBody = document.querySelector('#gps-data-table tbody');

        if (!data || data.length === 0) {
            document.getElementById('error').textContent = 'No data found!';
            return;
        }

        // Clear any previous data in the table body
        tableBody.innerHTML = '';

        // Populate table with data
        data.forEach(item => {
            const row = document.createElement('tr');

            row.innerHTML = `
                <td>${item.user}</td>
                <td>${item.device}</td>
                <td>${item.latitude}</td>
                <td>${item.longitude}</td>
                <td>${new Date(item.timestamp).toLocaleString()}</td>
                <td>${item.accuracy || 'N/A'}</td>
            `;

            tableBody.appendChild(row);
        });
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        document.getElementById('error').textContent = 'Error fetching data';
    });
}
