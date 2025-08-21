from typing import List, Dict

def read_transactions_from_sheets(api_key: str, spreadsheet_id: str) -> List[Dict]:
    # This is a stub for Google Sheets integration.
    # In a real application, you would use the Google Sheets API here.
    print(f"Reading from Google Sheets with API Key: {api_key} and Spreadsheet ID: {spreadsheet_id}")
    return [
        {"Asset Name": "Dummy Stock", "Transaction Date": "2023-01-01", "Type": "Buy", "Asset Price": 100.0},
        {"Asset Name": "Dummy Crypto", "Transaction Date": "2023-01-15", "Type": "Sell", "Asset Price": 500.0}
    ]

def write_transaction_to_sheets(api_key: str, spreadsheet_id: str, transaction_data: Dict):
    # This is a stub for Google Sheets integration.
    # In a real application, you would use the Google Sheets API here.
    print(f"Writing to Google Sheets with API Key: {api_key}, Spreadsheet ID: {spreadsheet_id}, Data: {transaction_data}")
    pass
