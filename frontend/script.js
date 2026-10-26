// Function to update the "Last updated at" time
function updateLastUpdatedTime() {
    const lastUpdatedElement = document.getElementById('last-updated');
    const currentTime = new Date().toLocaleTimeString([], { hour12: false });  // 24-hour format
    console.log(`Last updated time: ${currentTime}`);  // <-- Log for debugging
    lastUpdatedElement.textContent = `Last updated: ${currentTime}`;
}

document.addEventListener('DOMContentLoaded', function() {
    boot();  // Check the session, then show the login screen or the app

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

// The page and the API share an origin: nginx proxies /api and /auth to the
// backend (issue #115), and the browser authenticates with the HTTP-only
// session cookie from /auth/login. No token or backend address ships here.

// Wrapper around fetch for our API: sends the session cookie, adds the CSRF
// header the backend requires on state-changing requests, and drops back to
// the login screen when the session has expired.
function apiFetch(path, options = {}) {
    const headers = { 'X-Requested-With': 'XMLHttpRequest', ...(options.headers || {}) };
    if (options.body !== undefined && !(options.body instanceof FormData)) {
        headers['Content-Type'] = 'application/json';
    }
    return fetch(path, { ...options, headers, credentials: 'same-origin' }).then(response => {
        if (response.status === 401 && !path.startsWith('/auth/')) {
            showLogin('Your session has expired. Please log in again.');
            throw new Error('Not authenticated');
        }
        return response;
    });
}

// Helper function to convert ISO timestamp to local time, assuming the API is sending UTC timestamps
function convertUTCToLocal(utcDateString) {
    const utcDate = new Date(utcDateString + 'Z');  // Append 'Z' to treat it as UTC
    return utcDate.toLocaleString([], { hour12: false });  // Convert to 24-hour local time
}

// Populate the user dropdown. Admins pick from everyone with GPS data;
// other roles only ever see their own tracked person (issue #115), so the
// selector is locked to that one entry.
function fetchUsers(me) {
    const userSelect = document.getElementById('user-select');

    // Add event listener to fetch data when a valid user is selected
    userSelect.addEventListener('change', function() {
        if (userSelect.value !== '') {
            fetchDevicesForUser(userSelect.value);
            fetchGPSData(userSelect.value);  // Fetch data for the selected user
            updateLastUpdatedTime();  // Update the "Last updated at" time when user changes
        }
    });

    if (me.role !== 'admin') {
        if (!me.tracked_person) {
            document.getElementById('error').textContent =
                'Your account is not linked to a tracked person yet. Ask an admin to set one.';
            userSelect.disabled = true;
            return;
        }
        const option = document.createElement('option');
        option.value = me.tracked_person;
        option.textContent = me.tracked_person;
        userSelect.appendChild(option);
        userSelect.value = me.tracked_person;
        userSelect.disabled = true;
        userSelect.dispatchEvent(new Event('change'));
        return;
    }

    apiFetch('/api/v1/users')
    .then(response => response.json())
    .then(users => {
        if (!Array.isArray(users) || users.length === 0) {
            document.getElementById('error').textContent = 'No users found!';
            return;
        }
        fillTrackedPeople(users);

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
}

// Populate the device dropdown for the current user (issue #20). Always
// includes an "All devices" option that maps to no device filter.
function fetchDevicesForUser(selectedUser) {
    const deviceSelect = document.getElementById('device-select');
    if (!deviceSelect) return;
    apiFetch(`/api/v1/users/${encodeURIComponent(selectedUser)}/devices`)
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

    return apiFetch(`/api/v1/gps-data?${params.toString()}`)
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
            [item.user, item.device, item.latitude, item.longitude, localTimestamp, item.accuracy || 'N/A']
                .forEach(value => {
                    const cell = document.createElement('td');
                    cell.textContent = value;
                    row.appendChild(cell);
                });
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

// ----------------------------------------------------------------------------
// Per-user stats + chart (issue #22)
//
// We render three numeric "tiles" (distance / avg speed / point count) plus a
// 24-bucket bar chart of points-per-hour-of-day. Chart.js is lazy-loaded from
// a CDN on first use so the page-load cost is zero for users who never look
// at stats.
// ----------------------------------------------------------------------------

let chartJsLoadPromise = null;
let statsChartInstance = null;

function loadChartJs() {
    if (window.Chart) return Promise.resolve(window.Chart);
    if (chartJsLoadPromise) return chartJsLoadPromise;
    chartJsLoadPromise = new Promise((resolve, reject) => {
        const s = document.createElement('script');
        s.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js';
        s.onload = () => resolve(window.Chart);
        s.onerror = () => reject(new Error('Failed to load Chart.js'));
        document.head.appendChild(s);
    });
    return chartJsLoadPromise;
}

function fetchUserStats(selectedUser) {
    const panel = document.getElementById('stats-panel');
    if (!panel) return;
    apiFetch(`/api/v1/users/${encodeURIComponent(selectedUser)}/stats`)
        .then(r => r.json())
        .then(stats => {
            panel.hidden = false;
            document.getElementById('stat-distance').textContent =
                `${(stats.total_distance_km || 0).toFixed(2)} km`;
            document.getElementById('stat-speed').textContent =
                `${(stats.avg_speed_kmh || 0).toFixed(1)} km/h`;
            document.getElementById('stat-points').textContent =
                stats.point_count ?? 0;

            // Render the points-per-hour bar chart, lazy-loading Chart.js.
            loadChartJs().then(Chart => {
                const buckets = stats.points_per_hour || {};
                const labels = [];
                const data = [];
                for (let h = 0; h < 24; h++) {
                    labels.push(`${String(h).padStart(2, '0')}:00`);
                    data.push(buckets[h] ?? buckets[String(h)] ?? 0);
                }
                const ctx = document.getElementById('stats-chart').getContext('2d');
                if (statsChartInstance) {
                    statsChartInstance.data.labels = labels;
                    statsChartInstance.data.datasets[0].data = data;
                    statsChartInstance.update();
                    return;
                }
                statsChartInstance = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels,
                        datasets: [{
                            label: 'Points per hour-of-day',
                            data,
                            backgroundColor: 'rgba(0, 91, 150, 0.6)',
                            borderColor: '#005b96',
                            borderWidth: 1,
                        }],
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
                    },
                });
            }).catch(err => console.error(err));
        })
        .catch(err => {
            console.error('Error fetching stats:', err);
        });
}

// Hook stats refresh into the existing user-change flow.
document.addEventListener('DOMContentLoaded', function() {
    const userSelect = document.getElementById('user-select');
    if (userSelect) {
        userSelect.addEventListener('change', function() {
            if (userSelect.value !== '') fetchUserStats(userSelect.value);
        });
    }
});
// ----------------------------------------------------------------------------
// Login, session and role-aware UI (issue #115)
//
// boot() asks /auth/me who is logged in. A 401 shows the login form; anything
// else shows the app, with the user selector, export/delete buttons and the
// admin Users panel shown or hidden by role. The backend enforces the same
// rules (issue #114); hiding controls here is only about not offering actions
// that would be refused.
// ----------------------------------------------------------------------------

let currentUser = null;

function boot() {
    apiFetch('/auth/me')
        .then(response => (response.ok ? response.json() : null))
        .then(me => (me ? showApp(me) : showLogin()))
        .catch(error => {
            console.error('Error checking session:', error);
            showLogin('Could not reach the server.');
        });
}

function showLogin(message = '') {
    currentUser = null;
    document.getElementById('app-view').hidden = true;
    document.getElementById('login-view').hidden = false;
    document.getElementById('login-error').textContent = message;
    document.getElementById('login-username').focus();
}

function showApp(me) {
    currentUser = me;
    document.getElementById('login-view').hidden = true;
    document.getElementById('app-view').hidden = false;
    map.invalidateSize();  // the map was laid out while hidden

    document.getElementById('current-username').textContent = me.username;
    document.getElementById('current-role').textContent = me.role;
    document.getElementById('users-toggle').hidden = me.role !== 'admin';

    fetchUsers(me);
}

document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const submit = document.getElementById('login-submit');
    const errorEl = document.getElementById('login-error');
    submit.disabled = true;
    errorEl.textContent = '';

    apiFetch('/auth/login', {
        method: 'POST',
        body: JSON.stringify({
            username: document.getElementById('login-username').value,
            password: document.getElementById('login-password').value,
        }),
    })
        .then(response => {
            if (response.status === 429) throw new Error('Too many failed attempts. Wait a minute and try again.');
            if (!response.ok) throw new Error('Invalid username or password.');
            // Confirm the browser kept the cookie: a Secure cookie is dropped
            // on plain HTTP, which would otherwise look like a silent failure.
            return apiFetch('/auth/me');
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Logged in, but the browser rejected the session cookie. '
                    + 'Serve the app over HTTPS or set SESSION_COOKIE_SECURE=False for local HTTP.');
            }
            // Reload so the page starts clean for this account.
            window.location.reload();
        })
        .catch(error => {
            errorEl.textContent = error.message;
            document.getElementById('login-password').value = '';
        })
        .finally(() => { submit.disabled = false; });
});

