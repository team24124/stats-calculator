import numpy as np

from data.scores import EventData, MatchData
from teams.Team import Team


def get_epa_parameters(games_played: float):
    """
    Calculate the correct m and k EPA parameters
    :param games_played: Average number of games played by four teams
    :return: m and k values for EPA calculation
    """
    k = 0.33
    m = 0

    # Use the constant k = 0.33 to provide more stable epa results

    # if 6 < games_played <= 12:
    #     k = 0.33 - (games_played - 6) / 45
    # elif 12 < games_played <= 36:
    #     k = 0.2
    #     # m = (games_played - 12)/24 # Unchanged to make EPA reflect more offensive contributions
    # elif games_played > 36:
    #     k = 0.2
    #     # m = 1

    return m, k


def calculate_epa(red_epa: int,
                  blue_epa: int,
                  red_score: int,
                  blue_score: int,
                  games_played: float):
    """
    Calculate change in EPA for given teams given both alliances' final scores (order of teams does not matter)

    :param red_epa: Sum of score or scoring component EPA for red alliance
    :param blue_epa: SUm of score or scoring component EPA for blue alliance
    :param red_score: Score or scoring component for the red alliance
    :param blue_score: Score or scoring component for the blue alliance
    :param games_played: Average number of games played between all four teams
    :return: Tuple of the change in RED ALLIANCE's EPA, and the change in BLUE ALLIANCE's EPA
    """

    m, k = get_epa_parameters(games_played)

    delta_epa_red = k / (1 + m) * ((red_score - red_epa) - m * (blue_score - blue_epa))
    delta_epa_blue = k / (1 + m) * ((blue_score - blue_epa) - m * (red_score - red_epa))

    return delta_epa_red, delta_epa_blue

def update_epa(team_list: list[int], game_matrix: list[list[int]], event_data: EventData, team_data: dict[int, Team]):
    """
    Update EPA for all teams at an event for each match played at that event
    :param team_list: List of team numbers for teams at event
    :param game_matrix: Matrix of games played at the event
    :param event_data: Scoring data from the event
    :param team_data: Dictionary of teams where ALL teams must be present in the dictionary
    :return:
    """
    game_index = 0
    for i in range(0, len(game_matrix), 2):
        red_index = np.where(np.array(game_matrix[i]) == 1)[0]
        team1 = team_data[team_list[red_index[0]]]
        team2 = team_data[team_list[red_index[1]]]

        blue_index = np.where(np.array(game_matrix[i + 1]) == 1)[0]
        team3 = team_data[team_list[blue_index[0]]]
        team4 = team_data[team_list[blue_index[1]]]

        teams = [team1, team2, team3, team4]
        match_data: MatchData = event_data.matches[game_index]

        if match_data.get_match_name() in team1.matches:
            game_index += 1
            continue

        # Update number of games played
        team1.update_game_played(match_data.get_match_name())
        team2.update_game_played(match_data.get_match_name())
        team3.update_game_played(match_data.get_match_name())
        team4.update_game_played(match_data.get_match_name())

        games_played = (team1.games_played + team2.games_played + team3.games_played + team4.games_played) / 4

        # Extract relevant data to calculate epa
        red_score = match_data.red_alliance.total_score
        blue_score = match_data.blue_alliance.total_score
        red_epa = team1.epa_total + team2.epa_total
        blue_epa = team3.epa_total + team4.epa_total

        red_auto_score = match_data.red_alliance.auto_score
        blue_auto_score = match_data.blue_alliance.auto_score
        red_auto_epa = team1.epa_auto_total + team2.epa_auto_total
        blue_auto_epa = team3.epa_auto_total + team4.epa_auto_total

        red_tele_score = match_data.red_alliance.tele_score
        blue_tele_score = match_data.blue_alliance.tele_score
        red_tele_epa = team1.epa_tele_total + team2.epa_tele_total
        blue_tele_epa = team3.epa_tele_total + team4.epa_tele_total

        # Calculate each change
        change_red, change_blue = calculate_epa(red_epa, blue_epa,
                                                red_score, blue_score, games_played)
        change_red_auto, change_blue_auto = calculate_epa(red_auto_epa, blue_auto_epa,
                                                          red_auto_score, blue_auto_score, games_played)
        change_red_tele, change_blue_tele = calculate_epa(red_tele_epa, blue_tele_epa,
                                                          red_tele_score, blue_tele_score, games_played)
        # Update match and EPA for red alliance
        for j in range(0, 2):
            team = teams[j]
            team.update_epa(change_red, change_red_auto, change_red_tele)

        # Update match and EPA for blue alliance
        for j in range(2, 4):
            team = teams[j]
            team.update_epa(change_blue, change_blue_auto, change_blue_tele)

        game_index += 1