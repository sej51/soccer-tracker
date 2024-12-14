from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from .api_service import (
    get_all_leagues,
    get_teams_by_league,
    get_team_info
)
from .helper import get_fixtures_by_league, get_all_leagues, get_formatted_team_fixtures, get_standings_table, send_email, validate_form_inputs, generate_email_content

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
    league_code, team_name = request.form.get('league'), request.form.get('team')
    if not league_code or not team_name:
        return "League or team not selected. Please go back and try again.", 400

    team_info = get_team_info(team_name, league_code)
    if not team_info:
        return f"Sorry, no data found for team: {team_name}", 404

    today = datetime.now()
    upcoming_games = get_formatted_team_fixtures(team_info["id"], today)
    standings_table = get_standings_table(league_code)

    return render_template(
        'team.html',
        team=team_info,
        standings=standings_table,
        upcoming_games=upcoming_games,
        selected_team_id=team_info["id"]
    )


@main.route('/fixtures')
def fixtures():
    fixtures_by_league = get_fixtures_by_league()
    return render_template('fixtures.html', fixtures_by_league=fixtures_by_league)

@main.route('/api/teams/<league_code>')
def get_teams_api(league_code):
    teams = get_teams_by_league(league_code)
    if not teams:
        return {"teams": []}, 404
    return {"teams": [{"name": team["name"], "id": team["id"]} for team in teams]}, 200

@main.route('/email', methods=['GET', 'POST'])
def email_report():
    if request.method == 'POST':
        league_code, team_name, email = request.form.get('league'), request.form.get('team'), request.form.get('email')
        if not validate_form_inputs(league_code, team_name, email):
            flash("Please provide all required information.", "danger")
            return redirect(url_for('main.email_report'))

        team_info = get_team_info(team_name, league_code)
        if not team_info:
            flash(f"Team {team_name} not found in {league_code}!", "danger")
            return redirect(url_for('main.email_report'))

        email_content = generate_email_content(team_info, league_code)
        if send_email(email, f"Report for {team_name}", email_content):
            flash(f"Email sent successfully to {email}!", "success")
        else:
            flash("Failed to send email. Please try again later.", "danger")
        return redirect(url_for('main.home'))

    return render_template("email.html", leagues=get_all_leagues())