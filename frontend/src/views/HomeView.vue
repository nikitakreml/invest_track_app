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
  padding: 80px 20px; /* Increased padding for more vertical space */
  background-color: var(--primary-background);
  color: var(--text-color-light); /* Default text color light */
  min-height: calc(100vh - 100px); /* Adjust based on fixed nav height */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center; /* Ensure text is centered */
  animation: fadeIn 0.8s ease-out forwards;
}

h1 {
  color: var(--text-color-dark); /* Main heading white */
  margin-bottom: 15px;
  font-size: 3.5rem; /* Larger heading */
  font-weight: 900; /* Extra bold */
  letter-spacing: -0.04em;
  line-height: 1.1;
}

p {
  color: var(--text-color-light); /* Paragraph text light grey-blue */
  font-size: 1.3rem;
  max-width: 600px;
  margin-bottom: 30px;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
