import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = "https://api.football-data.org/v4"
API_TOKEN = os.getenv("API_TOKEN")

def get_all_leagues():
    """Fetch all supported leagues from the API."""
    headers = {"X-Auth-Token": API_TOKEN}
    response = requests.get(f"{API_BASE_URL}/competitions", headers=headers)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        print(f"Response content: {response.content}")
        return []
    
    leagues = response.json().get("competitions", [])

    # Used ChatGPT to generate this - we could not figure out how to get only the leagues we wanted
    filtered_leagues = [
        {"code": league["code"], "name": league["name"]}
        for league in leagues
        if league["code"] in ["PL", "BL1", "FL1", "PD", "SA"]
    ]
    return filtered_leagues

def get_teams_by_league(league_code):
    """Fetch all teams in the specified league."""
    headers = {"X-Auth-Token": API_TOKEN}
    response = requests.get(f"{API_BASE_URL}/competitions/{league_code}/teams", headers=headers)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        print(f"Response content: {response.content}")
        return []

    return response.json().get("teams", [])