import os
import tomllib
from pathlib import Path

from dotenv import load_dotenv
from datetime import datetime

from data.scores import get_season_score_parser


def get_auth():
    """
    Get the authentication header required for FIRST API calls from environment variables

    :return
        A tuple containing the username and token
    """
    load_dotenv()
    return os.getenv("API_USER"), os.getenv("API_TOKEN")


def get_config():
    file_path = '../config.toml'

    script_dir = Path(__file__).resolve().parent
    target_file_path = script_dir / file_path

    try:
        with open(target_file_path, 'rb') as file:
            config = tomllib.load(file)
        return config
    except FileNotFoundError:
        print(f"Error: File not found at {target_file_path}")
        return None
    except tomllib.TOMLDecodeError as e:
        print(f"Error parsing config TOML file: {e}")
        return None


def parse_score_data(season: int, event_code: str):
    """
    Obtain score data broken into components for a given event and season.
    :param season: A valid integer representing the season year
    :param event_code: A valid FIRST event code to draw events from
    :return:A list of MatchData objects containing scores broken into components
    """
    # Pulling a request for the scores with different parameters
    return get_season_score_parser(season).parse(event_code)


def parse_date(date: str):
    """
    Parse a datetime object using the postgres date format
    :return: datetime object
    """
    return datetime.strptime(date, '%a, %d %b %Y %H:%M:%S -0000')