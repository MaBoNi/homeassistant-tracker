# GPS Tracker Application

This project is a GPS tracking application that displays GPS data for specific users and their devices. It provides an interface to select a user, view their device's location data, and visualize the route the device has taken on a map.

## Features

- **User Selection**: Select a user from the dropdown to view their GPS data.
- **Table View**: Display GPS data such as latitude, longitude, timestamp, device, and accuracy in a table.
- **Map View**: Visualize the route the device has taken on a map. The map shows the connected points of GPS coordinates, marking the start and end of the route.
- **Data Fetching**: Fetches GPS data for a selected user from the API for the last 7 days and populates the table and map dynamically.

## Technologies Used

- **HTML, CSS, JavaScript**: Frontend components
- **Leaflet.js**: For rendering and displaying the map and plotting routes.
- **OpenStreetMap**: Free tile map service used by Leaflet for displaying the map.
- **Flask API**: Backend API for fetching user and GPS data.

## Installation and Setup

1. **Backend**: Set up the Flask API to serve the GPS data.
   - Refer to the backend API documentation to configure the routes for fetching users and GPS data.
   
2. **Frontend**:
   - The frontend is built using simple HTML, CSS, and JavaScript.
   - The map is rendered using **Leaflet.js** and displays the GPS coordinates on a polyline (connected route).

3. **Running the Frontend**:
   - Build the frontend Docker container:
     ```bash
     docker build -t gps-tracker-frontend .
     ```
   - Run the frontend:
     ```bash
     docker run -d -p 5172:80 gps-tracker-frontend
     ```

4. **Access the App**:
   - Open a browser and navigate to `http://localhost:5172/`.
   - Select a user from the dropdown to view their GPS data and route.

## New Map Feature

- **Map Integration**: The new map feature allows you to see the route the selected user has taken over the last 7 days.
  - The map is plotted using **Leaflet.js** with data points taken from the GPS coordinates retrieved from the backend.
  - The start and end of the route are marked with markers, and the entire route is connected with a blue polyline.
  - The map will automatically adjust its view to fit the entire route on the screen.
  
- **Usage**:
  - Simply select a user from the dropdown, and their route will be plotted on the map below the table.

