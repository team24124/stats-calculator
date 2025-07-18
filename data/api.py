import requests

from data import get_auth, get_config
from teams.Team import Team


def get_team_from_ftc(team_number: int) -> Team:
    """
    Get a team object from a team number from querying the FTC API
    :param team_number: Valid FTC Team Number
    :return: Team object without any games played
    """
    season = get_config()['season']
    team_response = requests.get(f"https://ftc-api.firstinspires.org/v2.0/{season}/teams?teamNumber={team_number}",
                                 auth=get_auth())

    if team_response.status_code == 400:
        raise ValueError(f"The team number {team_number} you tried to find does not exist.")

    team_data = team_response.json()['teams'][0]

    team = Team(
        team_number=team_number,
        country=team_data['country'],
        state_prov=team_data['stateProv'],
        city=team_data['city'],
        home_region=team_data['homeRegion'],
        name=team_data['nameShort']
    )

    return team


def get_team_from_nighthawks(team_number: int) -> Team:
    """
    Get a team object from a team number querying the Nighthawks Stats database.
    Only queries from the most recent season.
    (https://nighthawks-stats.vercel.app/api/teams)
    :param team_number: Valid FTC Team Number
    :return: Team object with last updated statistics and games played
    """
    from teams import get_team_from_json

    team_response = requests.get(f"https://nighthawks-stats.vercel.app/api/teams/{team_number}")

    if team_response.status_code == 404:
        raise ValueError(f"The team number {team_number} you tried to find does not exist.")

    team_data = team_response.json()
    team = get_team_from_json(team_data)

    return team