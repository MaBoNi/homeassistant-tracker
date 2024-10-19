# GPS Tracker Backend with Home Assistant Integration

This project is a GPS tracking backend built with Python, Flask, and PostgreSQL. It integrates with Home Assistant to track the GPS location of users and logs the data into a PostgreSQL database.

## Features
- Fetches GPS coordinates from Home Assistant for specific users
- Saves the location data in PostgreSQL
- Provides an API to query logged GPS data
- A web frontend for displaying the GPS data visually (to be developed)

## Requirements
- Docker
- Docker Compose
- Home Assistant (API access with long-lived token)

## Setup

1. Clone the repository:

```bash
git clone <your-repo-url>
cd <your-repo-directory>
