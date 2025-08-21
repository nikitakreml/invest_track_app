<template>
  <div>
    <h1>Dashboard / Summary</h1>
    <p>Selected Period: {{ period }}</p>
    <button @click="setPeriod('day')">Day</button>
    <button @click="setPeriod('month')">Month</button>
    <button @click="setPeriod('year')">Year</button>
    <button @click="setPeriod('all_time')">All Time</button>

    <div v-if="summary.message && (summary.current_total === 0 && summary.rate_of_return === 0)">
      <p>{{ summary.message }}</p>
    </div>
    <div v-else>
      <p>Current Total: {{ summary.current_total }}</p>
      <p>Rate of Return: {{ summary.rate_of_return }}%</p>
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
