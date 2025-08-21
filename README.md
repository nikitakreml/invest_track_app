# InvestTrack App

A Telegram-style web application for tracking purchases/sales of user assets (stocks, crypto, etc.) with Google Sheets integration.

## Project Structure

```
/project-root
  /backend
    main.py
    models.py
    database.py
    crud.py
    schemas.py
    google_sheets.py
  /frontend
    /src
      /components
        Dashboard.vue
        Transactions.vue
        Settings.vue
      /views
        HomeView.vue
      App.vue
      main.js
      /router
        index.js
  requirements.txt
  package.json
  README.md
```

## Setup and Run Instructions

### Backend Setup

1.  **Navigate to the project root directory (where `backend` and `frontend` folders are located):**
    ```bash
    cd /Users/nikitakreml/Documents/invest_track_app
    ```
2.  **Create a Python virtual environment (recommended) in the `backend` directory:**
    ```bash
    python3 -m venv backend/venv
    ```
3.  **Activate the virtual environment:**
    *   On macOS/Linux:
        ```bash
        source backend/venv/bin/activate
        ```
    *   On Windows:
        ```bash
        .\backend\venv\Scripts\activate
        ```
4.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Run the FastAPI application from the project root:**
    ```bash
    uvicorn backend.main:app --reload
    ```
    The backend will be running on `http://127.0.0.1:8000`.

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```
2.  **Install the Node.js dependencies:**
    ```bash
    npm install
    ```
3.  **Run the Vue.js development server:**
    ```bash
    npm run dev
    ```
    The frontend will be running on `http://localhost:5173` (or another port as indicated by Vite).

## Google Sheets Integration (Stubbed)

- The Google Sheets integration is currently stubbed out in `backend/google_sheets.py`.
- You can interact with the dummy Google Sheets functions via the `/settings` page in the frontend.
