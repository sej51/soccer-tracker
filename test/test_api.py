from app.api_service import get_all_leagues, get_teams_by_league

def test_get_all_leagues():
    leagues = get_all_leagues()
    assert isinstance(leagues, list)
    assert len(leagues) > 0
    assert "code" in leagues[0]
    assert "name" in leagues[0]

def test_get_teams_by_league():
    teams = get_teams_by_league("PL")
    assert isinstance(teams, list)
    assert len(teams) > 0
    assert "id" in teams[0]
    assert "name" in teams[0]