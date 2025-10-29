import gspread
from google.oauth2.service_account import Credentials
import csv
import os
import requests

# Authenticate with Google Sheets API (JSON from secret)
def authenticate_google_sheets(service_account_json):
    import json
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    credentials_info = json.loads(service_account_json)
    credentials = Credentials.from_service_account_info(credentials_info, scopes=SCOPES)
    client = gspread.authorize(credentials)
    return client

# Clear specific columns
def clear_columns(sheet_url, range_to_clear, service_account_json):
    client = authenticate_google_sheets(service_account_json)
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.get_worksheet(0)  # First worksheet
    worksheet.batch_clear([range_to_clear])
    return worksheet

# Read data from CSV (repo-relative path)
def read_csv_data(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return list(reader)

# Main execution (called from workflow)
def run_update(service_account_json, sheet_url, range_to_clear, csv_file_path):
    # Step 1: Run odds fetcher (assume NBA_PPODDS.py is in repo root)
    exec(open('NBA_PPODDS.py').read())  # Inline exec for simplicity; or import if modular

    # Step 2: Clear sheet
    worksheet = clear_columns(sheet_url, range_to_clear, service_account_json)

    # Step 3: Update sheet from CSV
    data_from_csv = read_csv_data(csv_file_path)
    worksheet.update(range_name="A1", values=data_from_csv)

if __name__ == "__main__":
    # For local testing—set env vars
    service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
    run_update(service_account_json, os.getenv('SHEET_URL'), os.getenv('RANGE_TO_CLEAR'), os.getenv('CSV_FILE_PATH'))
