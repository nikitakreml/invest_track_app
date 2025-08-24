from typing import List, Dict
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

# For simplicity, we are using a dummy Credentials object. In a real application,
# this would involve a proper OAuth2 flow to obtain and refresh credentials.
# The 'api_key' parameter currently represents a placeholder for such a mechanism.

def read_transactions_from_sheets(api_key: str, spreadsheet_id: str) -> List[Dict]:
    creds = Credentials(token=None, refresh_token=None, token_uri=None, client_id=None, client_secret=None, scopes=None)
    service = build('sheets', 'v4', credentials=creds)

    # The ID and range of a sample spreadsheet.
    SAMPLE_RANGE_NAME = 'Sheet1!A:D' # Adjust as needed

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
        return []
    
    transactions = []
    headers = [header.strip() for header in values[0]]  # Assuming first row is headers
    for row in values[1:]:
        # Ensure row has enough columns to match headers
        if len(row) >= len(headers):
            transaction = {
                "Asset Name": row[headers.index("Asset Name")],
                "Transaction Date": row[headers.index("Transaction Date")],
                "Type": row[headers.index("Type")],
                "Asset Price": float(row[headers.index("Asset Price")]), # Convert to float
            }
            transactions.append(transaction)
        else:
            print(f"Skipping row due to insufficient columns: {row}")
    
    print(f"Reading from Google Sheets with API Key: {api_key} and Spreadsheet ID: {spreadsheet_id}")
    print(f"Transactions from sheets: {transactions}")
    return transactions

def write_transaction_to_sheets(api_key: str, spreadsheet_id: str, transaction_data: Dict):
    creds = Credentials(token=None, refresh_token=None, token_uri=None, client_id=None, client_secret=None, scopes=None)
    service = build('sheets', 'v4', credentials=creds)

    # The ID and range of a sample spreadsheet.
    SAMPLE_RANGE_NAME = 'Sheet1!A:D' # Adjust if you have more columns for writing

    # Prepare the data to be written
    # The order of data should match the order of columns in the sheet: Asset Name, Transaction Date, Type, Asset Price
    values = [
        [
            transaction_data["asset_name"],
            transaction_data["date"],
            transaction_data["type"],
            transaction_data["price"]
        ]
    ]
    body = {
        'values': values
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range=SAMPLE_RANGE_NAME,
        valueInputOption='RAW', insertDataOption='INSERT_ROWS', body=body).execute()
    
    print(f"Writing to Google Sheets with API Key: {api_key}, Spreadsheet ID: {spreadsheet_id}, Data: {transaction_data}")
    print(f"{result.get('updates').get('updatedCells')} cells appended.")
