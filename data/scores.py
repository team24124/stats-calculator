from abc import abstractmethod


class AllianceScoreData:
    """
    Match Score representation for statistics calulcations
    """

    def __init__(self, total_score: int, auto_score: int, tele_score: int, end_score: int):
        """
        Construct new alliance scores from data
        :param total_score: Total score from the entire game
        :param auto_score: Score from the Autonomous period
        :param tele_score: Score from the TeleOp period
        :param end_score: Score from the Endgame period
        """
        self.total_score = total_score
        self.auto_score = auto_score
        self.tele_score = tele_score
        self.end_score = end_score


class MatchData:
    """
    Match representation for statistics calculations
    """

    def __init__(self, season: int, event_code: str, match_number: int, match_level: str, red_scores: AllianceScoreData,
                 blue_scores: AllianceScoreData):
        """
        Construct a new match using data
        :param season: Year of the season the match was played
        :param event_code: Event code of the match
        :param match_number: Qualification/Playoff number of the match
        :param match_level: Q if a qualification, P if a playoff
        :param red_scores: AllianceScoreData object for the red alliance
        :param blue_scores: ALlianceScoreData object for the blue alliance
        """
        self.season = season
        self.event_code = event_code
        self.match_number = match_number
        self.match_level = match_level
        self.red_alliance = red_scores
        self.blue_alliance = blue_scores

    def get_match_name(self):
        return f"{self.season}{self.event_code}{self.match_level}{self.match_number}"


class EventData:
    def __init__(self):
        self.matches = []
        self.total_match_scores = []
        self.auto_match_scores = []
        self.tele_match_scores = []
        self.end_match_scores = []

    def add(self, match: MatchData):
        self.matches.append(match)

        # Red alliance first as self-opposed convention
        self.total_match_scores.append(match.red_alliance.total_score)
        self.auto_match_scores.append(match.red_alliance.auto_score)
        self.tele_match_scores.append(match.red_alliance.tele_score)
        self.end_match_scores.append(match.red_alliance.end_score)

        # Followed by blue alliance
        self.total_match_scores.append(match.blue_alliance.total_score)
        self.auto_match_scores.append(match.blue_alliance.auto_score)
        self.tele_match_scores.append(match.blue_alliance.tele_score)
        self.end_match_scores.append(match.blue_alliance.end_score)


class SeasonScoreParser:
    @abstractmethod
    def parse(self, event_code) -> EventData:
        """
        Parse an event score data object given a valid FTC event code
        :param event_code: Valid FTC event code
        :return: List of all matches as MatchData
        """
        pass


def get_season_score_parser(season: int):
    """
    Get a valid score parser given the season
    :param season: FTC API season year
    :return: Valid score parser to process events
    """
    from data.parsers import IntoTheDeepScoreParser

    # noinspection PyUnreachableCode
    match season:
        case 2024:
            return IntoTheDeepScoreParser()
        case _:
            raise ValueError("The season you tried to look for does not have a designated score parser yet. "
                             "Make sure your desired year is correct or create and add a new season score parser")
