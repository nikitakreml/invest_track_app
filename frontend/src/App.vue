<template>
  <div id="app">
    <nav>
      <router-link to="/">Dashboard</router-link>
      <router-link to="/transactions">Transactions</router-link>
      <router-link to="/settings">Settings</router-link>
    </nav>
    <div class="router-view-content">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style>
/* Global Reset/Base Styles */
body {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Roboto', sans-serif;
  line-height: 1.6;
  background-color: var(--primary-background);
  color: var(--text-color-light);
  -webkit-text-size-adjust: 100%; /* Prevent text zoom on iOS */
}

:root {
  --color-darkest: #141619;
  --color-dark-grey-blue: #2C2E3A;
  --color-deep-blue: #050A44;
  --color-vibrant-blue: #0A21C0;
  --color-light-grey-blue: #B3B4BD;

  /* RGB versions for rgba() usage */
  --color-darkest-rgb: 20, 22, 25;
  --accent-color-rgb: 10, 33, 192;

  --primary-background: var(--color-darkest);
  --secondary-background: var(--color-dark-grey-blue);
  --text-color-dark: #FFFFFF;
  --text-color-light: var(--color-light-grey-blue);
  --accent-color: var(--color-vibrant-blue);
  --danger-color: #E53935;
}

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: var(--text-color-dark);
  min-height: 100vh;
  background-color: var(--primary-background);
}

nav {
  padding: 15px 30px;
  background-color: var(--color-dark-grey-blue);
  box-shadow: 0 2px 10px rgba(var(--color-darkest-rgb), 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
  flex-wrap: wrap; /* Allow nav items to wrap on smaller screens */
}

nav a {
  font-weight: bold;
  color: var(--text-color-light);
  margin: 0 20px;
  text-decoration: none;
  transition: color 0.3s ease, transform 0.2s ease;
  font-size: 1.1rem;
  padding: 5px 0; /* Add padding for easier touch on mobile */
}

nav a.router-link-exact-active {
  color: var(--accent-color);
  transform: translateY(-2px);
}

nav a:hover {
  color: var(--color-vibrant-blue);
  transform: translateY(-2px);
}

/* General button styling */
button {
  transition: all 0.3s ease;
  border-radius: 6px;
  padding: 10px 18px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border: none;
  background-color: var(--accent-color);
  color: var(--text-color-dark);
}

button:hover {
  filter: brightness(1.1);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(var(--color-darkest-rgb), 0.4);
}

/* Modal specific transitions */
.modal-overlay {
  transition: opacity 0.3s ease;
}

.modal-content {
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.27, 1.55);
}

/* Basic form group styling */
.form-group {
  margin-bottom: 15px;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: var(--text-color-dark);
  font-size: 0.95rem;
}

input[type="text"],
input[type="date"],
input[type="number"],
select {
  width: calc(100% - 22px);
  padding: 12px;
  border: 1px solid var(--color-dark-grey-blue);
  border-radius: 6px;
  font-size: 1rem;
  background-color: var(--color-darkest);
  color: var(--text-color-dark);
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

input:focus, select:focus {
  border-color: var(--accent-color);
  box-shadow: 0 0 0 3px rgba(var(--accent-color-rgb), 0.4);
  outline: none;
}

/* Content wrapper for views */
.router-view-content {
  padding-top: 100px; /* Offset for fixed navigation bar */
}

/* Responsive adjustments */
@media (max-width: 768px) {
  nav {
    flex-direction: column; /* Stack nav items vertically */
    padding: 10px 15px; /* Adjust padding for smaller screens */
  }

  nav a {
    margin: 5px 0; /* Adjust vertical margin for stacked links */
    font-size: 1rem;
  }

  .router-view-content {
    padding-top: 130px; /* Adjust padding for stacked nav */
  }

  h1 {
    font-size: clamp(2rem, 5vw, 2.8rem); /* Fluid font size for h1 */
  }

  p {
    font-size: clamp(0.9rem, 2.5vw, 1.1rem); /* Fluid font size for paragraphs */
  }
}

@media (max-width: 480px) {
  .router-view-content {
    padding-top: 150px; /* Further adjust for very small screens */
  }

  nav {
    padding: 10px 10px; /* Smaller padding for very small screens */
  }

  nav a {
    font-size: 0.9rem;
  }
}
</style>
