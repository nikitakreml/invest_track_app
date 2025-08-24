<template>
  <div class="dashboard-container">
    <h1>Dashboard / Summary</h1>
    <p>Selected Period: {{ period }}</p>
    <div class="button-group">
      <button @click="setPeriod('day')" :class="{ active: period === 'day' }">Day</button>
      <button @click="setPeriod('month')" :class="{ active: period === 'month' }">Month</button>
      <button @click="setPeriod('year')" :class="{ active: period === 'year' }">Year</button>
      <button @click="setPeriod('all_time')" :class="{ active: period === 'all_time' }">All Time</button>
    </div>

    <div class="summary-card" v-if="summary.message && (summary.current_total === 0 && summary.rate_of_return === 0)">
      <p>{{ summary.message }}</p>
    </div>
    <div class="summary-card" v-else>
      <p>Current Total: <span class="summary-value">{{ summary.current_total }}</span></p>
      <p>Rate of Return: <span :class="{'summary-value': true, 'positive': summary.rate_of_return > 0, 'negative': summary.rate_of_return < 0}">{{ summary.rate_of_return }}%</span></p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  name: 'Dashboard',
  setup() {
    const period = ref('all_time');
    const summary = ref({
      current_total: 0,
      rate_of_return: 0,
      message: 'Loading...'
    });

    const fetchSummary = async (p) => {
      try {
        const response = await fetch(`http://localhost:8000/portfolio/summary?period=${p}`);
        const data = await response.json();
        summary.value.current_total = data.current_total;
        summary.value.rate_of_return = data.rate_of_return;
        summary.value.message = data.message || null; // Set message if present, else null
      } catch (error) {
        console.error("Error fetching summary:", error);
        summary.value.current_total = 'Error';
        summary.value.rate_of_return = 'Error';
        summary.value.message = 'Error fetching summary.';
      }
    };

    const setPeriod = (p) => {
      period.value = p;
      fetchSummary(p);
    };

    onMounted(() => {
      fetchSummary(period.value);
    });

    return {
      period,
      summary,
      setPeriod
    };
  }
}
</script>

<style scoped>
.dashboard-container {
  padding: 40px; /* Increased padding */
  background-color: var(--primary-background);
  color: var(--text-color-light); /* Text now light on dark background */
  min-height: calc(100vh - 100px); /* Adjust based on fixed nav height */
}

h1 {
  color: var(--text-color-dark); /* Main heading is white */
  margin-bottom: 25px; /* Increased margin */
  font-size: 2.8rem; /* Larger heading */
  font-weight: 800; /* Bolder heading */
  letter-spacing: -0.03em;
}

p {
  color: var(--text-color-light); /* Paragraph text is light grey-blue */
  font-size: 1.1rem;
  margin-bottom: 15px;
}

.button-group {
  margin-bottom: 30px; /* Increased margin */
  display: flex;
  justify-content: center;
  gap: 10px; /* Spacing between buttons */
}

.button-group button {
  background-color: var(--secondary-background); /* Buttons background is secondary dark */
  color: var(--text-color-light);
  border: 1px solid var(--color-dark-grey-blue); /* Subtle border */
  padding: 10px 20px;
  margin: 0;
  border-radius: 8px; /* Slightly more rounded */
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  text-transform: capitalize; /* Capitalize only first letter */
  box-shadow: 0 2px 5px rgba(var(--color-darkest-rgb), 0.2);
}

.button-group button:hover {
  background-color: var(--color-vibrant-blue); /* Vibrant blue on hover */
  color: var(--text-color-dark); /* White text on hover */
  transform: translateY(-3px) scale(1.02); /* More pronounced hover */
  box-shadow: 0 5px 15px rgba(var(--accent-color-rgb), 0.3);
}

.button-group button.active {
  background-color: var(--accent-color); /* Active button is vibrant blue */
  color: var(--text-color-dark);
  border-color: var(--accent-color);
  box-shadow: 0 3px 10px rgba(var(--accent-color-rgb), 0.4);
}

.summary-card {
  background-color: var(--secondary-background); /* Card background is secondary dark */
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 6px 20px rgba(var(--color-darkest-rgb), 0.4);
  text-align: left;
  margin: 40px auto;
  max-width: 700px; /* Constrain width */
  opacity: 0;
  transform: translateY(30px);
  animation: fadeInSlideUp 0.6s ease-out forwards;
  border: 1px solid rgba(var(--color-light-grey-blue-rgb), 0.1); /* Subtle border */
}

.summary-card p {
  font-size: 1.2rem;
  margin-bottom: 12px;
  color: var(--text-color-light); /* Light grey-blue for card text */
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.summary-value {
  font-weight: bold;
  color: var(--text-color-dark); /* White for values */
  font-size: 1.3rem;
}

.positive {
  color: #5cb85c; /* Green for positive, ensure good contrast */
}

.negative {
  color: var(--danger-color); /* Red for negative */
}

@keyframes fadeInSlideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
