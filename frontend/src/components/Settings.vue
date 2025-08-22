<template>
  <div class="settings-container">
    <h1>Settings</h1>
    <p>Manage your Google Sheets API key here.</p>
    <form @submit.prevent="saveApiKey" class="settings-form">
      <div class="form-group">
        <label for="apiKey">Google Sheets API Key:</label>
        <input type="text" id="apiKey" v-model="apiKey" required />
      </div>
      <button type="submit" class="save-button">Save API Key</button>
    </form>

    <h2>Google Sheets Integration (Stub)</h2>
    <div class="sheets-integration">
      <div class="form-group">
        <label for="spreadsheetId">Spreadsheet ID:</label>
        <input type="text" id="spreadsheetId" v-model="spreadsheetId" />
      </div>
      <button @click="readFromSheets" class="read-button">Read Transactions from Sheets (Stub)</button>
      <button @click="writeToSheets" class="write-button">Write Dummy Transaction to Sheets (Stub)</button>
    </div>
    <p v-if="sheetsMessage" class="sheets-message">{{ sheetsMessage }}</p>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  name: 'Settings',
  setup() {
    const apiKey = ref('');
    const spreadsheetId = ref('');
    const sheetsMessage = ref('');

    const saveApiKey = async () => {
      try {
        const response = await fetch('http://localhost:8000/auth/set-key', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ api_key: apiKey.value })
        });
        if (response.ok) {
          alert("API Key saved successfully!");
        } else {
          alert("Failed to save API Key.");
        }
      } catch (error) {
        console.error("Error saving API Key:", error);
      }
    };

    const readFromSheets = async () => {
      try {
        sheetsMessage.value = 'Reading from sheets...';
        const response = await fetch(`http://localhost:8000/google_sheets/read_transactions?spreadsheet_id=${spreadsheetId.value}`);
        const data = await response.json();
        if (response.ok) {
          sheetsMessage.value = `Read success! Transactions: ${JSON.stringify(data.transactions)}`;
        } else {
          sheetsMessage.value = `Read failed: ${data.detail || response.statusText}`;
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
        const response = await fetch(`http://localhost:8000/google_sheets/write_transaction?spreadsheet_id=${spreadsheetId.value}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(dummyTransaction)
        });
        if (response.ok) {
          sheetsMessage.value = "Dummy transaction written to sheets (check console for stub output).";
        } else {
          sheetsMessage.value = `Write failed: ${data.detail || response.statusText}`;
        }
      } catch (error) {
        console.error("Error writing to sheets:", error);
        sheetsMessage.value = 'Error writing to sheets.';
      }
    };

    return {
      apiKey,
      spreadsheetId,
      sheetsMessage,
      saveApiKey,
      readFromSheets,
      writeToSheets
    };
  }
}
</script>

<style scoped>
.settings-container {
  padding: 20px;
  background-color: #F2F2F2;
  color: #174D38;
}

h1 {
  color: #4D1717;
  margin-bottom: 20px;
}

p {
  color: #174D38;
}

h2 {
  color: #174D38;
  margin-top: 30px;
  margin-bottom: 15px;
}

.settings-form, .sheets-integration {
  background-color: #FFFFFF;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #174D38;
}

input[type="text"] {
  width: calc(100% - 22px);
  padding: 10px;
  border: 1px solid #CBCBCB;
  border-radius: 4px;
  font-size: 1rem;
}

button {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  margin-right: 10px;
}

.save-button,
.read-button {
  background-color: #174D38;
  color: white;
}

.write-button {
  background-color: #CBCBCB;
  color: #174D38;
}

.sheets-message {
  margin-top: 15px;
  font-style: italic;
  color: #4D1717;
}
</style>
