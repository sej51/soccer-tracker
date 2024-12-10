import pytest
from app.api_service import get_all_leagues, get_teams_by_league, get_team_info, get_team_fixtures, get_standings

@pytest.fixture
def valid_league_code():
    return "PL"

@pytest.fixture
def valid_team_name():
    return "Manchester United"

def test_get_all_leagues():
    leagues = get_all_leagues()
    assert isinstance(leagues, list)
    assert len(leagues) > 0
    assert any(league["code"] == "PL" for league in leagues)

def test_get_teams_by_league(valid_league_code):
    teams = get_teams_by_league(valid_league_code)
    assert isinstance(teams, list)
    assert len(teams) > 0
    assert any("Manchester United" in team["name"] for team in teams)

def test_get_team_info(valid_team_name, valid_league_code):
    team_info = get_team_info(valid_team_name, valid_league_code)
    assert team_info is not None
    assert valid_team_name in team_info["name"]
    assert "id" in team_info

def test_get_team_fixtures(valid_team_name, valid_league_code):
    team_info = get_team_info(valid_team_name, valid_league_code)
    assert team_info is not None

    team_id = team_info["id"]
    fixtures = get_team_fixtures(team_id)
    assert isinstance(fixtures, dict)
    assert "matches" in fixtures
    assert len(fixtures["matches"]) > 0

def test_get_standings(valid_league_code):
    standings = get_standings(valid_league_code)
    assert isinstance(standings, dict)
    assert "standings" in standings
    assert len(standings["standings"]) > 0
    assert "table" in standings["standings"][0]
    assert len(standings["standings"][0]["table"]) > 0