<template>
  <div class="transactions-container">
    <h1>Transactions Log</h1>

    <div class="table-container">
      <h2>All Transactions</h2>
      <div class="table-scroll-wrapper">
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
  min-height: calc(100vh - var(--nav-height, 100px));
}

h1 {
  color: var(--text-color-dark);
  margin-bottom: 25px;
  /* font-size: 2.8rem; Let global clamp() handle this */
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
  /* font-size: 1.8rem; Let global clamp() handle this */
  font-weight: 700;
  text-align: center;
}

.table-scroll-wrapper {
  overflow-x: auto; /* Enable horizontal scrolling for tables on small screens */
  -webkit-overflow-scrolling: touch; /* Smooth scrolling on iOS */
}

.transactions-table {
  width: 100%;
  min-width: 600px; /* Ensure table has a minimum width for scrolling */
  border-collapse: separate;
  border-spacing: 0;
  margin-top: 20px;
}

.transactions-table th,
.transactions-table td {
  padding: 15px 18px;
  text-align: left;
  border-bottom: 1px solid var(--color-dark-grey-blue);
}

.transactions-table th {
  background-color: var(--color-dark-grey-blue);
  color: var(--text-color-light);
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
  background-color: var(--color-deep-blue);
}

.transactions-table td {
  color: var(--text-color-light);
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
}

.add-button:hover {
  transform: translateY(-5px) rotate(135deg) scale(1.05);
  box-shadow: 0 12px 30px rgba(var(--accent-color-rgb), 0.5);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .transactions-container {
    padding: 20px;
  }

  .table-container {
    padding: 20px;
    margin: 20px auto;
    max-width: 95%; /* Make table container more fluid */
  }

  .transactions-table th,
  .transactions-table td {
    padding: 10px 12px; /* Reduce padding for tighter table */
    font-size: 0.85rem; /* Smaller font size for table content */
  }

  .actions-cell button {
    padding: 6px 10px; /* Smaller action buttons */
    font-size: 0.8rem;
    margin-right: 5px;
  }

  .add-button {
    bottom: 20px; /* Adjust FAB position for mobile */
    right: 20px;
    width: 50px;
    height: 50px;
    font-size: 1.8rem;
    box-shadow: 0 4px 15px rgba(var(--color-darkest-rgb), 0.3);
  }

  .add-button:hover {
    transform: translateY(-3px) rotate(135deg) scale(1.02);
    box-shadow: 0 6px 20px rgba(var(--accent-color-rgb), 0.4);
  }
}

@media (max-width: 480px) {
  .transactions-container {
    padding: 15px;
  }

  .table-container {
    padding: 15px;
    margin: 15px auto;
  }

  h1 {
    font-size: clamp(2rem, 5vw, 2.8rem); /* Fluid font size for h1 on very small screens */
  }

  h2 {
    font-size: clamp(1.4rem, 4vw, 1.8rem); /* Fluid font size for h2 on very small screens */
  }

  .transactions-table th,
  .transactions-table td {
    padding: 8px 10px; /* Even tighter table cells */
    font-size: 0.8rem;
  }

  .actions-cell button {
    padding: 5px 8px;
    font-size: 0.75rem;
  }

  .add-button {
    bottom: 15px;
    right: 15px;
    width: 45px;
    height: 45px;
    font-size: 1.6rem;
  }
}
</style>
