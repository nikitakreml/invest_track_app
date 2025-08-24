# InvestTrackApp

A simple investment tracking application.

## Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/InvestTrackApp.git
    cd InvestTrackApp
    ```

2.  **Backend Setup (Python FastAPI)**

    a.  Create and activate a virtual environment:

        ```bash
        python -m venv backend/venv
        source backend/venv/bin/activate
        ```

    b.  Install dependencies:

        ```bash
        pip install -r requirements.txt
        ```

    c.  Run the backend server:

        ```bash
        uvicorn backend.main:app --reload
        ```

        The backend API will be available at `http://127.0.0.1:8000`.

3.  **Frontend Setup (Vue.js)**

    a.  Navigate to the frontend directory and install dependencies:

        ```bash
        cd frontend
        npm install
        ```

    b.  Run the frontend development server:

        ```bash
        npm run dev
        ```

        The frontend application will be available at `http://127.0.0.1:5173` (or another port if 5173 is in use).

## Configuration (via User Interface)

All API keys and settings are now managed directly within the application's settings page.

1.  **Access Settings:** Navigate to the 'Settings' page within the application.
2.  **Input Tokens/IDs:** Enter your Google Sheets API Key, Google Sheets Spreadsheet ID, and Tinkoff Invest API Token into the respective input fields.
3.  **Auto Transaction Price:** Toggle the 'Enable Auto Transaction Price' checkbox to allow the application to automatically fetch asset prices, or to input them manually.
4.  **Save Settings:** Click the 'Save Settings' button to store your configuration.

## Project Structure

*   **backend/**: FastAPI application for API endpoints, database interactions, and integration with external services like Tinkoff Invest and Google Sheets.
*   **frontend/**: Vue.js application for the user interface.


#Project Colors
- **Primary Background**: `#F2F2F2`
- **Secondary Background/Borders**: `#CBCBCB`
- **Accent/Success**: `#174D38`
- **Danger/Error**: `#4D1717`

Font: Montserrat