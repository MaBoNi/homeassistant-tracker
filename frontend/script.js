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

// ⚠️ SECURITY NOTE: The token and API URL are replaced by the Docker entrypoint script
// This means the authentication token is visible in the browser (view source, dev tools)
// Anyone with frontend access effectively has API access. This is a known limitation.
// See SECURITY.md for mitigation strategies and recommended solutions.
// Current mitigations: Rate limiting (30 req/min), CORS restrictions, access logging
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
            fetchDevicesForUser(userSelect.value);
            fetchGPSData(userSelect.value);  // Fetch data for the selected user
            updateLastUpdatedTime();  // Update the "Last updated at" time when user changes
        }
    });
}

// Populate the device dropdown for the current user (issue #20). Always
// includes an "All devices" option that maps to no device filter.
function fetchDevicesForUser(selectedUser) {
    const deviceSelect = document.getElementById('device-select');
    if (!deviceSelect) return;
    const url = `${backendApiUrl}/api/users/${encodeURIComponent(selectedUser)}/devices`;

    fetch(url, { headers: { 'Authorization': `Bearer ${token}` } })
        .then(response => response.json())
        .then(devices => {
            // Reset to just the "All devices" sentinel before re-populating.
            deviceSelect.innerHTML = '<option value="">All devices</option>';
            if (!devices || devices.length === 0) return;
            devices.forEach(device => {
                const option = document.createElement('option');
                option.value = device;
                option.textContent = device;
                deviceSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error fetching devices:', error);
        });
}

// Re-fetch GPS data whenever the device selection changes.
document.addEventListener('DOMContentLoaded', function() {
    const deviceSelect = document.getElementById('device-select');
    if (deviceSelect) {
        deviceSelect.addEventListener('change', function() {
            const userSelect = document.getElementById('user-select');
            if (userSelect.value !== '') {
                fetchGPSData(userSelect.value);
                updateLastUpdatedTime();
            }
        });
    }
});

// Fetch GPS data for the selected user and time range, and plot it on the map
function fetchGPSData(selectedUser) {
    const timeSelect = document.getElementById('time-select');
    const timeRange = timeSelect.value;

    // Build the URL with URLSearchParams so we can layer in optional filters
    // (device — #102, custom date range — #16) without manual string concat.
    const params = new URLSearchParams({ user: selectedUser });
    if (timeRange === 'custom') {
        // Custom date range support (issue #16). When the user picks "custom",
        // we forward start_date/end_date (YYYY-MM-DD) to the backend instead
        // of a relative bucket. Backend accepts ISO dates and returns 200/[]
        // when the range is empty.
        const startDate = document.getElementById('start-date').value;
        const endDate = document.getElementById('end-date').value;
        if (!startDate && !endDate) {
            // Nothing chosen yet — default to today.
            const today = new Date().toISOString().slice(0, 10);
            params.set('start_date', today);
        } else {
            if (startDate) params.set('start_date', startDate);
            if (endDate) params.set('end_date', endDate);
        }
    } else {
        params.set('time_range', timeRange);
    }

    // Optional device filter (issue #20).
    const deviceSelect = document.getElementById('device-select');
    const selectedDevice = deviceSelect ? deviceSelect.value : '';
    if (selectedDevice) params.set('device', selectedDevice);

    const fullUrl = `${backendApiUrl}/api/gps-data?${params.toString()}`;

    fetch(fullUrl, {
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
            const deviceSel = document.getElementById('device-select');
            errorElement.textContent = (deviceSel && deviceSel.value)
                ? `No GPS logs for device "${deviceSel.value}" in this range.`
                : 'No data found!';

            errorElement.textContent = 'No GPS logs for the selected date range.';
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

            // Issue #18: stash the route so the animation controls can replay it.
            window.__routeCoordinates = coordinates.slice();
            resetPlayback();
        } else {
            window.__routeCoordinates = [];
            resetPlayback();
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
    // Reveal the date-range pickers when the user chooses "custom".
    const dateRange = document.getElementById('date-range');
    if (this.value === 'custom') {
        dateRange.hidden = false;
    } else {
        dateRange.hidden = true;
    }

    const userSelect = document.getElementById('user-select');
    if (userSelect.value !== '' && this.value !== 'custom') {
        fetchGPSData(userSelect.value);  // Fetch data for the selected user when the time range changes
        updateLastUpdatedTime();  // Update the "Last updated at" time when time range changes
    }
});

// "Apply" button for custom date range (issue #16). Defer the fetch until the
// user explicitly confirms so we don't spam the backend on every date keystroke.
const applyDateRangeBtn = document.getElementById('apply-date-range');
if (applyDateRangeBtn) {
    applyDateRangeBtn.addEventListener('click', function() {
        const userSelect = document.getElementById('user-select');
        if (userSelect.value !== '') {
            fetchGPSData(userSelect.value);
            updateLastUpdatedTime();
        }
    });
}

// Add auto-refresh functionality every 30 seconds
setInterval(() => {
    const userSelect = document.getElementById('user-select');
    if (userSelect.value !== '') {
        fetchGPSData(userSelect.value);  // Refresh data every 30 seconds
        updateLastUpdatedTime();  // Update the "Last updated at" time on auto-refresh
    }
}, 30000); // 30 seconds

// ----------------------------------------------------------------------------
// Animated route playback (issue #18)
//
// Vanilla Leaflet + setInterval. We interpolate between consecutive points so
// a 1× pass takes roughly the real elapsed time, capped to a sane minimum
// per-segment dwell so single-shot replays of long routes don't take hours.
// The car icon is an inline data-URI SVG — no asset file needed.
// ----------------------------------------------------------------------------

const CAR_SVG = `<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32' width='32' height='32'>
  <rect x='4' y='10' width='24' height='10' rx='2' fill='#d62828' stroke='#000' stroke-width='1'/>
  <rect x='8' y='6' width='16' height='6' rx='1' fill='#f1faee' stroke='#000' stroke-width='1'/>
  <circle cx='10' cy='22' r='3' fill='#1d1d1d'/>
  <circle cx='22' cy='22' r='3' fill='#1d1d1d'/>
  <circle cx='10' cy='22' r='1.2' fill='#888'/>
  <circle cx='22' cy='22' r='1.2' fill='#888'/>
</svg>`;
const CAR_ICON = L.icon({
    iconUrl: 'data:image/svg+xml;base64,' + btoa(CAR_SVG),
    iconSize: [32, 32],
    iconAnchor: [16, 16],
});

const playback = {
    marker: null,
    timer: null,
    index: 0,           // index of the current segment start
    subStep: 0,         // 0..STEPS_PER_SEGMENT-1 progress along current segment
    speedMultiplier: 2,
    paused: true,
};

const STEPS_PER_SEGMENT = 20;   // smoother = higher; cheaper = lower
const BASE_TICK_MS = 60;        // tick interval at 1× speed

function tickInterval() {
    // Higher speed → shorter tick interval (clamped so we don't kill the browser).
    return Math.max(8, Math.round(BASE_TICK_MS / playback.speedMultiplier));
}

function resetPlayback() {
    if (playback.timer) {
        clearInterval(playback.timer);
        playback.timer = null;
    }
    if (playback.marker) {
        map.removeLayer(playback.marker);
        playback.marker = null;
    }
    playback.index = 0;
    playback.subStep = 0;
    playback.paused = true;

    const playBtn = document.getElementById('play-btn');
    const pauseBtn = document.getElementById('pause-btn');
    const hasRoute = (window.__routeCoordinates || []).length >= 2;
    if (playBtn) {
        playBtn.disabled = !hasRoute;
        playBtn.textContent = '▶ Play';
    }
    if (pauseBtn) pauseBtn.disabled = true;
}

function interp(a, b, t) {
    return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t];
}

function playbackTick() {
    const route = window.__routeCoordinates || [];
    if (route.length < 2) return;

    const a = route[playback.index];
    const b = route[playback.index + 1];
    const t = playback.subStep / STEPS_PER_SEGMENT;
    const [lat, lng] = interp(a, b, t);

    if (!playback.marker) {
        playback.marker = L.marker([lat, lng], { icon: CAR_ICON, zIndexOffset: 1000 }).addTo(map);
    } else {
        playback.marker.setLatLng([lat, lng]);
    }

    playback.subStep += 1;
    if (playback.subStep >= STEPS_PER_SEGMENT) {
        playback.subStep = 0;
        playback.index += 1;
        if (playback.index >= route.length - 1) {
            // Snap to final point and stop.
            const last = route[route.length - 1];
            playback.marker.setLatLng(last);
            clearInterval(playback.timer);
            playback.timer = null;
            playback.paused = true;
            const playBtn = document.getElementById('play-btn');
            const pauseBtn = document.getElementById('pause-btn');
            if (playBtn) playBtn.textContent = '▶ Replay';
            if (playBtn) playBtn.disabled = false;
            if (pauseBtn) pauseBtn.disabled = true;
        }
    }
}

function startPlayback() {
    const route = window.__routeCoordinates || [];
    if (route.length < 2) return;

    // If we finished the previous run, rewind.
    if (playback.index >= route.length - 1) {
        playback.index = 0;
        playback.subStep = 0;
        if (playback.marker) { map.removeLayer(playback.marker); playback.marker = null; }
    }

    playback.paused = false;
    if (playback.timer) clearInterval(playback.timer);
    playback.timer = setInterval(playbackTick, tickInterval());

    document.getElementById('play-btn').textContent = '▶ Playing…';
    document.getElementById('play-btn').disabled = true;
    document.getElementById('pause-btn').disabled = false;
}

function pausePlayback() {
    if (playback.timer) {
        clearInterval(playback.timer);
        playback.timer = null;
    }
    playback.paused = true;
    document.getElementById('play-btn').textContent = '▶ Resume';
    document.getElementById('play-btn').disabled = false;
    document.getElementById('pause-btn').disabled = true;
}

document.addEventListener('DOMContentLoaded', function() {
    const playBtn = document.getElementById('play-btn');
    const pauseBtn = document.getElementById('pause-btn');
    const speedSelect = document.getElementById('speed-select');
    if (playBtn) playBtn.addEventListener('click', startPlayback);
    if (pauseBtn) pauseBtn.addEventListener('click', pausePlayback);
    if (speedSelect) {
        speedSelect.addEventListener('change', function() {
            playback.speedMultiplier = parseFloat(this.value) || 1;
            // Reschedule the timer at the new cadence if currently playing.
            if (playback.timer) {
                clearInterval(playback.timer);
                playback.timer = setInterval(playbackTick, tickInterval());
            }
        });
        playback.speedMultiplier = parseFloat(speedSelect.value) || 1;
    }
});