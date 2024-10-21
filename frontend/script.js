// Function to update the "Last updated at" time
function updateLastUpdatedTime() {
    const lastUpdatedElement = document.getElementById('last-updated');
    const currentTime = new Date().toLocaleTimeString([], { hour12: false });  // 24-hour format
    console.log(`Last updated time: ${currentTime}`);  // <-- Log for debugging
    lastUpdatedElement.textContent = `Last updated: ${currentTime}`;
}

document.addEventListener('DOMContentLoaded', function() {
    fetchUsers();  // Fetch and populate users when the page loads

    // Function to update local time
    function updateLocalTime() {
        const localTimeElement = document.getElementById('local-time');
        const currentTime = new Date().toLocaleTimeString([], { hour12: false });  // 24-hour format
        localTimeElement.textContent = `Local Time: ${currentTime}`;
    }

    // Update local time every second
    updateLocalTime();
    setInterval(updateLocalTime, 1000);
});


// Initialize map globally so it can be accessed in functions
let map = L.map('map').setView([55.6761, 12.5683], 12);  // Default center on Denmark
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

// The token and API URL will be replaced by the Docker entrypoint script
const token = '__TRACKER_APP_TOKEN__';  // Placeholder for the token
const backendApiUrl = '__BACKEND_API_URL__';  // Placeholder for the backend API URL

// Helper function to convert ISO timestamp to local time, assuming the API is sending UTC timestamps
function convertUTCToLocal(utcDateString) {
    const utcDate = new Date(utcDateString + 'Z');  // Append 'Z' to treat it as UTC
    return utcDate.toLocaleString([], { hour12: false });  // Convert to 24-hour local time
}

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

        // Add a placeholder option to prompt the user to select someone
        const placeholderOption = document.createElement('option');
        placeholderOption.value = '';
        placeholderOption.textContent = 'Select a user';
        placeholderOption.disabled = true;
        placeholderOption.selected = true;
        userSelect.appendChild(placeholderOption);

        // Populate the dropdown with users
        users.forEach(user => {
            const option = document.createElement('option');
            option.value = user;
            option.textContent = user;
            userSelect.appendChild(option);
        });
    })
    .catch(error => {
        console.error('Error fetching users:', error);
        document.getElementById('error').textContent = 'Error fetching users';
    });

    // Add event listener to fetch data when a valid user is selected
    userSelect.addEventListener('change', function() {
        if (userSelect.value !== '') {
            fetchGPSData(userSelect.value);  // Fetch data for the selected user
            updateLastUpdatedTime();  // Update the "Last updated at" time when user changes
        }
    });
}

// Fetch GPS data for the selected user and time range, and plot it on the map
function fetchGPSData(selectedUser) {
    const timeSelect = document.getElementById('time-select');
    const timeRange = timeSelect.value;
    const url = `${backendApiUrl}/api/gps-data?user=${selectedUser}&time_range=${timeRange}`;  // URL with selected user and time range

    fetch(url, {
        headers: {
            'Authorization': `Bearer ${token}`,  // Using token from the environment
        }
    })
    .then(response => response.json())
    .then(data => {
        const tableBody = document.querySelector('#gps-data-table tbody');
        const errorElement = document.getElementById('error');

        // Clear previous data
        tableBody.innerHTML = '';  // Clear the table body
        map.eachLayer(layer => {   // Clear existing map markers and polylines
            if (layer instanceof L.Marker || layer instanceof L.Polyline) {
                map.removeLayer(layer);
            }
        });

        if (!data || data.length === 0) {
            errorElement.textContent = 'No data found!';
            return;
        }

        errorElement.textContent = '';  // Clear previous errors
        const coordinates = [];  // Array to hold coordinates for the route

        // Populate table with data and collect coordinates for the map
        data.forEach(item => {
            const localTimestamp = convertUTCToLocal(item.timestamp);  // Convert to local time

            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.user}</td>
                <td>${item.device}</td>
                <td>${item.latitude}</td>
                <td>${item.longitude}</td>
                <td>${localTimestamp}</td>
                <td>${item.accuracy || 'N/A'}</td>
            `;
            tableBody.appendChild(row);

            // Add coordinates to the array for the map
            const coordinate = [item.latitude, item.longitude];
            coordinates.push(coordinate);

            // Add a marker for each GPS location
            const marker = L.marker(coordinate).addTo(map);
            marker.bindPopup(`Time: ${localTimestamp}`);
        });

        // Fit the map to the route (if there are coordinates)
        if (coordinates.length > 0) {
            const startLocalTime = convertUTCToLocal(data[0].timestamp);
            const endLocalTime = convertUTCToLocal(data[data.length - 1].timestamp);

            // Add markers for the start and end of the route
            L.marker(coordinates[0]).addTo(map).bindPopup(`<b>Start</b><br>Time: ${startLocalTime}`).openPopup();  // Start
            L.marker(coordinates[coordinates.length - 1]).addTo(map).bindPopup(`<b>End</b><br>Time: ${endLocalTime}`);  // End

            // Draw the polyline (route) on the map
            L.polyline(coordinates, { color: 'blue' }).addTo(map);

            // Adjust map view to fit the plotted route
            map.fitBounds(coordinates);
        }

        // Update the "Last updated at" time after the data fetch is completed
        updateLastUpdatedTime();
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        document.getElementById('error').textContent = 'Error fetching data';
    });
}

// Add event listener for time range selector to reload data
document.getElementById('time-select').addEventListener('change', function() {
    const userSelect = document.getElementById('user-select');
    if (userSelect.value !== '') {
        fetchGPSData(userSelect.value);  // Fetch data for the selected user when the time range changes
        updateLastUpdatedTime();  // Update the "Last updated at" time when time range changes
    }
});

// Add auto-refresh functionality every 30 seconds
setInterval(() => {
    const userSelect = document.getElementById('user-select');
    if (userSelect.value !== '') {
        fetchGPSData(userSelect.value);  // Refresh data every 30 seconds
        updateLastUpdatedTime();  // Update the "Last updated at" time on auto-refresh
    }
}, 30000); // 30 seconds
