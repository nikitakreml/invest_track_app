<template>
  <div class="dashboard-container">
    <h1>Dashboard / Summary</h1>
    
    <div class="balance-card summary-card">
      <p>Cash Balance: <span class="summary-value">{{ formattedBalance }}</span></p>
      <div class="balance-actions">
        <input type="number" v-model.number="amount" placeholder="Amount" class="amount-input" />
        <button @click="topUp" class="top-up-button">Top Up</button>
        <button @click="withdraw" class="withdraw-button">Withdraw</button>
      </div>
      <p v-if="balanceMessage" :class="{'message-success': isSuccess, 'message-error': !isSuccess}">{{ balanceMessage }}</p>
    </div>

    <div class="portfolio-chart-card summary-card">
      <h2>Portfolio Composition</h2>
      <pie-chart :data="portfolioCompositionData" :colors="chartColors" :donut="true" :legend="'right'" :suffix="'$'"></pie-chart>
      <p class="total-portfolio-value">Total Portfolio Value: <span class="summary-value">{{ formattedTotalPortfolioValue }}</span></p>
      <p v-if="portfolioMessage" class="message-info">{{ portfolioMessage }}</p>
    </div>

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
import { ref, onMounted, computed } from 'vue';

export default {
  name: 'Dashboard',
  setup() {
    const period = ref('all_time');
    const summary = ref({
      current_total: 0,
      rate_of_return: 0,
      message: 'Loading...'
    });
    const currentBalance = ref(0);
    const amount = ref(0);
    const balanceMessage = ref('');
    const isSuccess = ref(true);

    const portfolioCompositionData = ref([]);
    const totalPortfolioValue = ref(0);
    const portfolioMessage = ref('');

    const chartColors = ["#0A21C0", "#2C2E3A", "#050A44", "#B3B4BD", "#141619"]; // Custom chart colors

    const formattedBalance = computed(() => `$${currentBalance.value.toFixed(2)}`);
    const formattedTotalPortfolioValue = computed(() => `$${totalPortfolioValue.value.toFixed(2)}`);

    const fetchUserData = async () => {
      try {
        const response = await fetch('http://localhost:8000/users/me/settings');
        if (response.ok) {
          const data = await response.json();
          currentBalance.value = data.balance; // Update current balance
        } else {
          console.error("Failed to fetch user settings.");
        }
      } catch (error) {
        console.error("Error fetching user settings:", error);
      }
    };

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

    const fetchPortfolioComposition = async () => {
      try {
        const response = await fetch('http://localhost:8000/portfolio/composition');
        if (response.ok) {
          const data = await response.json();
          portfolioCompositionData.value = data.composition;
          totalPortfolioValue.value = data.total_portfolio_value;
          portfolioMessage.value = data.message || '';
          console.log("Portfolio Composition Data from backend:", data);
          console.log("Data passed to chart:", portfolioCompositionData.value);
        } else {
          console.error("Failed to fetch portfolio composition.");
          portfolioMessage.value = "Failed to load portfolio composition.";
        }
      } catch (error) {
        console.error("Error fetching portfolio composition:", error);
        portfolioMessage.value = "Error loading portfolio composition.";
      }
    };

    const topUp = async () => {
      if (amount.value <= 0) {
        balanceMessage.value = "Please enter a positive amount.";
        isSuccess.value = false;
        return;
      }
      try {
        const response = await fetch('http://localhost:8000/users/me/top-up', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ amount: amount.value })
        });
        if (response.ok) {
          const data = await response.json();
          currentBalance.value = data.balance;
          balanceMessage.value = `Successfully topped up $${amount.value.toFixed(2)}.`;
          isSuccess.value = true;
          amount.value = 0; // Reset amount input
          fetchPortfolioComposition(); // Refresh portfolio data after balance change
        } else {
          const errorData = await response.json();
          balanceMessage.value = `Top-up failed: ${errorData.detail || response.statusText}`;
          isSuccess.value = false;
        }
      } catch (error) {
        console.error("Error topping up:", error);
        balanceMessage.value = "Error topping up account.";
        isSuccess.value = false;
      }
    };

    const withdraw = async () => {
      if (amount.value <= 0) {
        balanceMessage.value = "Please enter a positive amount.";
        isSuccess.value = false;
        return;
      }
      try {
        const response = await fetch('http://localhost:8000/users/me/withdraw', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ amount: amount.value })
        });
        if (response.ok) {
          const data = await response.json();
          currentBalance.value = data.balance;
          balanceMessage.value = `Successfully withdrew $${amount.value.toFixed(2)}.`;
          isSuccess.value = true;
          amount.value = 0; // Reset amount input
          fetchPortfolioComposition(); // Refresh portfolio data after balance change
        } else {
          const errorData = await response.json();
          balanceMessage.value = `Withdrawal failed: ${errorData.detail || response.statusText}`;
          isSuccess.value = false;
        }
      } catch (error) {
        console.error("Error withdrawing:", error);
        balanceMessage.value = "Error withdrawing from account.";
        isSuccess.value = false;
      }
    };

    const setPeriod = (p) => {
      period.value = p;
      fetchSummary(p);
    };

    onMounted(() => {
      fetchUserData(); // Fetch user balance on mount
      fetchSummary(period.value);
      fetchPortfolioComposition(); // Fetch portfolio composition on mount
    });

    return {
      period,
      summary,
      currentBalance,
      formattedBalance,
      amount,
      balanceMessage,
      isSuccess,
      portfolioCompositionData,
      totalPortfolioValue,
      formattedTotalPortfolioValue,
      portfolioMessage,
      chartColors,
      setPeriod,
      topUp,
      withdraw
    };
  }
}
</script>

