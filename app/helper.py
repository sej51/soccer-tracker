from datetime import datetime, timedelta
from .api_service import get_team_fixtures, get_standings
from zoneinfo import ZoneInfo
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from .api_service import get_all_leagues, get_fixtures, get_standings, get_team_fixtures
import os

def convert_to_local_time(utc_time, timezone="America/New_York"):
    """
    Convert a UTC time string to a local timezone.
    :param utc_time: UTC time string in ISO 8601 format (e.g., "2024-12-12T18:30:00Z")
    :param timezone: Target timezone (default: "America/New_York")
    :return: Local time string in a readable format
    """
    utc_dt = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%SZ")  # Parse UTC time
    local_dt = utc_dt.replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo(timezone))  # Convert to local timezone
    return local_dt.strftime("%A, %d %b %Y %H:%M")  # Format the local time

def format_game_dates(fixtures):
    for fixture in fixtures.get("matches", []):
        fixture["formattedDate"] = convert_to_local_time(fixture["utcDate"])
    return fixtures.get("matches", [])

def validate_form_inputs(league_code, team_name, email):
    return bool(league_code and team_name and email)

def get_formatted_team_fixtures(team_id, today):
    next_month = today + timedelta(days=30)
    fixtures = get_team_fixtures(
        team_id, date_from=today.strftime('%Y-%m-%d'), date_to=next_month.strftime('%Y-%m-%d')
    )
    return format_game_dates(fixtures)

def get_standings_table(league_code):
    standings = get_standings(league_code)
    if standings and "standings" in standings and len(standings["standings"]) > 0:
        return standings["standings"][0].get("table", [])
    return []

def get_fixtures_by_league():
    today = datetime.now()
    next_week = today + timedelta(weeks=1)

    date_from = today.strftime('%Y-%m-%d')
    date_to = next_week.strftime('%Y-%m-%d')

    fixtures_by_league = {}
    for league in get_all_leagues():
        league_fixtures = get_fixtures(league["code"], date_from=date_from, date_to=date_to)
        if league_fixtures:
            fixtures_by_league[league["name"]] = format_game_dates(league_fixtures)
    return fixtures_by_league

def send_email(to_email, subject, content):
    """
    Send an email using SendGrid.
    """
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
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

def generate_email_content(team_info, league_code):
    today = datetime.now()
    upcoming_games = get_formatted_team_fixtures(team_info["id"], today)
    standings_table = get_standings_table(league_code)

    return f"""
    <h1>{team_info['name']}</h1>
    <img src="{team_info['crest']}" alt="{team_info['name']} Logo" width="150">
    <h2>Upcoming Games</h2>
    <ul>
    {"".join(f"<li>{game['formattedDate']}: {game['homeTeam']['name']} vs {game['awayTeam']['name']}</li>" for game in upcoming_games)}
    </ul>
    <h2>Standings</h2>
    <table border="1" cellpadding="5">
        <tr>
            <th>Position</th>
            <th>Team</th>
            <th>Points</th>
        </tr>
        {"".join(f"<tr><td>{standing['position']}</td><td>{standing['team']['name']}</td><td>{standing['points']}</td></tr>" for standing in standings_table)}
    </table>
    """