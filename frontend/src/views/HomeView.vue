<template>
  <div class="home">
    <h1>Welcome to InvestTrack!</h1>
    <p>Your personal asset tracking application.</p>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
}
</script>

<style scoped>
.home {
  padding: 60px 20px; /* Adjusted padding for responsiveness */
  background-color: var(--primary-background);
  color: var(--text-color-light);
  min-height: calc(100vh - var(--nav-height, 100px)); /* Use CSS variable for nav height */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  animation: fadeIn 0.8s ease-out forwards;
}

h1 {
  color: var(--text-color-dark);
  margin-bottom: 15px;
  /* Rely on global clamp() for font-size */
  font-weight: 900;
  letter-spacing: -0.04em;
  line-height: 1.1;
}

p {
  color: var(--text-color-light);
  /* Rely on global clamp() for font-size */
  max-width: 90%; /* Adjust max-width for better mobile readability */
  margin-bottom: 30px;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 480px) {
  .home {
    padding: 40px 15px; /* Further reduced padding for very small screens */
  }
}
</style>
