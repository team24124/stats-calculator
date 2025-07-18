import json
import traceback

from teams.Team import Team


def flatten_team_data(team):
    return {
        'team_number': team.team_number,
        'team_name': team.name,
        'country': team.country,
        'state_prov': team.state_prov,
        'city': team.city,
        'home_region': team.home_region,

        'games_played': team.games_played,
        'matches': team.matches,

        'epa_total': team.epa_total,
        'auto_epa_total': team.epa_auto_total,
        'tele_epa_total': team.epa_tele_total,
        'historical_epa': team.historical_epa,
        'historical_auto_epa': team.historical_auto_epa,
        'historical_tele_epa': team.historical_tele_epa,

        'opr': team.opr,
        'opr_auto': team.opr_auto,
        'opr_tele': team.opr_tele,
        'opr_end': team.opr_end,
        'historical_opr': team.historical_opr,
        'historical_auto_opr': team.historical_auto_opr,
        'historical_tele_opr': team.historical_tele_opr,
        'historical_end_opr': team.historical_end_opr,
    }

def export_team_data(team_data: dict[int, Team], path):
    json_data = {team_number: flatten_team_data(team) for team_number, team in team_data.items()}

    # Save to file
    if path:
        try:
            with open(path, "w") as f:
                json.dump(json_data, f, indent=2)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)