from flask import Blueprint, render_template, request
from .api_service import get_all_leagues, get_teams_by_league

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
    return render_template('team.html', team_name=team_name)