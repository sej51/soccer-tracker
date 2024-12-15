import pytest
from app.api_service import (
    get_all_leagues,
    get_teams_by_league,
    get_team_info,
    get_team_fixtures,
    get_standings,
    get_fixtures,
)
from app.helper import send_email

@pytest.fixture
def valid_league_code():
    return "PL"

@pytest.fixture
def valid_team_name():
    return "Manchester United"

@pytest.fixture
def valid_email():
    return "test@example.com"

def test_get_all_leagues():
    leagues = get_all_leagues()
    assert isinstance(leagues, list)
    assert len(leagues) > 0
    assert any(league.get("code") == "PL" for league in leagues)

def test_get_teams_by_league(valid_league_code):
    teams = get_teams_by_league(valid_league_code)
    assert isinstance(teams, list)
    assert len(teams) > 0
    assert any("Manchester United" in team.get("name", "") for team in teams)

def test_get_team_info(valid_team_name, valid_league_code):
    team_info = get_team_info(valid_team_name, valid_league_code)
    assert team_info is not None
    assert valid_team_name in team_info.get("name", "")

def test_get_team_fixtures(valid_team_name, valid_league_code):
    team_info = get_team_info(valid_team_name, valid_league_code)
    assert team_info is not None

    team_id = team_info.get("id")
    assert team_id is not None, "Team ID not found in team info"

    fixtures = get_team_fixtures(team_id)
    assert isinstance(fixtures, dict)
    assert "matches" in fixtures

def test_get_standings(valid_league_code):
    standings = get_standings(valid_league_code)
    assert isinstance(standings, dict)
    assert "standings" in standings
    assert len(standings.get("standings", [])) > 0

def test_get_fixtures(valid_league_code):
    fixtures = get_fixtures(valid_league_code, date_from="2024-12-01", date_to="2024-12-31")
    assert isinstance(fixtures, dict)
    assert "matches" in fixtures

def test_send_email(valid_email):
    email_sent = send_email(
        to_email=valid_email,
        subject="Test Email",
        content="<h1>Test Content</h1>",
    )
    assert email_sent is True
