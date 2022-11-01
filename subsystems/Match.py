class Match:
    def __init__(self, data):
        self.__data = data

    def get_data_path(self, path, initial_data = None):
        if initial_data is None: initial_data = self.__data
        if isinstance(path, str): path = path.split()
        if len(path) == 0: return initial_data
        return self.get_data_path(path[1:], initial_data[path[0]])

    def score_of(self, team):
        return self.get_data_path(f"alliances {team} score")

    def total_score_of(self, team):
        return self.get_data_path(f"score_breakdown {team} totalPoints")

    def teams_of(self, team):
        return self.get_data_path(f"alliances {team} team_keys")

    @property
    def winning_alliance(self): return self.get_data_path("winning_alliance")