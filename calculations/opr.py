import numpy as np

from data.scores import EventData
from teams.Team import Team


def calculate_opr(game_matrix: list[list[int]], event_data: EventData):
    """
    Calculate OPR for an event given the game matrix and event data object
    :param game_matrix: Matrix of games played at the event
    :param event_data: EventData object containing scores for each match
    :return: Tuple containing total, auto, tele and endgame opr for all teams according to the game matrix
    """
    total_opr = np.linalg.lstsq(game_matrix, event_data.total_match_scores)[0]
    auto_opr = np.linalg.lstsq(game_matrix, event_data.auto_match_scores)[0]
    tele_opr = np.linalg.lstsq(game_matrix, event_data.tele_match_scores)[0]
    end_opr = np.linalg.lstsq(game_matrix, event_data.end_match_scores)[0]

    return total_opr, auto_opr, tele_opr, end_opr


def update_opr(team_list: list[int], game_matrix: list[list[int]], event_data: EventData, team_data: dict[int, Team]):
    """
    Update the OPR for all teams at an event given the event code and a dictionary with the team data
    :param team_list: List of team numbers for teams at the event
    :param game_matrix: Matrix of games played at the event
    :param event_data: EventData object containing scores for each match at the event
    :param team_data: Dictionary that MUST have the team number and team object as a key and value
    :return: None
    """

    total_opr, auto_opr, tele_opr, end_opr = calculate_opr(game_matrix, event_data)

    for i in range(len(team_list)):
        team_number = team_list[i]  # Use team number from team list to get team
        team_obj = team_data[team_number]
        team_obj.update_opr(total_opr[i], auto_opr[i], tele_opr[i], end_opr[i])