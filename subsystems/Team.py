import statbotics, requests
from typing import Dict, Any, Optional
from copy import deepcopy
from bs4 import BeautifulSoup

sb = statbotics.Statbotics()


class Team:
    def __init__(self, team_number: int) -> None:
        self.__team_number = team_number
        try:
            self.__data: Optional[Dict[str, Any]] = sb.get_team(self.team_number)
            r = requests.get(f"https://www.thebluealliance.com/team/{self.team_number}")
            if r.status_code == 200:
                self.__soup: Optional[BeautifulSoup] = BeautifulSoup(r.content, features = "html.parser")
            else:
                self.__soup: Optional[BeautifulSoup] = None
        except UserWarning: self.__data: Optional[Dict[str, Any]] = None

    @property
    def team_number(self) -> int:
        return self.__team_number

    @property
    def data(self) -> Optional[Dict[str, Any]]:
        return deepcopy(self.__data)

    @property
    def soup(self) -> Optional[BeautifulSoup]:
        return self.__soup

    @property
    def name(self) -> str:
        return self.data["name"]

    @property
    def is_off_season(self) -> bool:
        return self.data["offseason"]

    @property
    def state(self) -> Optional[str]:
        return self.data["state"]

    @property
    def country(self) -> str:
        return self.data["country"]

    @property
    def district(self) -> str:
        return self.data["district"]

    @property
    def district_name(self) -> str:
        district = self.district
        if district == "chs": return "FIRST Chesapeake District"
        if district == "fim": return "FIRST In Michigan District"
        if district == "fit": return "FIRST In Texas District"
        if district == "fin": return "FIRST Indiana Robotics District"
        if district == "isr": return "FIRST Israel District"
        if district == "fma": return "FIRST Mid-Atlantic District"
        if district == "fnc": return "FIRST North Carolina District"
        if district == "ne":  return "New England District"
        if district == "ont": return "Ontario District"
        if district == "pnw": return "Pacific Northwest District"
        if district == "pch": return "Peachtree District"
        return "no district"

    @property
    def rookie_year(self) -> int:
        return self.data["rookie_year"]

    @property
    def is_active(self) -> bool:
        return self.data["active"]

    @property
    def norm_epa(self) -> float:
        return self.data["norm_epa"]

    @property
    def norm_epa_recent(self) -> float:
        return self.data["norm_epa_recent"]

    @property
    def norm_epa_mean(self) -> float:
        return self.data["norm_epa_mean"]

    @property
    def norm_epa_max(self) -> float:
        return self.data["norm_epa_max"]

    @property
    def wins(self) -> int:
        return self.data["wins"]

    @property
    def losses(self) -> int:
        return self.data["losses"]

    @property
    def ties(self) -> int:
        return self.data["ties"]

    @property
    def match_count(self) -> int:
        return self.data["count"]

    @property
    def win_rate(self) -> float:
        return self.data["winrate"]

    @property
    def full_wins(self) -> int:
        return self.data["full_wins"]

    @property
    def full_losses(self) -> int:
        return self.data["full_losses"]

    @property
    def full_ties(self) -> int:
        return self.data["full_ties"]

    @property
    def full_match_count(self) -> int:
        return self.data["full_count"]

    @property
    def full_win_rate(self) -> float:
        return self.data["full_winrate"]

    @property
    def icon_url(self) -> Optional[str]:
        if not self.soup: return None
        element = self.soup.find("img", {"class": "team-avatar"})
        if element is None: return None
        return element.get("src")