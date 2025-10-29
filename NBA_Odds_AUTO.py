import subprocess
import gspread
from google.oauth2.service_account import Credentials
import csv

# Authenticate with Google Sheets API
def authenticate_google_sheets(json_keyfile_path):
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    credentials = Credentials.from_service_account_file(json_keyfile_path, scopes=SCOPES)
    client = gspread.authorize(credentials)
    return client

# Clear specific columns
def clear_columns(sheet_url, range_to_clear, json_keyfile_path):
    client = authenticate_google_sheets(json_keyfile_path)
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.get_worksheet(0)  # Assuming the first worksheet
    worksheet.batch_clear([range_to_clear])  # Clear the specified range
    return worksheet

# Read data from CSV
def read_csv_data(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return list(reader)  # Convert CSV rows to a list of lists

# Main execution logic
def run_update():
    # Paths and configurations
    SERVICE_ACCOUNT_FILE = "/Users/kahlilhodge/NBA 2024/service_account.json"
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1icQQCvavKgi0w4pZa--RWvdF9PHyQxUDC5jEyoyIlTY/edit?gid=1296920125#gid=1296920125"
    RANGE_TO_CLEAR = "A:G"
    CSV_FILE_PATH = "/Users/kahlilhodge/NBA 2024/NBA_odds_2024.csv"

    # Step 1: Run NBA_PPODDS.py to update the CSV file
    print("Running NBA_PPODDS.py...")
    subprocess.run(["python3", "/Users/kahlilhodge/NBA 2024/NBA_PPODDS.py"], check=True)
    print("NBA_PPODDS.py executed successfully.")

    # Step 2: Clear columns A:G in the Google Sheet
    print("Clearing columns A:G...")
    worksheet = clear_columns(SHEET_URL, RANGE_TO_CLEAR, SERVICE_ACCOUNT_FILE)

    # Step 3: Import data from CSV into the Google Sheet
    print("Importing data from CSV...")
    data_from_csv = read_csv_data(CSV_FILE_PATH)
    worksheet.update(range_name="A1", values=data_from_csv)  # Start updating from A1
    print("Google Sheet updated successfully.")

if __name__ == "__main__":
    run_update()