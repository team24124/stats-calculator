import requests
from data.scores import SeasonScoreParser, MatchData, AllianceScoreData, EventData


class IntoTheDeepScoreParser(SeasonScoreParser):
    def parse(self, event_code: str) -> EventData:
        from data import get_auth

        # Get the scoring data json from the FTC API
        response = requests.get(f"https://ftc-api.firstinspires.org/v2.0/2024/scores/" + event_code + "/qual",
                                auth=get_auth())  # only grab from qualifiers to equally compare all teams
        score_data = response.json()['matchScores']
        event_data = EventData()

        for match_score in score_data:
            match_level = 'q' if match_score['matchLevel'] == "QUALIFICATION" else "p"
            match_number = match_score['matchNumber']

            red_alliance = match_score['alliances'][1] # Red alliance is the second team in this year's API
            blue_alliance = match_score['alliances'][0]

            # Red alliance
            red_total_score = red_alliance['preFoulTotal']
            red_auto_score = red_alliance['autoPoints']
            red_teleop_score = red_alliance['teleopSamplePoints'] + red_alliance['teleopSpecimenPoints']
            red_endgame_score = red_alliance['teleopPoints'] - red_teleop_score

            red_alliane_scores = AllianceScoreData(red_total_score, red_auto_score,
                                                   red_teleop_score, red_endgame_score)

            # Then blue alliance
            blue_total_score = blue_alliance['preFoulTotal']
            blue_auto_score = blue_alliance['autoPoints']
            blue_teleop_score = blue_alliance['teleopSamplePoints'] + blue_alliance['teleopSpecimenPoints']
            blue_endgame_score = blue_alliance['teleopPoints'] - blue_teleop_score

            blue_alliance_scores = AllianceScoreData(blue_total_score, blue_auto_score,
                                                     blue_teleop_score, blue_endgame_score)

            # Create our match data object
            match_data = MatchData(
                2024,
                event_code,
                match_number,
                match_level,
                red_alliane_scores,
                blue_alliance_scores)

            # Add the match data to event data
            event_data.add(match_data)

        return event_data