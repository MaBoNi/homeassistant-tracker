document.addEventListener('DOMContentLoaded', function() {
    fetchUsers();  // Fetch and populate users when the page loads
    fetchGPSData();  // Fetch default GPS data (for the first user) when the page loads
});

// Initialize map globally so it can be accessed in functions
let map = L.map('map').setView([55.6761, 12.5683], 12);  // Default center on Denmark
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

// The token and API URL will be replaced by the Docker entrypoint script
const token = '__TRACKER_APP_TOKEN__';  // Placeholder for the token
const backendApiUrl = '__BACKEND_API_URL__';  // Placeholder for the backend API URL

// Fetch users from the API and populate the dropdown
function fetchUsers() {
    const userSelect = document.getElementById('user-select');
    const url = `${backendApiUrl}/api/users`;  // API endpoint for fetching users

    fetch(url, {
        headers: {
            'Authorization': `Bearer ${token}`,  // Using token from the environment
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

// Fetch GPS data for the selected user and plot it on the map
function fetchGPSData(selectedUser) {
    const url = `${backendApiUrl}/api/gps-data?user=${selectedUser}&time_range=last_7_days`;  // URL with selected user

    fetch(url, {
        headers: {
            'Authorization': `Bearer ${token}`,  // Using token from the environment
        }
    })
    .then(response => response.json())
    .then(data => {
        const tableBody = document.querySelector('#gps-data-table tbody');
        const errorElement = document.getElementById('error');

        if (!data || data.length === 0) {
            errorElement.textContent = 'No data found!';
            return;
        }

        // Clear any previous data in the table body
        tableBody.innerHTML = '';
        errorElement.textContent = '';  // Clear previous errors

        // Clear the map layers before plotting new data
        map.eachLayer((layer) => {
            if (layer instanceof L.Marker || layer instanceof L.Polyline) {
                map.removeLayer(layer);
            }
        });

        const coordinates = [];  // Array to hold coordinates for the route

        // Populate table with data and collect coordinates for the map
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

            // Add coordinates to the array for the map
            coordinates.push([item.latitude, item.longitude]);
        });

        // Fit the map to the route (if there are coordinates)
        if (coordinates.length > 0) {
            // Add markers for the start and end of the route
            L.marker(coordinates[0]).addTo(map).bindPopup("Start").openPopup();  // Start
            L.marker(coordinates[coordinates.length - 1]).addTo(map).bindPopup("End");  // End

            // Draw the polyline (route) on the map
            L.polyline(coordinates, { color: 'blue' }).addTo(map);

            // Adjust map view to fit the plotted route
            map.fitBounds(coordinates);
        }
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        document.getElementById('error').textContent = 'Error fetching data';
    });
}
