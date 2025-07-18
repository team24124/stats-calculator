class Team:
    def __init__(self, team_number, name, country, state_prov, city, home_region):
        self.team_number = team_number
        self.name = name

        # List of all matches played in consecutive order
        self.matches = []
        self.games_played = 0

        self.country = country
        self.state_prov = state_prov
        self.city = city
        self.home_region = home_region

        self.epa_total = 0
        self.epa_auto_total = 0
        self.epa_tele_total = 0
        self.historical_epa = []
        self.historical_auto_epa = []
        self.historical_tele_epa = []

        self.historical_opr = []
        self.historical_auto_opr = []
        self.historical_tele_opr = []
        self.historical_end_opr = []
        self.opr = 0
        self.opr_auto = 0
        self.opr_tele = 0
        self.opr_end = 0

    def update_game_played(self, match_name):
        self.matches.append(match_name)
        self.games_played += 1

    def update_epa(self, delta_epa, delta_epa_auto, delta_epa_tele):
        """
        Update all EPA values for current team object
        :param delta_epa: Calculated CHANGE in EPA
        :param delta_epa_auto: Calculated CHANGE in Auto EPA
        :param delta_epa_tele: Calculated CHANGE in TeleOp EPA
        :return: None
        """
        new_epa = self.epa_total + delta_epa
        self.epa_total = new_epa
        self.historical_epa.append(new_epa)

        new_epa_auto = self.epa_auto_total + delta_epa_auto
        self.epa_auto_total = new_epa_auto
        self.historical_auto_epa.append(new_epa_auto)

        new_epa_tele = self.epa_tele_total + delta_epa_tele
        self.epa_tele_total = new_epa_tele
        self.historical_tele_epa.append(new_epa_tele)


    def update_opr(self, opr_total, opr_auto, opr_tele, opr_end):
        """
        Update all OPR values for current team object
        :param opr_total: Calculated new total OPR
        :param opr_auto: Calculated new Auto OPR
        :param opr_tele: Calculated new TeleOp OPR
        :param opr_end: Calculated new Endgame OPR
        :return: None
        """
        self.historical_opr.append(float(opr_total))  # Connvert numpy floats to python floats
        self.historical_auto_opr.append(float(opr_auto))
        self.historical_tele_opr.append(float(opr_tele))
        self.historical_end_opr.append(float(opr_end))
        self.opr = float(opr_total)
        self.opr_auto = float(opr_auto)
        self.opr_tele = float(opr_tele)
        self.opr_end = float(opr_end)

    def __repr__(self):
        return f"Team #{self.team_number} | Games Played: {self.games_played} | EPA Total: {self.epa_total}"
