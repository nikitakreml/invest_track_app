<template>
  <div class="modal-overlay" :class="{ active: isVisible }" v-if="isVisible" @click.self="closeModal">
    <div class="modal-content">
      <h2>{{ transactionId ? 'Edit Transaction' : 'Add New Transaction' }}</h2>
      <form @submit.prevent="submitTransaction">
        <div class="form-group">
          <label for="assetName">Asset Name:</label>
          <input type="text" id="assetName" v-model="form.asset_name" required />
        </div>
        <div class="form-group">
          <label for="date">Date:</label>
          <input type="date" id="date" v-model="form.date" required />
        </div>
        <div class="form-group">
          <label for="type">Type:</label>
          <select id="type" v-model="form.type" required>
            <option value="Buy">Buy</option>
            <option value="Sell">Sell</option>
          </select>
        </div>
        <div class="form-group">
          <label for="price">Price:</label>
          <input type="number" id="price" v-model="form.price" :disabled="settings.auto_transaction_price_enabled && form.asset_name && form.date" required />
          <button type="button" class="estimate-price-button" @click="estimatePrice" v-if="settings.auto_transaction_price_enabled && form.asset_name && form.date">Estimate Price</button>
        </div>
        <div class="modal-actions">
          <button type="submit" class="submit-button">{{ transactionId ? 'Update' : 'Add' }} Transaction</button>
          <button type="button" class="cancel-button" @click="closeModal">Cancel</button>
        </div>
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
  background: rgba(var(--color-darkest-rgb), 0.7); /* Using darkest color with opacity */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.modal-overlay.active {
  opacity: 1;
}

.modal-content {
  background: var(--secondary-background); /* Use secondary background for modal content */
  padding: 30px;
  border-radius: 15px;
  min-width: 450px; /* Slightly wider modal */
  max-width: 90%;
  box-shadow: 0 8px 30px rgba(var(--color-darkest-rgb), 0.6);
  transform: scale(0.8);
  opacity: 0;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  color: var(--text-color-light); /* Default text color in modal */
  border: 1px solid rgba(var(--color-light-grey-blue-rgb), 0.1);
}

.modal-overlay.active .modal-content {
  transform: scale(1);
  opacity: 1;
}

.modal-content h2 {
  margin-top: 0;
  margin-bottom: 25px;
  color: var(--text-color-dark); /* Heading white */
  font-size: 1.8rem;
  font-weight: 700;
  text-align: center;
}

.form-group {
  margin-bottom: 20px;
}

.modal-content label {
  margin-bottom: 8px; /* Increased margin */
  font-weight: 500;
  color: var(--text-color-light); /* Labels light grey-blue */
  font-size: 0.95rem;
}

.modal-content input[type="text"],
.modal-content input[type="date"],
.modal-content input[type="number"],
.modal-content select {
  width: 100%; /* Set width to 100% */
  box-sizing: border-box; /* Include padding and border in width */
  padding: 12px;
  border: 1px solid var(--color-dark-grey-blue);
  border-radius: 8px;
  font-size: 1rem;
  background-color: var(--color-darkest); /* Inputs are dark */
  color: var(--text-color-dark); /* Light text in dark inputs */
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.modal-content input:focus, .modal-content select:focus {
  border-color: var(--accent-color);
  box-shadow: 0 0 0 3px rgba(var(--accent-color-rgb), 0.4);
  outline: none;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px; /* Spacing between buttons */
  margin-top: 30px;
}

.modal-content button {
  padding: 12px 25px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.modal-content button:hover {
  filter: brightness(1.1);
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 5px 15px rgba(var(--color-darkest-rgb), 0.3);
}

.modal-content .submit-button {
  background-color: var(--accent-color);
  color: var(--text-color-dark);
}

.modal-content .cancel-button {
  background-color: var(--color-dark-grey-blue); /* Subtle dark background for cancel */
  color: var(--text-color-light);
}

.estimate-price-button {
  margin-top: 10px; /* Space between input and button */
  display: block; /* Full width for button below input */
  width: 100%; /* Ensure button also takes full width */
  background-color: var(--color-deep-blue); /* Distinct color for estimate button */
  color: var(--text-color-dark);
  border: 1px solid var(--color-deep-blue);
}

.estimate-price-button:hover {
  filter: brightness(1.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(var(--color-deep-blue-rgb), 0.4);
}
</style>
