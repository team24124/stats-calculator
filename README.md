# Nighthawks Stats Calculator
Standard Python modules used by Nighthawks Robotics teams to calculate OPR and EPA statistics for FIRST Tech Challenge teams.

`Powered by Python 3.12`

## Usage
1) Create a `.env` file in the main directory of this project.
2) Inside your `.env` file add your FIRST API username and password in the following format:
````
API_USER=[username]
API_TOKEN=[password]
````
3) From a command line interface in the project directory run `pip install -r requirements.txt`to install the required python dependencies.
4) Use `run.py` to debug, test and calculate statistics.

## Updating for New Seasons
In order to update the calculator for new seasons follow the following instructions:

Each season the specific ways of scoring differ and the API reflects this difference in the name/value pairs of it's responses. 
In order for our statistics to work we need to write a new class each season to parse these values and translate them into respective autonomous, teleop and endgame scoring components.

You can view how name/value pairs are formatted for each new season by navigating to:

```https://ftc-api.firstinspires.org/v2.0/2024/scores/[EVENT_CODE]/qual/```

replacing **[EVENT_CODE]** with a valid event code for the new season. 

Create a new season score parser: 
1) Navigate to `/data/parsers.py`
2) Create a new class that **inherits from the ``SeasonScoreParser`` class**
2) Create a new method `parse()` in the class that takes a new string **event_code** as an argument and returns a new EventData object
3) Following the existing parsers (_IntoTheDeepScoreParser_) format to create AllianceScoreData objects, MatchData objects and finally adding them to the EventData object

Reference the new score parser:
1) Navigate to `/data/scores.py`
2) Go to the `get_season_score_parser()` method
3) Add the new season to the match/case statement and return a new instance of your created season score parser


Update the config to the new season:
1) Navigate to `/config.toml`
2) Change the `season` value to your new season matching the value in the match/case statement