document.getElementById('logout-btn').addEventListener('click', function() {
    apiFetch('/auth/logout', { method: 'POST' }).finally(() => window.location.reload());
});

// Export / delete for the selected person. Readonly accounts can do neither,
// so the buttons stay hidden for them.
function updateDataActions(person) {
    const actions = document.getElementById('data-actions');
    if (!person || !currentUser || currentUser.role === 'readonly') {
        actions.hidden = true;
        return;
    }
    const base = `/api/v1/users/${encodeURIComponent(person)}/export`;
    document.getElementById('export-json').href = `${base}?format=json`;
    document.getElementById('export-csv').href = `${base}?format=csv`;
    actions.hidden = false;
}

document.getElementById('user-select').addEventListener('change', function() {
    updateDataActions(this.value);
});

document.getElementById('delete-data').addEventListener('click', function() {
    const person = document.getElementById('user-select').value;
    if (!person) return;
    if (!window.confirm(`Permanently delete all GPS history for "${person}"? This cannot be undone.`)) return;
    apiFetch(`/api/v1/users/${encodeURIComponent(person)}/data`, { method: 'DELETE' })
        .then(response => response.json().then(body => ({ ok: response.ok, body })))
        .then(({ ok, body }) => {
            if (!ok) throw new Error(body.message || 'Delete failed');
            // Refresh first: an empty result rewrites the message line.
            return fetchGPSData(person).then(() => {
                document.getElementById('error').textContent =
                    `Deleted ${body.deleted_rows} GPS log entries for ${person}.`;
            });
        })
        .catch(error => {
            document.getElementById('error').textContent = error.message;
        });
});

