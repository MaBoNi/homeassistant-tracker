![Build Status](https://img.shields.io/github/actions/workflow/status/maboni/homeassistant-tracker/docker-publish.yml?branch=main&style=for-the-badge)
![License](https://img.shields.io/github/license/maboni/homeassistant-tracker?style=for-the-badge)
![Repo Size](https://img.shields.io/github/repo-size/maboni/homeassistant-tracker?style=for-the-badge)

[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-homeassistant--tracker--frontend-blue?logo=docker&style=for-the-badge)](https://hub.docker.com/r/maboni82/homeassistant-tracker-frontend)[![Docker Pulls](https://img.shields.io/docker/pulls/maboni82/homeassistant-tracker-frontend?style=for-the-badge)](https://hub.docker.com/r/maboni82/homeassistant-tracker-frontend)


[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-homeassistant--tracker--backend-blue?logo=docker&style=for-the-badge)](https://hub.docker.com/r/maboni82/homeassistant-tracker-backend)[![Docker Pulls](https://img.shields.io/docker/pulls/maboni82/homeassistant-tracker-backend?style=for-the-badge)](https://hub.docker.com/r/maboni82/homeassistant-tracker-backend)


A Dockerized GPS tracker application that fetches GPS data from Home Assistant and visualizes it. The backend fetches GPS data from Home Assistant API, while the frontend displays the data on a map.

## Features
- **GPS Tracking** – Retrieve GPS coordinates from Home Assistant for selected users and devices.
- **Map Visualization** – Display routes on a map using Leaflet for interactive visualization.
- **User Data Filtering** – Select users from a dropdown menu to view their GPS data.
- **Dockerized** – Quick deployment of backend and frontend via Docker.

## Getting Started

### Prerequisites
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/maboni/ha-gps-tracker.git
    cd ha-gps-tracker
    ```

2. **Set up Docker environment**:
    Create a `.env` file and configure the Home Assistant API details:
    ```
    HA_API_URL=https://your-home-assistant-url/api
    HA_TOKEN=your_long_lived_token
    ```

3. **Run the containers**:
    ```bash
    docker-compose up -d
    ```

4. The **frontend** will be available at `http://localhost:5172` and the **backend API** at `http://localhost:5171`.

### Usage
When you visit the frontend, you can select a user from the dropdown, and the GPS route will be displayed on the map. The data is updated every few seconds from Home Assistant.

### Example Data in the Table

| User         | Device             | Latitude      | Longitude     | Timestamp            | Accuracy |
|--------------|--------------------|---------------|---------------|----------------------|----------|
| martin_bonde | ipad_pro_bondes     | 55.563566     | 9.479099      | 19/10/2024, 21:35:52| 6        |
| martin_bonde | bonds_iphone_13_pro | 55.563547     | 9.479100      | 19/10/2024, 21:35:52| 9        |

### Map Visualization

The map under the table will plot the route based on the GPS coordinates from the table, providing a visual representation of the journey. The route is updated dynamically as new data is received.

## Docker Hub Repositories

- **Backend**: <a href="https://hub.docker.com/r/maboni82/homeassistant-tracker-backend" target="_blank">homeassistant-tracker-backend</a>
- **Frontend**: <a href="https://hub.docker.com/r/maboni82/homeassistant-tracker-frontend" target="_blank">homeassistant-tracker-frontend</a>

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Built for efficient tracking and visualization of GPS data using Home Assistant and open-source tools.

## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

## Repobeats Analytics
---

![Alt](https://repobeats.axiom.co/api/embed/bdefb2b5821082ae5d7ef63926053e0edc2ec335.svg "Repobeats analytics image")

---