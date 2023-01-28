from utils import *
from constants import *
from subsystems.Team import Team
import os
import time

NAME = "teamepa"
DESCRIPTION = "Graphs teams' EPA over the years"

async def run(ctx, teams: ("The team numbers to check, separated by commas", str)):
    if not os.path.exists(IMAGE_DIR):
        os.mkdir(IMAGE_DIR)
    try:
        teams = [Team(int(x.strip())) for x in teams.split(",")]
    except ValueError:
        await error(ctx, "Invalid team number!")
        return
    if len(teams) > len(TEAM_COLORS):
        await error(ctx, f"Please use at most {len(TEAM_COLORS)} teams!")
        return
    for team in teams:
        if team.data is None:
            await error(ctx, f"There is no team numbered {team.team_number}!")
            return
    year_set = set()
    for i, team in enumerate(teams):
        years, epas = [], []
        for year in range(team.rookie_year, time.localtime().tm_year + 1):
            year_data = get_team_year(team.team_number, year)
            if year_data is None: continue
            epa = year_data["norm_epa_end"]
            if epa is not None:
                years.append(year)
                epas.append(epa)
        line, = plt.plot(years, epas, "o-", color = TEAM_COLORS[i])
        line.set_label(f"Team {team.team_number}")
        year_set = year_set.union(set(years))
    cache.save()
    xlim = plt.gca().get_xlim()
    line, = plt.plot([0, 2 * years[-1]], [1500, 1500], "-", color = "#00ff00")
    line.set_label("Baseline")
    plt.xlim(xlim)
    plt.ylabel("EPA")
    plt.title(f"Team EPAs")
    plt.legend()
    plt.xticks(sorted(list(year_set)))
    plt.grid(which = "both", axis = "both", color = "#cccccc")
    ax = plt.gca()
    ax.set_xticklabels(ax.get_xticks(), rotation = 90)
    await send_plot(ctx, f"EPA data for teams {', '.join(str(i.team_number) for i in teams)}")