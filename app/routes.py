from flask import Blueprint, render_template, request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo 

from .api_service import get_all_leagues, get_teams_by_league, get_team_info, get_team_fixtures
from .helper import convert_to_local_time

main = Blueprint('main', __name__)
@main.route('/')
def home():
    leagues = get_all_leagues()
    teams_by_league = {
        league["name"]: get_teams_by_league(league["code"])
        for league in leagues
    }
    return render_template('home.html', teams_by_league=teams_by_league)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/team', methods=['POST'])
def team():
    team_name = request.form['team']
    team_info = get_team_info(team_name)

    if not team_info:
        return f"Sorry, no data found for team: {team_name}", 404

    today = datetime.now()
    team_id = team_info["id"]
    last_month = today - timedelta(days=30)
    next_month = today + timedelta(days=30)

    upcoming_games = get_team_fixtures(
        team_id, date_from=today.strftime('%Y-%m-%d'), date_to=next_month.strftime('%Y-%m-%d')
    )

    # We could not figure out local time conversion, so we used ChatGPT and learned about ZoneInfo
    def format_game_dates(games):
        for game in games.get("matches", []):
            game["formattedDate"] = convert_to_local_time(game["utcDate"])
        return games.get("matches", [])

    upcoming_games = format_game_dates(upcoming_games)

    return render_template(
        "team.html",
        team=team_info,
        upcoming_games=upcoming_games
    )