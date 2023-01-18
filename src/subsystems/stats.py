import statbotics

from classes.team import Team

class Stats:
    sb = None
    def __init__(self):
        self.sb = statbotics.Statbotics()

    def get_team(self, team_num: int):
        try:
            return Team(self.sb.get_team(team_num))
        except UserWarning:
            raise UserWarning(f"Team {team_num} not found")