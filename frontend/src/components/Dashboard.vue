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
  padding: 20px;
  background-color: #F2F2F2;
  color: #174D38;
}

h1 {
  color: #4D1717;
  margin-bottom: 20px;
}

.button-group {
  margin-bottom: 20px;
}

.button-group button {
  background-color: #CBCBCB;
  color: #174D38;
  border: 1px solid #CBCBCB;
  padding: 8px 15px;
  margin: 0 5px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.button-group button:hover {
  background-color: #174D38;
  color: white;
}

.button-group button.active {
  background-color: #174D38;
  color: white;
  border-color: #174D38;
}

.summary-card {
  background-color: #FFFFFF;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: left;
  margin-top: 20px;
}

.summary-card p {
  font-size: 1.1rem;
  margin-bottom: 10px;
  color: #174D38;
}

.summary-value {
  font-weight: bold;
  color: #4D1717;
}

.positive {
  color: #174D38;
}

.negative {
  color: #4D1717;
}
</style>
