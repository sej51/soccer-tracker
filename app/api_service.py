import requests

from .config import API_BASE_URL, API_TOKEN

def fetch_data_from_api(url, params=None):
    """
    Generalized function to fetch data from the API.
    """
    headers = {"X-Auth-Token": API_TOKEN}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        print(f"Response content: {response.content}")
        return None

def get_all_leagues():
    """
    Fetch all supported leagues.
    """
    url = f"{API_BASE_URL}/competitions"
    leagues_data = fetch_data_from_api(url)
    if not leagues_data:
        return []
    return [
        {"code": league["code"], "name": league["name"]}
        for league in leagues_data.get("competitions", [])
        if league["code"] in ["PL", "BL1", "FL1", "PD", "SA"]
    ]

def get_teams_by_league(league_code):
    """
    Fetch all teams for a specific league.
    """
    url = f"{API_BASE_URL}/competitions/{league_code}/teams"
    teams_data = fetch_data_from_api(url)
    return teams_data.get("teams", []) if teams_data else []

def get_team_info(team_name, league_code):
    """
    Fetch specific team information by league.
    """
    teams = get_teams_by_league(league_code)
    for team in teams:
        if team_name.lower() in team["name"].lower():
            return team
    return None

def get_team_fixtures(team_id, date_from=None, date_to=None):
    """
    Fetch team-specific fixtures in a date range.
    """
    url = f"{API_BASE_URL}/teams/{team_id}/matches"
    params = {"dateFrom": date_from, "dateTo": date_to}
    fixtures_data = fetch_data_from_api(url, params=params)
    return fixtures_data if fixtures_data else {}

def get_standings(competition="PL"):
    """
    Fetch standings for a specific league.
    """
    url = f"{API_BASE_URL}/competitions/{competition}/standings"
    standings_data = fetch_data_from_api(url)
    return standings_data if standings_data else {"standings": []}

def get_fixtures(competition, date_from=None, date_to=None):
    """
    Fetch fixtures for the specified competition and date range.
    """
    headers = {"X-Auth-Token": API_TOKEN}
    params = {"dateFrom": date_from, "dateTo": date_to}

    response = requests.get(f"{API_BASE_URL}/competitions/{competition}/matches", headers=headers, params=params)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        print(f"Response content: {response.content}")
        return None

    return response.json()