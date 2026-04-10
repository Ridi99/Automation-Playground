import requests
import time
import os
from datetime import datetime

# --- SANITIZED CONFIGURATION ---
API_KEY = os.getenv("API_SPORTS_KEY", "YOUR_API_KEY") 
API_HOST = "v3.football.api-sports.io"

def get_team_history_from_api(team_id):
    """ Asks the API for the last 5 matches of a team (Stateless) """
    try:
        url = f"https://{API_HOST}/fixtures"
        params = {'team': team_id, 'last': 5, 'status': 'FT'}
        headers = {'x-apisports-key': API_KEY, 'x-apisports-host': API_HOST}
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        # In-memory aggregation logic...
        return 2.5 # Mock return for bootstrap
    except:
        return 0

print("✅ Stateless API Microservice Loaded.")
