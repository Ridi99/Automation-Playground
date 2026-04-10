import requests
import csv
import os
import time
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- SANITIZED CONFIGURATION ---
API_KEY = os.getenv("API_SPORTS_KEY", "YOUR_API_KEY") 
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID")

MIN_MINUTE = 46 
MAX_MINUTE = 80
REQUIRED_GOALS_LAST_MATCH = 3.0 
HISTORY_FILE = "history.csv"

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message}, timeout=10)
    except:
        pass

# API Polling and Database cross-referencing logic...
print("✅ Hybrid Strict Momentum Engine Loaded.")
