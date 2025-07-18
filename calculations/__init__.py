from datetime import datetime

import requests

from averages import get_start_avg
from calculations.epa import update_epa
from calculations.opr import update_opr
from data import get_config, get_auth, get_season_score_parser
from data.api import get_team_from_ftc
from data.scores import EventData
from events import get_all_events
from events.Event import Event
from export import export_team_data
from teams import get_team_data_from_event, get_team_data_from_events
from teams.Team import Team


def calculate_all_stats():
    events = get_all_events()
    return calculate_epa_opr(events)


def calculate_epa_opr(events: list[Event]):
    team_data: dict[int, Team] = {}

    # Get starting avg for EPA calculations
    avg_total, avg_auto, avg_tele = get_start_avg()

    for event in events:
        update_teams_at_event(event, team_data, avg_total, avg_auto, avg_tele)

    return team_data


def update_teams_to_date(last_updated: datetime):
    """
    Updates existing team data to the latest day given a last updated date
    :param last_updated: Python datetime representing the last time a set of team data was updated
    :return: A tuple containing a list of new events and updated team data as a dictionary of team numbers and team data
    """
    new_events = get_all_events(min_date=last_updated.date(), max_date=datetime.today().date())
    event_codes = [event.event_code for event in new_events]

    avg_total, avg_auto, avg_tele = get_start_avg()
    team_data = get_team_data_from_events(event_codes)

    for event in new_events:
        print(event.event_code)
        update_teams_at_event(event, team_data, avg_total, avg_auto, avg_tele)

    return new_events, team_data



def update_teams_at_event(event: Event, team_data: dict[int, Team], avg_total: float, avg_auto: float, avg_tele: float):
    """
    Update data for all teams using matches from given event code
    :param event: Event object to process
    :param team_data: Team data dictionary with existing statistics/matches. (Key = team_number, Value = team_object)
    :param avg_total: Starting season total average for EPA calculations
    :param avg_auto: Starting season auto average for EPA calculations
    :param avg_tele: Starting season TeleOp average for EPA calculations
    :return: None
    """
    season = get_config()['season']
    event_code = event.event_code
    team_number_list = event.team_list

    game_matrix = create_game_matrix(event_code, team_number_list)
    event_data: EventData = get_season_score_parser(season).parse(event_code)

    for team_number in team_number_list:
        # Process teams that don't exist yet
        if team_number not in team_data.keys():
            team = get_team_from_ftc(team_number)

            # Add starting averages to team data
            team.update_game_played("START")
            team.update_epa(avg_total, avg_auto, avg_tele)

            # Save to team data
            team_data[team_number] = team

    # Skip if the event has no games
    if len(game_matrix) <= 0: return team_data

    update_opr(team_number_list, game_matrix, event_data, team_data)
    update_epa(team_number_list, game_matrix, event_data, team_data)
    return None


def create_game_matrix(event_code: str, team_list: list[int]):
    """
    Calculates the game matrix, indicating which teams played in which matches
    :param event_code: Valid FIRST Event Code
    :param team_list: Valid list of teams from the event
    :return: The game matrix
    """
    season = get_config()['season']

    response = requests.get(
        f"http://ftc-api.firstinspires.org/v2.0/{season}/matches/" + event_code + "?tournamentLevel=qual", auth=get_auth())
    matches = response.json()['matches']  # only grab from qualifiers to equally compare all teams

    game_matrix = []

    # Add 1 to row at index where team number is in list
    for match in matches:
        red_alliances = [0] * len(team_list)
        blue_allainces = [0] * len(team_list)

        # for each match find if each team is on a red or blue alliance team
        for team in match['teams']:
            alliance = team['station']
            if alliance == 'Red1' or alliance == 'Red2':
                red_alliances[team_list.index(team['teamNumber'])] = 1
            else:
                blue_allainces[team_list.index(team['teamNumber'])] = 1

        game_matrix.append(red_alliances)
        game_matrix.append(blue_allainces)

    return game_matrix