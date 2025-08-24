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

## UI Design & Animations

### Design Principles

The interface has been updated to a modern, minimalistic dark theme, focusing on clean lines, clear typography, and subtle interactions to enhance user experience while retaining full functionality. The design draws inspiration from modern web applications, emphasizing spacious layouts and a sophisticated aesthetic.

### Color Palette

The UI now utilizes a carefully selected dark theme color palette, defined by the following CSS variables:

*   `--color-darkest`: `#141619` (Primary background, deep shadows, input backgrounds)
*   `--color-dark-grey-blue`: `#2C2E3A` (Secondary backgrounds like navigation and cards, subtle borders)
*   `--color-deep-blue`: `#050A44` (Used for deeper accents or specific section backgrounds, subtle hover states)
*   `--color-vibrant-blue`: `#0A21C0` (Vibrant accent color for interactive elements, primary buttons, active states, and highlights)
*   `--color-light-grey-blue`: `#B3B4BD` (Used for secondary text, subtle borders, and inactive elements)

### Typography

*   **Font Family**: 'Roboto', sans-serif (Applied globally for a modern and readable look, chosen for its versatility and clean appearance on dark backgrounds).
*   **Font Weights**: Utilized for hierarchy and emphasis in headings (e.g., `800`, `900` for main titles) and interactive elements (`500`, `600` for buttons and navigation links).

### Animations

Subtle animations have been integrated across the application to provide a smoother and more engaging user experience:

*   **Button & Link Hovers:** Interactive buttons and navigation links feature smooth `transform` (slight lift) and `brightness`/`color` transitions on hover, providing clear visual feedback.
*   **Modal Transitions:** The transaction modal now includes `fade-in` (opacity) and `scale-up` (transform) effects for a dynamic and engaging entrance.
*   **Card & Section Fade-in:** Key content areas like dashboard summary cards, settings forms, and transaction tables animate with a `fade-in` and `slide-up` effect when they appear, guiding the user's attention.
*   **Floating Action Button (FAB):** The "Add Transaction" FAB features a distinct `transform` (more pronounced lift and a 135-degree rotation) on hover, making it more interactive and visually appealing.
*   **Input Focus:** Form input fields provide visual feedback with smooth `border-color` and `box-shadow` transitions on focus.

## Project Structure

*   **backend/**: FastAPI application for API endpoints, database interactions, and integration with external services like Tinkoff Invest and Google Sheets.
*   **frontend/**: Vue.js application for the user interface.

Font: Montserrat