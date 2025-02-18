import pandas as pd
from openpyxl import load_workbook
import dotenv
import os
import requests
import time

dotenv.load_dotenv()
CIELO_API_KEY=os.getenv("CIELO_API_KEY")

# Load your Excel file
file_path = 'test.xlsx'  
def save_pnl_and_winrate_to_excel():
  df = pd.read_excel(file_path, engine='openpyxl')

  # Function to get price based on wallet address
  def get_price(wallet_address):
    cielo_url = f"https://feed-api.cielo.finance/api/v1/{wallet_address}/pnl/total-stats"  # URL to check wallet stats using Cielo API
    cielo_headers = {
      "accept": "application/json",
      "X-API-KEY": CIELO_API_KEY  # Set headers with Cielo API key
    }
    
    cielo_response = requests.get(cielo_url, headers=cielo_headers)  # Send GET request to Cielo API
    print(f"Checking {wallet_address}... => cielo response status code is {cielo_response.status_code}")
    if cielo_response.status_code != 200:
      return "Not sure"
    else :
      cielo_data = cielo_response.json()
      print(cielo_data)
      Pnl = cielo_data['data']['realized_pnl_usd']
      Winrate = cielo_data['data']['winrate']
      return Pnl, Winrate

  df[['Total_Pnl', 'Winrate']] = df.iloc[:, 0].apply(get_price).apply(pd.Series)


  # Save the updated DataFrame back to Excel
  output_file_path = 'test.xlsx'  # Update with your desired output path
  df.to_excel(output_file_path, index=False)

  # Load the workbook and select the active worksheet
  wb = load_workbook(output_file_path)
  ws = wb.active

  # Set the original width for columns
  ws.column_dimensions['A'].width = 58
  ws.column_dimensions['B'].width = 15
  ws.column_dimensions['C'].width = 15

  # Save the workbook again
  wb.save(output_file_path)
  print("Pnl and winrate modified successfully! Will update in 24 hours later..")

while True:  # Infinite loop to repeatedly execute the following actions
  save_pnl_and_winrate_to_excel()
  time.sleep(86400)  # Pause execution for 259200 seconds (3 days) before repeating