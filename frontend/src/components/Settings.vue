<template>
  <div class="settings-container">
    <h1>Settings</h1>
    <p>Manage your application settings here.</p>
    <form @submit.prevent="saveSettings" class="settings-form">
      <div class="form-group">
        <label for="googleSheetsApiKey">Google Sheets API Key:</label>
        <input type="text" id="googleSheetsApiKey" v-model="settings.google_sheets_api_key" />
      </div>
      <div class="form-group">
        <label for="googleSheetsSpreadsheetId">Google Sheets Spreadsheet ID:</label>
        <input type="text" id="googleSheetsSpreadsheetId" v-model="settings.google_sheets_spreadsheet_id" />
      </div>
      <div class="form-group">
        <label for="tinkoffInvestApiToken">Tinkoff Invest API Token:</label>
        <input type="text" id="tinkoffInvestApiToken" v-model="settings.tinkoff_invest_api_token" />
      </div>
      <div class="form-group checkbox-group">
        <input type="checkbox" id="autoTransactionPriceEnabled" v-model="settings.auto_transaction_price_enabled" />
        <label for="autoTransactionPriceEnabled">Enable Auto Transaction Price</label>
      </div>
      <button type="submit" class="save-button">Save Settings</button>
    </form>

    <h2>Google Sheets Integration Actions (Stub)</h2>
    <div class="sheets-integration">
      <button @click="readFromSheets" class="read-button">Read Transactions from Sheets</button>
      <button @click="writeToSheets" class="write-button">Write Dummy Transaction to Sheets</button>
    </div>
    <p v-if="sheetsMessage" class="sheets-message">{{ sheetsMessage }}</p>
  </div>
</template>

<script>
import { ref, onMounted, reactive } from 'vue';

export default {
  name: 'Settings',
  setup() {
    const settings = reactive({
      google_sheets_api_key: '',
      google_sheets_spreadsheet_id: '',
      tinkoff_invest_api_token: '',
      auto_transaction_price_enabled: true
    });
    const sheetsMessage = ref('');

    const fetchSettings = async () => {
      try {
        const response = await fetch('http://localhost:8000/users/me/settings');
        if (response.ok) {
          const data = await response.json();
          Object.assign(settings, data);
        } else {
          console.error("Failed to fetch settings.");
        }
      } catch (error) {
        console.error("Error fetching settings:", error);
      }
    };

    const saveSettings = async () => {
      try {
        const response = await fetch('http://localhost:8000/users/me/settings', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(settings)
        });
        if (response.ok) {
          alert("Settings saved successfully!");
        } else {
          alert("Failed to save settings.");
        }
      } catch (error) {
        console.error("Error saving settings:", error);
      }
    };

    const readFromSheets = async () => {
      try {
        sheetsMessage.value = 'Reading from sheets...';
        const response = await fetch(`http://localhost:8000/google_sheets/read_transactions`);
        const data = await response.json();
        if (response.ok) {
          sheetsMessage.value = `Read success! Transactions: ${JSON.stringify(data.transactions)}`;
        } else {
          const errorData = await response.json();
          sheetsMessage.value = `Read failed: ${errorData.detail || response.statusText}`;
        }
      } catch (error) {
        console.error("Error reading from sheets:", error);
        sheetsMessage.value = 'Error reading from sheets.';
      }
    };

    const writeToSheets = async () => {
      try {
        sheetsMessage.value = 'Writing to sheets...';
        const dummyTransaction = {
          asset_name: "Test Asset",
          date: new Date().toISOString().slice(0, 10),
          type: "Buy",
          price: 123.45
        };
        const response = await fetch(`http://localhost:8000/google_sheets/write_transaction`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(dummyTransaction)
        });
        if (response.ok) {
          sheetsMessage.value = "Dummy transaction written to sheets (check console for stub output).";
        } else {
          const errorData = await response.json();
          sheetsMessage.value = `Write failed: ${errorData.detail || response.statusText}`;
        }
      } catch (error) {
        console.error("Error writing to sheets:", error);
        sheetsMessage.value = 'Error writing to sheets.';
      }
    };

    onMounted(() => {
      fetchSettings();
    });

    return {
      settings,
      sheetsMessage,
      saveSettings,
      readFromSheets,
      writeToSheets
    };
  }
}
</script>

