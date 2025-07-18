import requests

from data import get_config, get_auth
from data.api import get_team_from_nighthawks
from teams.Team import Team


def get_team_from_json(team_data: dict) -> Team:
    """
    Create a team object from a json response
    :param team_data: Correctly shaped JSON response as a dictionary
    :return: Team object
    """
    # Extract data from json response

    team_number = team_data['team_number']
    team_name = team_data['team_name']
    country = team_data['country']
    state_province = team_data['state_province']
    city = team_data['city']
    home_region = team_data['home_region']

    games_played = team_data['games_played']
    matches = team_data['matches']

    epa_total = team_data['epa_total']
    auto_epa_total = team_data['auto_epa_total']
    tele_epa_total = team_data['tele_epa_total']

    historical_epa = team_data['historical_epa']
    historical_auto_epa = team_data['historical_auto_epa']
    historical_tele_epa = team_data['historical_tele_epa']

    opr = team_data['opr']
    opr_auto = team_data['opr_auto']
    opr_tele = team_data['opr_tele']
    opr_end = team_data['opr_end']

    historical_opr = team_data['historical_opr']
    historical_auto_opr = team_data['historical_auto_opr']
    historical_tele_opr = team_data['historical_tele_opr']
    historical_end_opr = team_data['historical_end_opr']

    # Create team object
    team = Team(team_number, team_name, country, state_province, city, home_region)
    team.games_played = games_played
    team.matches = matches

    team.epa_total = epa_total
    team.epa_auto_total = auto_epa_total
    team.epa_tele_total = tele_epa_total

    team.historical_epa = historical_epa
    team.historical_auto_epa = historical_auto_epa
    team.historical_tele_epa = historical_tele_epa

    team.opr = opr
    team.opr_auto = opr_auto
    team.opr_tele = opr_tele
    team.opr_end = opr_end

    team.historical_opr = historical_opr
    team.historical_auto_opr = historical_auto_opr
    team.historical_tele_opr = historical_tele_opr
    team.historical_end_opr = historical_end_opr

    return team


def get_teams_at_event(event_code: str) -> list[int]:
    """
    Retrieve a list of team numbers for teams at a given event code
    :param event_code: Valid FTC event code
    :return: List off all team numbers at an event
    """
    season = get_config()['season']
    teams_response = requests.get(f"https://ftc-api.firstinspires.org/v2.0/{season}/teams?eventCode={event_code}",
                                  auth=get_auth())

    if teams_response.status_code == 400:
        raise ValueError("The given event code could not be found.")

    teams_data = teams_response.json()['teams']
    team_number_list = [team['teamNumber'] for team in teams_data]

    return team_number_list


def get_team_data_from_event(event_code: str) -> dict[int, Team]:
    """
    Get team data for all teams at a given evvent
    :param event_code: Valid FTC event code
    :return: Dictionary of all team data at event (key=team number, value=team data object)
    """
    # Create a list of all team numbers
    team_number_list = get_teams_at_event(event_code)

    # Use dictionary comprehension to create team data
    team_data = {team_number: get_team_from_nighthawks(team_number) for team_number in team_number_list}
    return team_data


def get_team_data_from_events(event_codes: list[str]) -> dict[int, Team]:
    """
    Get team data for all teams from a given list of events
    :param event_codes: List of Valid FTC event code
    :return: Dictionary of all team data at event (key=team number, value=team data object)
    """
    # Create a list of all team numbers
    team_number_list = []

    for event_code in event_codes:
        team_number_list += get_teams_at_event(event_code)

    # Use dictionary comprehension to create team data
    team_data = {team_number: get_team_from_nighthawks(team_number) for team_number in team_number_list}
    return team_data
