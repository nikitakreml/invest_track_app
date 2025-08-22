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
            <td>
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
  padding: 20px;
  background-color: #F2F2F2;
  color: #174D38;
}

h1 {
  color: #4D1717;
  margin-bottom: 20px;
}

.table-container {
  background: #FFFFFF;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #174D38;
  margin-top: 0;
  margin-bottom: 15px;
}

.transactions-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
}

.transactions-table th,
.transactions-table td {
  border: 1px solid #CBCBCB;
  padding: 10px;
  text-align: left;
}

.transactions-table th {
  background-color: #CBCBCB;
  font-weight: bold;
  color: #174D38;
}

.transactions-table tr:nth-child(even) {
  background-color: #F2F2F2;
}

.edit-button,
.delete-button {
  padding: 5px 10px;
  margin-right: 5px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.edit-button {
  background-color: #174D38;
  color: white;
}

.delete-button {
  background-color: #4D1717;
  color: white;
}

.add-button {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 60px;
  height: 60px;
  background-color: #174D38;
  color: white;
  border: none;
  border-radius: 50%;
  font-size: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  z-index: 999;
}
</style>