<style scoped>
.settings-container {
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

p {
  color: var(--text-color-light);
  /* font-size: 1.1rem; Let global clamp() handle this */
  margin-bottom: 20px;
}

h2 {
  color: var(--text-color-dark);
  margin-top: 40px;
  margin-bottom: 20px;
  /* font-size: 1.8rem; Let global clamp() handle this */
  font-weight: 700;
}

.settings-form, .sheets-integration {
  background-color: var(--secondary-background);
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 6px 20px rgba(var(--color-darkest-rgb), 0.4);
  margin: 30px auto;
  max-width: 600px;
  animation: fadeIn 0.6s ease-out forwards;
  border: 1px solid rgba(var(--color-light-grey-blue-rgb), 0.1);
}

.form-group {
  margin-bottom: 20px;
}

.checkbox-group {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  padding: 10px;
  background-color: var(--color-darkest);
  border-radius: 8px;
  border: 1px solid var(--color-dark-grey-blue);
  box-shadow: inset 0 1px 3px rgba(var(--color-darkest-rgb), 0.3);
}

.checkbox-group input[type="checkbox"] {
  width: 20px;
  height: 20px;
  margin-right: 15px;
  transform: scale(1);
  accent-color: var(--accent-color);
  cursor: pointer;
  transition: transform 0.2s ease;
}

.checkbox-group input[type="checkbox"]:checked {
  transform: scale(1.1);
}

.checkbox-group label {
  margin-bottom: 0;
  font-size: 1rem;
  color: var(--text-color-dark);
  font-weight: 500;
}

label {
  /* Global label styles already defined in App.vue, ensure consistency */
}

input[type="text"] {
  /* Global input styles already defined in App.vue, ensure consistency */
}

button {
  /* Global button styles already defined in App.vue, ensure consistency */
}

.save-button,
.read-button {
  background-color: var(--accent-color);
  color: var(--text-color-dark);
}

.write-button {
  background-color: var(--secondary-background);
  color: var(--text-color-light);
  border: 1px solid var(--color-dark-grey-blue);
}

.sheets-message {
  margin-top: 20px;
  font-style: italic;
  color: var(--danger-color);
  font-size: 0.95rem;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .settings-container {
    padding: 20px;
  }

  .settings-form, .sheets-integration {
    padding: 25px;
    margin: 25px auto;
    max-width: 95%;
  }

  h1 {
    font-size: clamp(2rem, 5vw, 2.8rem);
  }

  h2 {
    font-size: clamp(1.4rem, 4vw, 1.8rem);
    margin-top: 30px;
  }

  p {
    font-size: clamp(0.9rem, 2.5vw, 1.1rem);
  }

  .checkbox-group {
    padding: 8px;
  }

  .checkbox-group input[type="checkbox"] {
    width: 18px;
    height: 18px;
    margin-right: 10px;
  }

  .checkbox-group label {
    font-size: 0.9rem;
  }

  .save-button, .read-button, .write-button {
    padding: 10px 20px;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .settings-container {
    padding: 15px;
  }

  .settings-form, .sheets-integration {
    padding: 20px;
    margin: 20px auto;
  }

  .form-group {
    margin-bottom: 15px;
  }

  .checkbox-group {
    flex-direction: column;
    align-items: flex-start;
    padding: 10px 15px;
  }

  .checkbox-group input[type="checkbox"] {
    margin-bottom: 5px;
  }

  .checkbox-group label {
    text-align: left;
    width: 100%;
  }

  .modal-content button {
    width: 100%;
    margin-top: 10px;
    margin-right: 0;
  }
}
</style>
