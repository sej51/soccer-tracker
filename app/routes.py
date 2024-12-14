from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta
from .api_service import (
    get_all_leagues,
    get_teams_by_league,
    get_team_info,
    get_team_fixtures,
    get_standings,
    get_fixtures
)
from .helper import format_game_dates, send_email

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def home():
    leagues = get_all_leagues()
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
        return "League or team not selected. Please go back and try again.", 400

    team_info = get_team_info(team_name, league_code)
    if not team_info:
        return f"Sorry, no data found for team: {team_name}", 404

    today = datetime.now()
    next_month = today + timedelta(days=30)
    team_id = team_info["id"]

    upcoming_games = get_team_fixtures(
        team_id, date_from=today.strftime('%Y-%m-%d'), date_to=next_month.strftime('%Y-%m-%d')
    )
    upcoming_games = format_game_dates(upcoming_games)

    standings = get_standings(league_code)

    standings_table = []
    if standings and "standings" in standings and len(standings["standings"]) > 0:
        standings_table = standings["standings"][0].get("table", [])

    return render_template(
        'team.html',
        team=team_info,
        standings=standings_table,
        upcoming_games=upcoming_games,
        selected_team_id=team_id
    )

@main.route('/fixtures')
def fixtures():
    today = datetime.now()
    next_week = today + timedelta(weeks=1)

    date_from = today.strftime('%Y-%m-%d')
    date_to = next_week.strftime('%Y-%m-%d')

    leagues = get_all_leagues()

    fixtures_by_league = {}
    for league in leagues:
        league_fixtures = get_fixtures(league["code"], date_from=date_from, date_to=date_to)
        if league_fixtures:
            fixtures_by_league[league["name"]] = format_game_dates(league_fixtures)

    return render_template('fixtures.html', fixtures_by_league=fixtures_by_league)

@main.route('/api/teams/<league_code>')
def get_teams_api(league_code):
    teams = get_teams_by_league(league_code)
    if not teams:
        return {"teams": []}, 404
    return {"teams": [{"name": team["name"]} for team in teams]}, 200

@main.route('/email', methods=['GET', 'POST'])
def email_report():
    if request.method == 'POST':
        league_code = request.form.get('league')
        team_name = request.form.get('team')
        email = request.form.get('email')

        # Validate form inputs
        if not league_code or not team_name or not email:
            flash("Please provide all required information.", "danger")
            return redirect(url_for('main.email_report'))
        
        # Fetch team data
        team_info = get_team_info(team_name, league_code)
        if not team_info:
            flash(f"Team {team_name} not found in {league_code}!", "danger")
            return redirect(url_for('main.email_report'))
        
        # Fetch additional data for the report
        team_id = team_info["id"]
        today = datetime.now()
        next_month = today + timedelta(days=30)
        upcoming_games = get_team_fixtures(
            team_id, date_from=today.strftime('%Y-%m-%d'), date_to=next_month.strftime('%Y-%m-%d')
        )
        standings = get_standings(league_code)

        # Format upcoming games
        formatted_games = format_game_dates(upcoming_games)

        # Generate email content
        email_content = f"""
        <h1>{team_info['name']}</h1>
        <img src="{team_info['crest']}" alt="{team_info['name']} Logo" width="150">
        <h2>Upcoming Games</h2>
        <ul>
        {"".join(f"<li>{game['formattedDate']}: {game['homeTeam']['name']} vs {game['awayTeam']['name']}</li>" for game in formatted_games)}
        </ul>
        <h2>Standings</h2>
        <table border="1" cellpadding="5">
            <tr>
                <th>Position</th>
                <th>Team</th>
                <th>Points</th>
            </tr>
            {"".join(f"<tr><td>{standing['position']}</td><td>{standing['team']['name']}</td><td>{standing['points']}</td></tr>" for standing in standings.get('standings', [])[0].get('table', []))}
        </table>
        """

        # Send the email
        if send_email(email, f"Report for {team_name}", email_content):
            flash(f"Email sent successfully to {email}!", "success")
        else:
            flash("Failed to send email. Please try again later.", "danger")
        return redirect(url_for('main.home'))
    
    # Fetch all teams for all leagues
    leagues = get_all_leagues()
    all_teams = []
    for league in leagues:
        league_teams = get_teams_by_league(league["code"])
        for team in league_teams:
            all_teams.append({"name": team["name"], "league": league["name"]})

    return render_template("email.html", teams=all_teams, leagues=leagues)