// ----------------------------------------------------------------------------
// Admin Users panel: list accounts, change role / tracked person / active,
// and add new accounts.
// ----------------------------------------------------------------------------

function fillTrackedPeople(people) {
    const list = document.getElementById('tracked-people');
    list.innerHTML = '';
    people.forEach(person => {
        const option = document.createElement('option');
        option.value = person;
        list.appendChild(option);
    });
}

function setUsersMessage(text, isError = false) {
    const el = document.getElementById('users-message');
    el.textContent = text;
    el.classList.toggle('form-error', isError);
}

document.getElementById('users-toggle').addEventListener('click', function() {
    const panel = document.getElementById('users-panel');
    panel.hidden = !panel.hidden;
    if (!panel.hidden) loadUsersTable();
});

function loadUsersTable() {
    apiFetch('/auth/users')
        .then(response => response.json())
        .then(users => {
            const tbody = document.querySelector('#users-table tbody');
            tbody.innerHTML = '';
            users.forEach(user => tbody.appendChild(userRow(user)));
        })
        .catch(error => setUsersMessage(`Could not load users: ${error.message}`, true));
}

function userRow(user) {
    const row = document.createElement('tr');
    const isSelf = currentUser && user.id === currentUser.id;

    const nameCell = document.createElement('td');
    nameCell.textContent = user.username;

    const roleSelect = document.createElement('select');
    ['admin', 'user', 'readonly'].forEach(role => {
        const option = document.createElement('option');
        option.value = role;
        option.textContent = role;
        roleSelect.appendChild(option);
    });
    roleSelect.value = user.role;
    roleSelect.disabled = isSelf;  // admins can't demote themselves
    roleSelect.setAttribute('aria-label', `Role for ${user.username}`);

    const personInput = document.createElement('input');
    personInput.type = 'text';
    personInput.value = user.tracked_person || '';
    personInput.setAttribute('list', 'tracked-people');
    personInput.setAttribute('aria-label', `Tracked person for ${user.username}`);

    const activeInput = document.createElement('input');
    activeInput.type = 'checkbox';
    activeInput.checked = user.is_active;
    activeInput.disabled = isSelf;  // or deactivate themselves
    activeInput.setAttribute('aria-label', `${user.username} active`);

    const lastLogin = document.createElement('td');
    lastLogin.textContent = user.last_login_at ? convertUTCToLocal(user.last_login_at) : 'never';

    const save = document.createElement('button');
    save.type = 'button';
    save.textContent = 'Save';
    save.addEventListener('click', () => {
        const body = { tracked_person: personInput.value.trim() };
        if (!isSelf) {
            body.role = roleSelect.value;
            body.is_active = activeInput.checked;
        }
        apiFetch(`/auth/users/${user.id}`, { method: 'PATCH', body: JSON.stringify(body) })
            .then(response => response.json().then(data => ({ ok: response.ok, data })))
            .then(({ ok, data }) => {
                if (!ok) throw new Error(data.message || 'Update failed');
                setUsersMessage(`Saved ${data.username}.`);
                loadUsersTable();
            })
            .catch(error => setUsersMessage(error.message, true));
    });

    [nameCell, wrapCell(roleSelect), wrapCell(personInput), wrapCell(activeInput), lastLogin, wrapCell(save)]
        .forEach(cell => row.appendChild(cell));
    return row;
}

function wrapCell(element) {
    const cell = document.createElement('td');
    cell.appendChild(element);
    return cell;
}

document.getElementById('invite-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const form = this;
    apiFetch('/auth/register', {
        method: 'POST',
        body: JSON.stringify({
            username: document.getElementById('invite-username').value.trim(),
            password: document.getElementById('invite-password').value,
            role: document.getElementById('invite-role').value,
            tracked_person: document.getElementById('invite-person').value.trim() || null,
        }),
    })
        .then(response => response.json().then(data => ({ ok: response.ok, data })))
        .then(({ ok, data }) => {
            if (!ok) throw new Error(data.message || 'Could not add user');
            setUsersMessage(`Added ${data.username} (${data.role}).`);
            form.reset();
            loadUsersTable();
        })
        .catch(error => setUsersMessage(error.message, true));
});
