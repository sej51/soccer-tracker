import os
import requests
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

API_BASE_URL = "https://api.football-data.org/v4"
API_TOKEN = os.getenv("API_TOKEN")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

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

def get_team_info(team_name, league_code):
    """Fetch team information by name within the given league."""
    headers = {"X-Auth-Token": API_TOKEN}
    response = requests.get(f"{API_BASE_URL}/competitions/{league_code}/teams", headers=headers)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        print(f"Response content: {response.content}")
        return None

    teams = response.json().get("teams", [])
    for team in teams:
        if team_name.lower() in team["name"].lower():
            return team
    return None

def get_team_fixtures(team_id, date_from=None, date_to=None):
    """Fetch fixtures for a specific team within a date range."""
    headers = {"X-Auth-Token": API_TOKEN}
    params = {}
    if date_from:
        params["dateFrom"] = date_from
    if date_to:
        params["dateTo"] = date_to

    response = requests.get(f"{API_BASE_URL}/teams/{team_id}/matches", headers=headers, params=params)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        print(f"Response content: {response.content}")
        return None

    return response.json()  # Return fixtures data

def get_standings(competition="PL"):
    """Fetch league standings."""
    headers = {"X-Auth-Token": API_TOKEN}
    response = requests.get(f"{API_BASE_URL}/competitions/{competition}/standings", headers=headers)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        print(f"Response content: {response.content}")
        return {"standings": []} 

    standings_data = response.json()
    if "standings" not in standings_data:
        print(f"Unexpected standings structure: {standings_data}")
        return {"standings": []}

    return standings_data

def get_fixtures(competition, date_from=None, date_to=None):
    """Fetch fixtures for the specified competition and date range."""
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

def get_all_teams(competition="PL"):
    """Fetch all teams in the specified competition."""
    headers = {"X-Auth-Token": API_TOKEN}
    response = requests.get(f"{API_BASE_URL}/competitions/{competition}/teams", headers=headers)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        print(f"Response content: {response.content}")
        return None

    return response.json().get("teams", [])

def send_email(to_email, subject, content):
    """Send an email using SendGrid."""
    try:
        message = Mail(
            from_email="sjolly03@gmail.com",
            to_emails=to_email,
            subject=subject,
            html_content=content
    )
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent successfully! Status code: {response.status_code}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False