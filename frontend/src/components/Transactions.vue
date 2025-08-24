<template>
  <div class="transactions-container">
    <h1>Transactions Log</h1>

    <div class="table-container">
      <h2>All Transactions</h2>
      <table class="transactions-table">
        <thead>
          <tr>
            <th>Asset Name</th>
            <th>Date</th>
            <th>Type</th>
            <th>Price</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="transaction in transactions" :key="transaction.id">
            <td>{{ (transaction.asset && transaction.asset.name) || transaction.asset_name }}</td>
            <td>{{ transaction.date }}</td>
            <td>{{ transaction.type }}</td>
            <td>{{ transaction.price }}</td>
            <td class="actions-cell">
              <button @click="editTransaction(transaction)" class="edit-button">Edit</button>
              <button @click="deleteTransaction(transaction.id)" class="delete-button">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <button class="add-button" @click="openAddTransactionModal">+</button>

    <TransactionModal
      :is-visible="isModalVisible"
      :transaction-data="editingTransaction"
      @close="closeModal"
      @save-transaction="handleSaveTransaction"
    />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import TransactionModal from './TransactionModal.vue';

export default {
  name: 'Transactions',
  components: {
    TransactionModal
  },
  setup() {
    const transactions = ref([]);
    const isModalVisible = ref(false);
    const editingTransaction = ref(null);

    const fetchTransactions = async () => {
      try {
        const response = await fetch('http://localhost:8000/transactions');
        transactions.value = await response.json();
      } catch (error) {
        console.error("Error fetching transactions:", error);
      }
    };

    const openAddTransactionModal = () => {
      editingTransaction.value = null;
      isModalVisible.value = true;
    };

    const editTransaction = (transaction) => {
      editingTransaction.value = transaction;
      isModalVisible.value = true;
    };

    const closeModal = () => {
      editingTransaction.value = null; // Reset editing transaction before closing modal
      isModalVisible.value = false;
    };

    const handleSaveTransaction = async (transactionData) => {
      try {
        let response;
        if (transactionData.id) {
          response = await fetch(`http://localhost:8000/transactions/${transactionData.id}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(transactionData)
          });
        } else {
          response = await fetch('http://localhost:8000/transactions', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(transactionData)
          });
        }

        if (response.ok) {
          fetchTransactions();
        } else {
          console.error("Failed to submit transaction:", response.statusText);
        }
      } catch (error) {
        console.error("Error submitting transaction:", error);
      }
    };

    const deleteTransaction = async (id) => {
      try {
        const response = await fetch(`http://localhost:8000/transactions/${id}`, {
          method: 'DELETE'
        });
        if (response.ok) {
          fetchTransactions();
        } else {
          console.error("Failed to delete transaction:", response.statusText);
        }
      } catch (error) {
        console.error("Error deleting transaction:", error);
      }
    };

    onMounted(() => {
      fetchTransactions();
    });

    return {
      transactions,
      isModalVisible,
      editingTransaction,
      openAddTransactionModal,
      editTransaction,
      closeModal,
      handleSaveTransaction,
      deleteTransaction,
    };
  },
};
</script>

<style scoped>
.transactions-container {
  position: relative;
  padding: 40px;
  background-color: var(--primary-background);
  color: var(--text-color-light);
  min-height: calc(100vh - 100px);
}

h1 {
  color: var(--text-color-dark);
  margin-bottom: 25px;
  font-size: 2.8rem;
  font-weight: 800;
  letter-spacing: -0.03em;
}

.table-container {
  background: var(--secondary-background);
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 6px 20px rgba(var(--color-darkest-rgb), 0.4);
  margin: 30px auto;
  max-width: 900px;
  animation: fadeIn 0.6s ease-out forwards;
  border: 1px solid rgba(var(--color-light-grey-blue-rgb), 0.1);
}

h2 {
  color: var(--text-color-dark);
  margin-top: 0;
  margin-bottom: 25px;
  font-size: 1.8rem;
  font-weight: 700;
  text-align: center;
}

.transactions-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-top: 20px;
}

.transactions-table th,
.transactions-table td {
  padding: 15px 18px;
  text-align: left;
  border-bottom: 1px solid var(--color-dark-grey-blue); /* Darker border for table rows */
}

.transactions-table th {
  background-color: var(--color-dark-grey-blue);
  color: var(--text-color-light); /* Light text for headers */
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.95rem;
  letter-spacing: 0.08em;
}

.transactions-table th:first-child {
  border-top-left-radius: 10px;
}

.transactions-table th:last-child {
  border-top-right-radius: 10px;
}

.transactions-table tbody tr {
  transition: background-color 0.3s ease;
}

.transactions-table tbody tr:hover {
  background-color: var(--color-deep-blue); /* Subtle hover effect on dark */
}

.transactions-table td {
  color: var(--text-color-light); /* Light text for table data */
}

.actions-cell {
  white-space: nowrap;
}

.edit-button,
.delete-button {
  padding: 10px 18px;
  margin-right: 10px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.edit-button {
  background-color: var(--color-vibrant-blue);
  color: var(--text-color-dark);
}

.edit-button:hover {
  filter: brightness(1.1);
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(var(--accent-color-rgb), 0.3);
}

.delete-button {
  background-color: var(--danger-color);
  color: var(--text-color-dark);
}

.delete-button:hover {
  filter: brightness(1.1);
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(var(--danger-color-rgb), 0.3);
}

.add-button {
  position: fixed;
  bottom: 40px;
  right: 40px;
  width: 60px;
  height: 60px;
  background-color: var(--accent-color);
  color: var(--text-color-dark);
  border: none;
  border-radius: 50%;
  font-size: 2.2rem;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 8px 25px rgba(var(--color-darkest-rgb), 0.4);
  z-index: 999;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  /* Removed pointer-events: auto; as it was for debugging */
}

.add-button:hover {
  transform: translateY(-5px) rotate(135deg) scale(1.05);
  box-shadow: 0 12px 30px rgba(var(--accent-color-rgb), 0.5);
}

/* Removed temporary modal-overlay style */

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
