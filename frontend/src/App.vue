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
  background-color: var(--primary-background); /* Primary background now dark */
  color: var(--text-color-light); /* Default text color now light */
}

:root {
  --color-darkest: #141619; /* Almost black */
  --color-dark-grey-blue: #2C2E3A; /* Darker grey-blue for secondary elements */
  --color-deep-blue: #050A44; /* Dark blue, can be used for deep accents or specific backgrounds */
  --color-vibrant-blue: #0A21C0; /* Bright blue for interactive elements */
  --color-light-grey-blue: #B3B4BD; /* Lighter grey-blue for subtle text/borders */

  /* RGB versions for rgba() usage */
  --color-darkest-rgb: 20, 22, 25;
  --accent-color-rgb: 10, 33, 192;

  --primary-background: var(--color-darkest); /* Main background */
  --secondary-background: var(--color-dark-grey-blue); /* For cards, panels */
  --text-color-dark: #FFFFFF; /* Main text color on dark background */
  --text-color-light: var(--color-light-grey-blue); /* Secondary text, subtle elements */
  --accent-color: var(--color-vibrant-blue);
  --danger-color: #E53935; /* Brighter red for danger, contrasting with dark */
}

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: var(--text-color-dark); /* Ensure app text is visible */
  min-height: 100vh;
  background-color: var(--primary-background); /* Ensure app background matches body */
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
}

nav a {
  font-weight: bold;
  color: var(--text-color-light); /* Nav links are now light on dark background */
  margin: 0 20px;
  text-decoration: none;
  transition: color 0.3s ease, transform 0.2s ease;
  font-size: 1.1rem;
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
  background-color: var(--accent-color); /* Default buttons are vibrant blue */
  color: var(--text-color-dark); /* White text on vibrant blue */
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
  color: var(--text-color-dark); /* Labels are light on dark background */
  font-size: 0.95rem;
}

input[type="text"],
input[type="date"],
input[type="number"],
select {
  width: calc(100% - 22px);
  padding: 12px;
  border: 1px solid var(--color-dark-grey-blue); /* Darker border for inputs */
  border-radius: 6px;
  font-size: 1rem;
  background-color: var(--color-darkest); /* Inputs are dark */
  color: var(--text-color-dark); /* Light text in dark inputs */
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

</style>
