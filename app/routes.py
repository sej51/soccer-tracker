from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo 

from .api_service import get_all_leagues, get_teams_by_league, get_team_info, get_team_fixtures, get_standings, get_fixtures
from .helper import convert_to_local_time, format_game_dates

main = Blueprint('main', __name__)
@main.route('/', methods=['GET', 'POST'])
def home():
    leagues = [
        {"code": "PL", "name": "Premier League"},
        {"code": "BL1", "name": "Bundesliga"},
        {"code": "FL1", "name": "Ligue 1"},
        {"code": "PD", "name": "La Liga"},
        {"code": "SA", "name": "Serie A"}
    ]

    selected_league = request.form.get('league')
    teams = get_teams_by_league(selected_league) if selected_league else []

    return render_template('home.html', leagues=leagues, teams=teams, selected_league=selected_league)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/team', methods=['POST'])
def team():
    league_code = request.form.get('league')
    team_name = request.form.get('team')

    if not league_code or not team_name:
        flash("Please select a league and a team.", "danger")
        return redirect(url_for("main.home"))

    team_info = get_team_info(team_name, league_code)
    if not team_info:
        flash(f"No data found for the team '{team_name}'.", "warning")
        return redirect(url_for("main.home"))

    today = datetime.now()
    next_month = today + timedelta(days=30)
    team_id = team_info["id"]

    upcoming_games = get_team_fixtures(
        team_id, date_from=today.strftime('%Y-%m-%d'), date_to=next_month.strftime('%Y-%m-%d')
    )

    if not upcoming_games:
        flash(f"No upcoming fixtures found for {team_name}.", "info")

    standings = get_standings(league_code)
    if not standings or not standings.get("standings", []):
        flash(f"Standings data is unavailable for {league_code}.", "info")

    upcoming_games = format_game_dates(upcoming_games)

    standings = get_standings(league_code)

    return render_template(
        'team.html',
        team=team_info,
        standings=standings.get("standings", [])[0].get("table", []),
        upcoming_games=upcoming_games,
        selected_team_id=team_id
    )

@main.route('/fixtures')
def fixtures():
    today = datetime.now()
    next_week = today + timedelta(weeks=1)

    date_from = today.strftime('%Y-%m-%d')
    date_to = next_week.strftime('%Y-%m-%d')

    leagues = [
        {"code": "PL", "name": "Premier League"},
        {"code": "BL1", "name": "Bundesliga"},
        {"code": "FL1", "name": "Ligue 1"},
        {"code": "PD", "name": "La Liga"},
        {"code": "SA", "name": "Serie A"}
    ]

    fixtures_by_league = {}
    for league in leagues:
        fixtures = get_fixtures(league["code"], date_from=date_from, date_to=date_to)
        if fixtures:
            fixtures_by_league[league["name"]] = format_game_dates(fixtures)
    
    if not fixtures_by_league:
        flash("No fixtures available for the upcoming week.", "info")
        return redirect(url_for("main.home"))


    return render_template('fixtures.html', fixtures_by_league=fixtures_by_league)