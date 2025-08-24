<template>
  <div class="modal-overlay" v-if="isVisible" @click.self="closeModal">
    <div class="modal-content">
      <h2>{{ transactionId ? 'Edit Transaction' : 'Add New Transaction' }}</h2>
      <form @submit.prevent="submitTransaction">
        <div>
          <label for="assetName">Asset Name:</label>
          <input type="text" id="assetName" v-model="form.asset_name" required />
        </div>
        <div>
          <label for="date">Date:</label>
          <input type="date" id="date" v-model="form.date" required />
        </div>
        <div>
          <label for="type">Type:</label>
          <select id="type" v-model="form.type" required>
            <option value="Buy">Buy</option>
            <option value="Sell">Sell</option>
          </select>
        </div>
        <div>
          <label for="price">Price:</label>
          <input type="number" id="price" v-model="form.price" :disabled="settings.auto_transaction_price_enabled && form.asset_name && form.date" required />
          <button type="button" @click="estimatePrice" v-if="settings.auto_transaction_price_enabled && form.asset_name && form.date">Estimate Price</button>
        </div>
        <button type="submit">{{ transactionId ? 'Update' : 'Add' }} Transaction</button>
        <button type="button" @click="closeModal">Cancel</button>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, reactive, watch, onMounted } from 'vue';

export default {
  name: 'TransactionModal',
  props: {
    isVisible: Boolean,
    transactionData: Object,
  },
  emits: ['close', 'save-transaction'],
  setup(props, { emit }) {
    const transactionId = ref(null);
    const form = reactive({
      asset_name: '',
      date: '',
      type: 'Buy',
      price: 0
    });
    const settings = reactive({
      auto_transaction_price_enabled: true
    });

    const fetchSettings = async () => {
      try {
        const response = await fetch('http://localhost:8000/users/me/settings');
        if (response.ok) {
          const data = await response.json();
          settings.auto_transaction_price_enabled = data.auto_transaction_price_enabled;
        } else {
          console.error("Failed to fetch settings.");
        }
      } catch (error) {
        console.error("Error fetching settings:", error);
      }
    };

    const estimatePrice = async () => {
      if (!form.asset_name || !form.date) {
        alert("Please enter asset name and date to estimate price.");
        return;
      }
      try {
        const response = await fetch(`http://localhost:8000/asset/estimate-price?ticker=${form.asset_name}&target_date=${form.date}`);
        const data = await response.json();
        if (response.ok) {
          form.price = data.price;
        } else {
          alert(`Failed to estimate price: ${data.detail || response.statusText}`);
        }
      } catch (error) {
        console.error("Error estimating price:", error);
        alert("Error estimating price.");
      }
    };

    const resetForm = () => {
      transactionId.value = null;
      form.asset_name = '';
      form.date = '';
      form.type = 'Buy';
      form.price = 0;
    };

    watch(() => props.transactionData, (newVal) => {
      if (newVal) {
        transactionId.value = newVal.id;
        form.asset_name = newVal.asset ? newVal.asset.name : '';
        form.date = newVal.date; 
        form.type = newVal.type;
        form.price = newVal.price;
      } else {
        resetForm();
      }
    });

    onMounted(() => {
      fetchSettings();
    });

    const submitTransaction = () => {
      emit('save-transaction', { id: transactionId.value, ...form });
      closeModal();
    };

    const closeModal = () => {
      emit('close');
      resetForm();
    };

    return {
      transactionId,
      form,
      settings,
      submitTransaction,
      closeModal,
      estimatePrice
    };
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(77, 23, 23, 0.5); /* Using #4D1717 with 50% opacity */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: #F2F2F2; /* Changed from white to F2F2F2 for consistency */
  padding: 20px;
  border-radius: 8px;
  min-width: 400px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.modal-content h2 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #4D1717;
}

.modal-content form div {
  margin-bottom: 15px;
}

.modal-content label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #174D38;
}

.modal-content input[type="text"],
.modal-content input[type="date"],
.modal-content input[type="number"],
.modal-content select {
  width: calc(100% - 22px); /* Account for padding and border */
  padding: 10px;
  border: 1px solid #CBCBCB;
  border-radius: 4px;
  font-size: 1rem;
}

.modal-content button {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  margin-right: 10px;
}

.modal-content button[type="submit"] {
  background-color: #174D38;
  color: white;
}

.modal-content button[type="button"] {
  background-color: #4D1717;
  color: white;
}

.modal-content button[type="button"]:last-child {
  margin-right: 0;
}
</style>