<style scoped>
.dashboard-container {
  padding: 40px;
  background-color: var(--primary-background);
  color: var(--text-color-light);
  min-height: calc(100vh - var(--nav-height, 100px));
}

h1 {
  color: var(--text-color-dark);
  margin-bottom: 25px;
  font-weight: 800;
  letter-spacing: -0.03em;
}

p {
  color: var(--text-color-light);
  margin-bottom: 15px;
}

.balance-card {
  background-color: var(--secondary-background);
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 6px 20px rgba(var(--color-darkest-rgb), 0.4);
  text-align: left;
  margin: 40px auto 20px auto;
  max-width: 700px;
  animation: fadeInSlideUp 0.6s ease-out forwards;
  border: 1px solid rgba(var(--color-light-grey-blue-rgb), 0.1);
}

.balance-card p {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 20px;
  color: var(--text-color-dark);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.balance-actions {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-top: 15px;
}

.amount-input {
  flex-grow: 1;
  padding: 10px;
  border: 1px solid var(--color-dark-grey-blue);
  border-radius: 8px;
  background-color: var(--color-darkest);
  color: var(--text-color-dark);
  font-size: 1rem;
  box-sizing: border-box;
}

.top-up-button {
  background-color: var(--accent-color);
  color: var(--text-color-dark);
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
}

.withdraw-button {
  background-color: var(--color-deep-blue); /* Different color for withdraw */
  color: var(--text-color-dark);
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
}

.message-success {
  color: #5cb85c;
  margin-top: 10px;
  font-size: 0.95rem;
}

.message-error {
  color: var(--danger-color);
  margin-top: 10px;
  font-size: 0.95rem;
}

.message-info {
  color: var(--text-color-light); /* For informative messages */
  margin-top: 10px;
  font-size: 0.95rem;
}

.portfolio-chart-card {
  background-color: var(--secondary-background);
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 6px 20px rgba(var(--color-darkest-rgb), 0.4);
  margin: 30px auto; /* Margin from balance card */
  max-width: 700px;
  animation: fadeInSlideUp 0.6s ease-out forwards;
  border: 1px solid rgba(var(--color-light-grey-blue-rgb), 0.1);
}

.portfolio-chart-card h2 {
  color: var(--text-color-dark);
  margin-top: 0;
  margin-bottom: 25px;
  font-size: 1.8rem;
  font-weight: 700;
  text-align: center;
}

.total-portfolio-value {
  text-align: center;
  font-size: 1.2rem;
  font-weight: 600;
  margin-top: 20px;
  color: var(--text-color-dark);
}

.button-group {
  margin-bottom: 30px;
  display: flex;
  justify-content: center;
  gap: 10px;
}

.button-group button {
  background-color: var(--secondary-background);
  color: var(--text-color-light);
  border: 1px solid var(--color-dark-grey-blue);
  padding: 10px 20px;
  margin: 0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  text-transform: capitalize;
  box-shadow: 0 2px 5px rgba(var(--color-darkest-rgb), 0.2);
}

.button-group button:hover {
  background-color: var(--color-vibrant-blue);
  color: var(--text-color-dark);
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 5px 15px rgba(var(--accent-color-rgb), 0.3);
}

.button-group button.active {
  background-color: var(--accent-color);
  color: var(--text-color-dark);
  border-color: var(--accent-color);
  box-shadow: 0 3px 10px rgba(var(--accent-color-rgb), 0.4);
}

.summary-card {
  background-color: var(--secondary-background);
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 6px 20px rgba(var(--color-darkest-rgb), 0.4);
  text-align: left;
  margin: 40px auto;
  max-width: 700px;
  opacity: 0;
  transform: translateY(30px);
  animation: fadeInSlideUp 0.6s ease-out forwards;
  border: 1px solid rgba(var(--color-light-grey-blue-rgb), 0.1);
}

.summary-card p {
  margin-bottom: 12px;
  color: var(--text-color-light);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.summary-value {
  font-weight: bold;
  color: var(--text-color-dark);
}

.positive {
  color: #5cb85c;
}

.negative {
  color: var(--danger-color);
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

/* Responsive adjustments */
@media (max-width: 768px) {
  .dashboard-container {
    padding: 20px;
  }

  .balance-card, .portfolio-chart-card, .summary-card {
    margin: 30px auto 20px auto;
    padding: 25px;
    max-width: 95%;
  }

  .balance-card p {
    font-size: 1.3rem;
  }

  .balance-actions {
    flex-direction: column;
    gap: 8px;
  }

  .amount-input {
    width: 100%;
  }

  .top-up-button, .withdraw-button {
    width: 100%;
    padding: 12px 15px;
  }

  .portfolio-chart-card h2 {
    font-size: clamp(1.4rem, 4vw, 1.8rem);
    margin-bottom: 20px;
  }

  .total-portfolio-value {
    font-size: 1.1rem;
  }

  .button-group {
    flex-direction: column;
    gap: 8px;
  }

  .button-group button {
    width: 100%;
    padding: 12px 15px;
  }

  .summary-card p {
    flex-direction: column;
    align-items: flex-start;
    margin-bottom: 8px;
  }

  .summary-value {
    margin-top: 5px;
  }
}

@media (max-width: 480px) {
  .dashboard-container {
    padding: 15px;
  }

  .balance-card, .portfolio-chart-card, .summary-card {
    padding: 20px;
    margin: 20px auto 15px auto;
  }

  .balance-card p {
    font-size: 1.2rem;
    flex-direction: column;
    align-items: flex-start;
  }

  .amount-input {
    font-size: 0.9rem;
    padding: 8px;
  }

  .top-up-button, .withdraw-button {
    font-size: 0.9rem;
    padding: 10px 15px;
  }

  .portfolio-chart-card h2 {
    font-size: clamp(1.2rem, 3.5vw, 1.4rem);
    margin-bottom: 15px;
  }

  .total-portfolio-value {
    font-size: 1rem;
  }

  .summary-card p {
    align-items: flex-start;
  }
}
</style>
