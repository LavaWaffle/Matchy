from subsystems.utils import *
from subsystems.Award import Award

class TeamTotalData:
    def __init__(self, team: str):
        self.team = team
        self.awards: list[Award] = []
        self.fetch_data()

    def fetch_data(self):
        data = get_data(f"https://www.thebluealliance.com/api/v3/team/frc{self.team}/awards")
        self.awards = [Award(award_data) for award_data in data]