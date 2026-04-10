import requests
import csv
import io
import datetime
import time
import os
import telebot

# --- SANITIZED CONFIGURATION ---
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN") 
CHANNEL_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID") 

LEAGUES = ["E0", "E1", "SP1", "I1", "D1", "F1", "N1", "P1", "T1"]
BASE_URL = "https://www.football-data.co.uk/mmz4281/2526/" 

bot = telebot.TeleBot(BOT_TOKEN)

def fetch_and_clean_data():
    all_matches = []
    for league in LEAGUES:
        url = f"{BASE_URL}{league}.csv"
        try:
            response = requests.get(url)
            response.raise_for_status()
            csv_data = csv.DictReader(io.StringIO(response.text))
            
            for row in csv_data:
                if not row.get('Date'): continue # Data Sanitization
                clean_match = {
                    'League': league,
                    'HomeTeam': row.get('HomeTeam'),
                    'AwayTeam': row.get('AwayTeam'),
                    'FTHG': int(row['FTHG']) if row.get('FTHG') not in [None, ''] else None,
                    'FTAG': int(row['FTAG']) if row.get('FTAG') not in [None, ''] else None,
                    'AwayOdds': float(row['AvgA']) if row.get('AvgA') not in [None, ''] else 0.0
                }
                all_matches.append(clean_match)
        except Exception as e:
            pass
    return all_matches

# Main engine logic goes here...
print("✅ ETL Data Sniper Engine Loaded.")
