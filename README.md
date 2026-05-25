# Smart Food Distribution 🌍🍽️

Smart Food Distribution is a comprehensive web platform designed to bridge the gap between food waste and hunger. It connects businesses (restaurants, hotels, caterers) that have surplus food with non-profit organizations (NGOs, shelters) capable of distributing it to those in need.

## 🚀 Features

* **Premium UI/UX:** A stunning, state-of-the-art dark theme featuring glassmorphism, glowing accents, and smooth staggered entrance animations.
* **Real-Time WebSockets:** Powered by Django Channels, NGOs receive instant, live Toast notifications the second a restaurant submits new surplus food—no page refresh required!
* **Volunteer Logistics:** NGOs can register a fleet of volunteers (bikes, cars, vans) and actively assign drivers to pick up accepted food donations from a dedicated Logistics dashboard.
* **Role-Based Access:** Dedicated dashboards for Restaurants (Donors), NGOs (Receivers), and Admins (Platform Overseers).
* **Live Surplus Tracking:** NGOs can instantly view and accept available surplus food in their area.
* **Visual Analytics:** Fully integrated Chart.js doughnut charts and interactive Leaflet dark-mode maps to track food distribution geographically and by event type.
* **Zero-Scroll Dashboards:** Highly optimized, compact layouts for maximum efficiency.

## 🛠️ Technology Stack

* **Backend:** Python, Django, Django Channels (WebSockets)
* **Frontend:** HTML5, Vanilla CSS, Bootstrap 5, JavaScript
* **Data Visualization:** Chart.js, Leaflet.js
* **Containerization:** Docker

## 🐳 How to Run with Docker (Recommended)

This project is fully containerized with Docker for easy setup. 

1. **Build the Docker Image:**
   ```bash
   docker build -t smart-food-app .
   ```

2. **Run the Container (with Data Persistence):**
   *Important: We use a volume mount (`-v`) to ensure that your SQLite database is saved permanently to your local machine. If you don't use this, your accounts and food data will be wiped when the container restarts.*
   
   **For Windows (PowerShell):**
   ```powershell
   docker run -p 8000:8000 -v ${PWD}:/app smart-food-app
   ```
   
   **For Mac/Linux (Bash):**
   ```bash
   docker run -p 8000:8000 -v $(pwd):/app smart-food-app
   ```

3. **Access the Application:**
   Open your web browser and navigate to: [http://localhost:8000](http://localhost:8000)

## 💻 How to Run Locally (Without Docker)

If you prefer to run the project natively without Docker:

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Apply Migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```
   Access the site at `http://localhost:8000`.
