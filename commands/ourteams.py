from utils import *
from constants import *
from bs4 import BeautifulSoup
from subsystems.Team import Team
import requests
import time

NAME = "ourteams"
DESCRIPTION = "Lists teams we compete against in a given year"

async def run(
    ctx,
    year: ("The year to check", int) = time.localtime().tm_year,
    rank: ("Whether or not to rank by current EPA", bool) = False
):
    urls = [f"https://www.thebluealliance.com/event/{year}{event_key}"
            for event_key in EVENT_KEYS]
    out = []
    for url in urls:
        r = requests.get(url)
        if r.status_code != 200: continue
        soup = BeautifulSoup(r.content, features = "html.parser")
        title = soup.find(name = "h1").contents[0]
        team_names = soup.find_all(name = "div", attrs = {"class": "team-name"})
        team_names = [tn.find(name = "a").contents[::2] for tn in team_names]
        hiding = None
        if rank:
            teams = [Team(int(t[0])) for t in team_names]
            teams = sorted([team for team in teams if team.norm_epa],
                           key = lambda t: t.norm_epa, reverse = True)
            hiding = len(team_names) - len(teams)
            team_names = [[str(team.team_number), team.name] for team in teams]
        out.append(f"""
**Teams in {title}**{'' if hiding is None else f' (hiding {hiding} teams with unknown EPAs)'}:
{chr(10).join(f'`Team {str(number).rjust(4)}` {team_name}' + (' (us)' if number == str(OUR_TEAM) else '')
              for number, team_name in team_names)}
""".strip())
    embed = hikari.Embed(
        title = f"Teams faced in {year}"
                f"{' (ranked from highest to lowest EPA)' if rank else ''}",
        description = "\n\n".join(out),
        color = "#00ff00"
    )
    await ctx.respond(embed)