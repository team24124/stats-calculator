"""
Run relevant tests or prototypes using this file.
"""
import datetime

from calculations import update_teams_to_date

if __name__ == '__main__':
    update_teams_to_date(datetime.datetime(2025, 7, 1, 0, 0, 0, 0))