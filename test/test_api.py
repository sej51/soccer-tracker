import pytest
from unittest.mock import patch
from app.api_service import get_teams_by_league, get_team_info, get_standings, get_fixtures
from app.helper import send_email

# We kept getting the GitHub Actions failure due to the API's capacity.
# So, we used ChatGPT to see if we could reolve this issue and it recommended unittest.mock

@pytest.fixture
def valid_league_code():
    return "PL"

@pytest.fixture
def valid_team_name():
    return "Manchester United"

@pytest.fixture
def valid_email():
    return "test@example.com"

@pytest.fixture
def mock_teams():
    return [{"name": "Manchester United"}, {"name": "Chelsea"}]

@pytest.fixture
def mock_standings():
    return {
        "standings": [
            {
                "table": [
                    {"position": 1, "team": {"name": "Manchester United"}, "points": 50},
                    {"position": 2, "team": {"name": "Chelsea"}, "points": 48},
                ]
            }
        ]
    }

@pytest.fixture
def mock_fixtures():
    return {
        "matches": [
            {
                "utcDate": "2024-12-15T17:30:00Z",
                "homeTeam": {"name": "Chelsea"},
                "awayTeam": {"name": "Manchester United"},
            }
        ]
    }


@patch("app.api_service.get_teams_by_league")
def test_get_teams_by_league(mock_get_teams_by_league):
    # Mocked response to match the actual API response structure
    mock_teams = [
        {
            "area": {"name": "England"},
            "id": 66,
            "name": "Manchester United FC",
            "shortName": "Man United",
            "tla": "MUN",
        },
        {
            "area": {"name": "England"},
            "id": 61,
            "name": "Chelsea FC",
            "shortName": "Chelsea",
            "tla": "CHE",
        },
    ]
    
    mock_get_teams_by_league.return_value = mock_teams
    
    # Call the function under test
    teams = get_teams_by_league("PL")
    
    print("Teams returned:", teams)
    
    # Adjust assertions to match the data structure
    assert isinstance(teams, list)
    assert len(teams) > 0
    assert any(team["name"] == "Manchester United FC" for team in teams)

@patch("app.api_service.get_team_info")
def test_get_team_info(mock_get_team_info, valid_team_name, valid_league_code):
    mock_get_team_info.return_value = {"name": "Manchester United FC"}
    team_info = get_team_info(valid_team_name, valid_league_code)

    print("Team info returned:", team_info)

    assert team_info is not None
    assert valid_team_name in team_info["name"]

@patch("app.api_service.get_standings")
def test_get_standings(mock_get_standings, valid_league_code, mock_standings):
    mock_get_standings.return_value = mock_standings
    standings = get_standings(valid_league_code)
    assert isinstance(standings, dict)
    assert "standings" in standings
    assert len(standings["standings"][0]["table"]) > 0

@patch("app.api_service.get_fixtures")
def test_get_fixtures(mock_get_fixtures, valid_league_code, mock_fixtures):
    mock_get_fixtures.return_value = mock_fixtures
    fixtures = get_fixtures(valid_league_code, date_from="2024-12-01", date_to="2024-12-31")
    assert isinstance(fixtures, dict)
    assert len(fixtures["matches"]) > 0

@patch("app.helper.send_email")
def test_send_email(mock_send_email, valid_email):
    mock_send_email.return_value = True
    email_sent = send_email(
        to_email=valid_email,
        subject="Test Email",
        content="<h1>Test Content</h1>",
    )
    assert email_sent is True