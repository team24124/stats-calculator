from datetime import datetime, date
from data import get_config, get_season_score_parser
from data.scores import EventData
from events import get_all_events


def calculate_start_avg():
    """
    Calculates the start of the season average for use in EPA calculations
    :return: Average total score, average auto score, average teleop score
    """
    season = get_config()['season']

    max_date = date(season, 11, 30) # Set a max date to consider events
    events = get_all_events(max_date=max_date)

    num_scores = avg_total = avg_auto = avg_teleop = 0
    # Find the averages in the first number of events
    print(len(events))
    for event in events:
        print(event.event_code)
        event_code = event.event_code
        event_data: EventData = get_season_score_parser(season).parse(event_code)
        num_scores += len(event_data.matches) * 2 # Multiply the number of matches by two (to account for red AND blue alliances)
        avg_total += sum(event_data.total_match_scores)
        avg_auto += sum(event_data.auto_match_scores)
        avg_teleop += sum(event_data.tele_match_scores)

    avg_total /= num_scores
    avg_total /= 2

    avg_auto /= num_scores
    avg_auto /= 2

    avg_teleop /= num_scores
    avg_teleop /= 2

    return avg_total, avg_auto, avg_teleop


def get_start_avg():
    """
    :return: Average total score, average auto score, average teleop score for early events
    """
    config = get_config()

    # True if predetermined averages should be used or if a new average should be calculated at runtime
    use_predetermined: bool = config['averages']['use_predetermined']

    # Calculate average to use in EPA calculations
    if not use_predetermined:
        avg_total, avg_auto, avg_tele = calculate_start_avg()
    else:
        avg_total = config['averages']['total']
        avg_auto = config['averages']['auto']
        avg_tele = config['averages']['tele']

    return avg_total, avg_auto, avg_tele


if __name__ == '__main__':
    total, auto, tele = calculate_start_avg()
    print(f"""The following averages have been calculated:
    Total: {total}
    Auto: {auto}
    TeleOP: {tele}
    """)
