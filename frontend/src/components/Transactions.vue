<template>
  <div>
    <h1>Transactions Log</h1>
    <h2>Add/Edit Transaction</h2>
    <form @submit.prevent="submitTransaction">
      <div>
        <label for="assetName">Asset Name:</label>
        <input type="text" id="assetName" v-model="transactionForm.asset_name" required />
      </div>
      <div>
        <label for="date">Date:</label>
        <input type="date" id="date" v-model="transactionForm.date" required />
      </div>
      <div>
        <label for="type">Type:</label>
        <select id="type" v-model="transactionForm.type" required>
          <option value="Buy">Buy</option>
          <option value="Sell">Sell</option>
        </select>
      </div>
      <div>
        <label for="price">Price:</label>
        <input type="number" id="price" v-model="transactionForm.price" required />
      </div>
      <button type="submit">{{ editingTransactionId ? 'Update' : 'Add' }} Transaction</button>
      <button type="button" v-if="editingTransactionId" @click="cancelEdit">Cancel Edit</button>
    </form>

    <h2>All Transactions</h2>
    <ul>
      <li v-for="transaction in transactions" :key="transaction.id">
        {{ transaction.asset_name }} - {{ transaction.date }} - {{ transaction.type }} - {{ transaction.price }}
        <button @click="editTransaction(transaction)">Edit</button>
        <button @click="deleteTransaction(transaction.id)">Delete</button>
      </li>
    </ul>
  </div>
</template>

<script>
import { ref, onMounted, reactive } from 'vue';

export default {
  name: 'Transactions',
  setup() {
    const transactions = ref([]);
    const transactionForm = reactive({
      asset_name: '',
      date: '',
      type: 'Buy',
      price: 0
    });
    const editingTransactionId = ref(null);

    const fetchTransactions = async () => {
      try {
        const response = await fetch('http://localhost:8000/transactions');
        transactions.value = await response.json();
      } catch (error) {
        console.error("Error fetching transactions:", error);
      }
    };

    const submitTransaction = async () => {
      try {
        let response;
        if (editingTransactionId.value) {
          response = await fetch(`http://localhost:8000/transactions/${editingTransactionId.value}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(transactionForm)
          });
        } else {
          response = await fetch('http://localhost:8000/transactions', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(transactionForm)
          });
        }
        
        if (response.ok) {
          resetForm();
          fetchTransactions();
        } else {
          console.error("Failed to submit transaction:", response.statusText);
        }
      } catch (error) {
        console.error("Error submitting transaction:", error);
      }
    };

    const editTransaction = (transaction) => {
      editingTransactionId.value = transaction.id;
      transactionForm.asset_name = transaction.asset.name; // Assuming asset is nested
      transactionForm.date = transaction.date; // Assuming date is in YYYY-MM-DD format
      transactionForm.type = transaction.type;
      transactionForm.price = transaction.price;
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

    const cancelEdit = () => {
      resetForm();
    };

    const resetForm = () => {
      editingTransactionId.value = null;
      transactionForm.asset_name = '';
      transactionForm.date = '';
      transactionForm.type = 'Buy';
      transactionForm.price = 0;
    };

    onMounted(() => {
      fetchTransactions();
    });

    return {
      transactions,
      transactionForm,
      editingTransactionId,
      submitTransaction,
      editTransaction,
      deleteTransaction,
      cancelEdit
    };
  }
}
</script>
