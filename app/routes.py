from flask import Blueprint, render_template

main = Blueprint('main', __name__)
@main.route('/')
def home():
    leagues = [
        {"code": "PL", "name": "Premier League"},
        {"code": "BL1", "name": "Bundesliga"},
        {"code": "FL1", "name": "Ligue 1"},
        {"code": "PD", "name": "La Liga"},
        {"code": "SA", "name": "Serie A"},
    ]
    return render_template('home.html', leagues=leagues)

@main.route('/about')
def about():
    return render_template('about.html')