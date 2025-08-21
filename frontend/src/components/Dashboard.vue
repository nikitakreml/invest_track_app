<template>
  <div>
    <h1>Dashboard / Summary</h1>
    <p>Portfolio performance will be displayed here.</p>
    <p>Selected Period: {{ period }}</p>
    <button @click="setPeriod('day')">Day</button>
    <button @click="setPeriod('month')">Month</button>
    <button @click="setPeriod('year')">Year</button>
    <button @click="setPeriod('all_time')">All Time</button>
    <p>Returns: {{ returns }}</p>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  name: 'Dashboard',
  setup() {
    const period = ref('all_time');
    const returns = ref('N/A');

    const fetchSummary = async (p) => {
      try {
        const response = await fetch(`http://localhost:8000/portfolio/summary?period=${p}`);
        const data = await response.json();
        returns.value = data.returns;
      } catch (error) {
        console.error("Error fetching summary:", error);
        returns.value = "Error";
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
      returns,
      setPeriod
    };
  }
}
</script>
