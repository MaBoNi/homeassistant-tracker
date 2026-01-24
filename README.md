# Home Assistant GPS Tracker

![Build Status](https://img.shields.io/github/actions/workflow/status/maboni/homeassistant-tracker/docker-publish.yml?branch=main&style=for-the-badge)
![License](https://img.shields.io/github/license/maboni/homeassistant-tracker?style=for-the-badge)
![Repo Size](https://img.shields.io/github/repo-size/maboni/homeassistant-tracker?style=for-the-badge)

[![Docker Hub Backend](https://img.shields.io/badge/Docker%20Hub-homeassistant--tracker--backend-blue?logo=docker&style=for-the-badge)](https://hub.docker.com/r/maboni82/homeassistant-tracker-backend)
[![Docker Pulls Backend](https://img.shields.io/docker/pulls/maboni82/homeassistant-tracker-backend?style=for-the-badge)](https://hub.docker.com/r/maboni82/homeassistant-tracker-backend)

[![Docker Hub Frontend](https://img.shields.io/badge/Docker%20Hub-homeassistant--tracker--frontend-blue?logo=docker&style=for-the-badge)](https://hub.docker.com/r/maboni82/homeassistant-tracker-frontend)
[![Docker Pulls Frontend](https://img.shields.io/docker/pulls/maboni82/homeassistant-tracker-frontend?style=for-the-badge)](https://hub.docker.com/r/maboni82/homeassistant-tracker-frontend)

A secure, Dockerized GPS tracker application that fetches location data from Home Assistant and visualizes it on an interactive map. Track multiple users and devices with historical data, time-range filtering, and real-time updates.

## Features

### Tracking & Visualization
- **Multi-User GPS Tracking** – Track multiple Home Assistant users and their devices simultaneously
- **Interactive Map** – Leaflet-based map with route visualization and markers
- **Time Range Filtering** – View GPS history: live, last hour, 2/3/6 hours, day, week, or month
- **Real-Time Updates** – Automatic GPS data fetching every 30 seconds
- **Device Deduplication** – Only stores GPS data when location changes (reduces database bloat)

### Security
- **Bearer Token Authentication** – API authentication with constant-time comparison (prevents timing attacks)
- **Rate Limiting** – 200 requests/day, 50 requests/hour to prevent API abuse
- **CORS Protection** – Restricted to specific origins (configurable)
- **Non-Root Containers** – All Docker containers run as non-root users for enhanced security
- **Supply Chain Attestations** – SBOM and provenance attestations for Docker images

### Infrastructure
- **Fully Dockerized** – Easy deployment with docker-compose
- **PostgreSQL Database** – Persistent storage with health checks
- **Environment-Based Config** – Easy configuration via `.env` file
- **Health Check Endpoints** – Docker health monitoring for automatic restarts

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌────────────────┐
│   Frontend  │────▶│   Backend    │────▶│ Home Assistant │
│  (Nginx)    │     │   (Flask)    │     │      API       │
│  Port 5172  │     │  Port 5171   │     └────────────────┘
└─────────────┘     └──────────────┘              │
                            │                      │
                            ▼                      │
                    ┌──────────────┐              │
                    │  PostgreSQL  │◀─────────────┘
                    │   Database   │   (GPS Data)
                    └──────────────┘
```

## Getting Started

### Prerequisites
- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/)
- Home Assistant instance with API access
- Home Assistant Long-Lived Access Token

### Quick Start

1. **Clone the repository**:
    ```bash
    git clone https://github.com/MaBoNi/homeassistant-tracker.git
    cd homeassistant-tracker
    ```

2. **Create environment configuration**:
    ```bash
    cp .env.template .env
    ```

3. **Edit `.env` file** with your configuration:
    ```env
    # Database Configuration
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=your_secure_password
    POSTGRES_DB=gps_tracker
    DATABASE_URL=postgresql://postgres:your_secure_password@homeassistant-tracker-db:5432/gps_tracker

    # Home Assistant Configuration
    HA_API_URL=https://your-home-assistant-url/api
    HA_TOKEN=your_long_lived_access_token
    HA_USERS=user1,user2,user3  # Comma-separated, without 'person.' prefix

    # Application Configuration
    DROP_DB_ON_START=False  # Set to True to recreate DB on startup (dev only)
    TRACKER_APP_TOKEN=your_very_secret_static_token  # Generate a strong random token

    # Frontend Configuration
    BACKEND_API_URL=http://homeassistant-tracker-backend:5171
    ```

    > **Important**: Replace all placeholder values with your actual credentials. Use strong, random passwords.

4. **Start the application**:
    ```bash
    docker-compose up -d
    ```

5. **Access the application**:
    - Frontend: http://localhost:5172
    - Backend API: http://localhost:5171
    - Health Check: http://localhost:5171/api/health

### Getting Your Home Assistant Token

1. Log into your Home Assistant instance
2. Click on your profile (bottom left)
3. Scroll down to "Long-Lived Access Tokens"
4. Click "Create Token"
5. Give it a name (e.g., "GPS Tracker") and copy the token

### Adding Users to Track

In your `.env` file, set `HA_USERS` to a comma-separated list of person entity names **without** the `person.` prefix:

```env
# If your Home Assistant persons are:
# - person.john_doe
# - person.jane_doe
# Then configure:
HA_USERS=john_doe,jane_doe
```

## Usage

### Frontend Interface

1. **Select User**: Choose from the dropdown menu of tracked users
2. **Select Time Range**: Choose how far back to display GPS history
   - Live (current location only)
   - Last hour, 2 hours, 3 hours, 6 hours
   - Last day, last 7 days, last 30 days
3. **View Map**: Interactive map shows the route with markers
4. **View Table**: Detailed table with timestamp, device, coordinates, and accuracy

### Data Table Example

| User         | Device             | Latitude  | Longitude | Timestamp            | Accuracy |
|--------------|--------------------|-----------|-----------|-----------------------|----------|
| martin_bonde | bonds_iphone_16_pro| 55.563551 | 9.479070  | 24/01/2026, 17:11:23 | 9        |
| martin_bonde | bonds_iphone_13_pro| 55.563595 | 9.479085  | 24/01/2026, 17:11:23 | 6        |

## API Endpoints

All endpoints except `/api/health` and `/api/healthz` require authentication via `Authorization: Bearer <TRACKER_APP_TOKEN>` header.

### Endpoints

- `GET /api/gps-data?user=<username>&time_range=<range>` - Fetch GPS logs for a user
  - **Parameters**:
    - `user`: Username (without 'person.' prefix)
    - `time_range`: `live`, `last_hour`, `last_2_hours`, `last_3_hours`, `last_6_hours`, `last_day`, `last_7_days`, `last_30_days`
  - **Response**: JSON array of GPS logs with coordinates, device, timestamp, accuracy

- `GET /api/users` - Get list of all tracked users
  - **Response**: JSON array of usernames

- `GET /api/healthz` - Simple health check (for Docker)
  - **Response**: `{"status": "healthy"}`

- `GET /api/health` - Detailed health check
  - **Response**: JSON with Flask status, database status, Home Assistant API status

### Example API Request

```bash
curl -H "Authorization: Bearer your_token_here" \
  "http://localhost:5171/api/gps-data?user=john_doe&time_range=last_day"
```

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Yes | - |
| `POSTGRES_USER` | PostgreSQL username | Yes | - |
| `POSTGRES_PASSWORD` | PostgreSQL password | Yes | - |
| `POSTGRES_DB` | PostgreSQL database name | Yes | - |
| `HA_API_URL` | Home Assistant API URL | Yes | - |
| `HA_TOKEN` | Home Assistant long-lived token | Yes | - |
| `HA_USERS` | Comma-separated list of users (without 'person.' prefix) | Yes | - |
| `TRACKER_APP_TOKEN` | API authentication token | Yes | - |
| `BACKEND_API_URL` | Backend URL for frontend | Yes | - |
| `DROP_DB_ON_START` | Recreate database on startup (dev only) | No | `False` |

## Development

### Local Development

```bash
# Backend development
cd backend
pip install -r requirements.txt
python app.py

# Linting
pylint backend --rcfile=.pylintrc
```

### Building Docker Images

```bash
# Build specific service
docker-compose build backend
docker-compose build frontend

# Build all services
docker-compose build
```

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

## Troubleshooting

### Backend container unhealthy

Check logs: `docker-compose logs backend`

Common issues:
- Invalid Home Assistant credentials (check `HA_TOKEN` and `HA_API_URL`)
- Database connection issues (verify `DATABASE_URL`)
- Missing environment variables

### Frontend shows no data

- Verify backend is healthy: `curl http://localhost:5171/api/healthz`
- Check browser console for errors
- Verify authentication token is set in `.env`

### GPS data not updating

- Check Home Assistant person entities exist
- Verify device trackers are associated with person entities
- Check backend logs for API errors: `docker-compose logs -f backend`

### Database connection errors

- Ensure PostgreSQL container is running: `docker-compose ps`
- Verify database credentials in `.env` match those in `DATABASE_URL`
- Check if port 5432 is already in use

## Security Considerations

- **Never commit `.env` file** - Already in `.gitignore`
- **Use strong tokens** - Generate random 32+ character tokens
- **HTTPS in production** - Deploy behind reverse proxy with TLS
- **Regular updates** - Keep dependencies up to date with Dependabot
- **Rate limiting active** - 200 requests/day, 50/hour per IP
- **Monitor logs** - Check for unusual access patterns

For detailed security documentation, see open issues.

## Docker Hub

Pre-built images are available on Docker Hub with supply chain attestations:

- **Backend**: [maboni82/homeassistant-tracker-backend](https://hub.docker.com/r/maboni82/homeassistant-tracker-backend)
- **Frontend**: [maboni82/homeassistant-tracker-frontend](https://hub.docker.com/r/maboni82/homeassistant-tracker-frontend)

Images are automatically built and published on every push to `main` branch with:
- SBOM (Software Bill of Materials)
- Provenance attestations
- Multi-date versioning (latest + date-stamped)

## Technology Stack

- **Backend**: Python 3.14, Flask, SQLAlchemy, APScheduler, Flask-CORS, Flask-Limiter
- **Frontend**: HTML, CSS, JavaScript, Leaflet.js for maps
- **Database**: PostgreSQL 13
- **Container**: Docker, Docker Compose
- **CI/CD**: GitHub Actions, CodeQL security scanning

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure:
- Code passes linting (`pylint backend`)
- Docker containers build successfully
- No security vulnerabilities introduced

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Home Assistant integration for GPS tracking
- Uses Leaflet.js for beautiful map visualizations
- PostgreSQL for reliable data storage
- Docker for easy deployment

## Support

- **Issues**: [GitHub Issues](https://github.com/MaBoNi/homeassistant-tracker/issues)
- **Pull Requests**: [GitHub Pull Requests](https://github.com/MaBoNi/homeassistant-tracker/pulls)

## Repobeats Analytics

![Alt](https://repobeats.axiom.co/api/embed/bdefb2b5821082ae5d7ef63926053e0edc2ec335.svg "Repobeats analytics image")