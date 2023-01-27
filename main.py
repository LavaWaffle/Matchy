from dotenv import dotenv_values
from subsystems.Team import Team
from utils import *
from keep_alive import keep_alive
from bs4 import BeautifulSoup
import lightbulb
import hikari
import functools
import operator
import os
import statbotics
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import time
import requests

OUR_TEAM = 293
IMAGE_DIR = "images"
EVENT_KEYS = ["njski", "njrob"]

TEAM_COLORS = [
    "#000000",
    "#ff0000",
    "#0000ff",
    "#00ffff",
    "#ff00ff",
    "#cc00ff",
    "#ff8800",
    "#888888",
    "#44cc44"
]

if os.path.exists(IMAGE_DIR):
    for file in os.listdir(IMAGE_DIR):
        os.remove(os.path.join(IMAGE_DIR, file))


async def error(ctx, text):
    await ctx.respond(hikari.Embed(title = "Error", description = text, color = "#ff0000"))


sb = statbotics.Statbotics()

# discord bot stuff goes here

if IS_REPLIT:
    bot = lightbulb.BotApp(
        os.getenv("DISCORD-BOT-TOKEN"),
        prefix = "."
    )
    keep_alive()
else:
    env_vars = dotenv_values('.env')

    bot = lightbulb.BotApp(
        token=env_vars['DISCORD-BOT-TOKEN'],
        prefix="."
    )


@bot.command()
@lightbulb.command("ping", "Prints pong")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def ping(ctx: lightbulb.Context):
    await ctx.respond("pong")


@bot.command()
@lightbulb.option("team_number", "The team number", int)
@lightbulb.command("team", "Gets team information")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def team(ctx: lightbulb.Context) -> None:
    team_data = Team(ctx.options.team_number)
    if team_data.data is None:
        await error(ctx, f"There is no team numbered {ctx.options.team_number}!")
        return
    description = f"""
This team {'**IS**' if team_data.is_off_season else 'is **NOT**'} off season.
This team is in {(team_data.state + ' in ') if team_data.state is not None else ''}\
{team_data.country if team_data.country is not None else 'an unknown country'}.
Member of {team_data.district_name}
This team had their rookie year in {team_data.rookie_year if team_data.rookie_year is not None else 'an unknown year'}.
Wins: {team_data.full_wins} / Losses: {team_data.full_losses} / Ties: {team_data.full_ties}
Win rate: {str(team_data.full_win_rate * 100) + '%' if team_data.full_win_rate is not None else 'unknown'} \
wins out of {team_data.full_match_count} games
EPA: {team_data.norm_epa if team_data.norm_epa is not None else 'unknown'} (average is 1500)
""".strip()
    embed = hikari.Embed(
        title = f"Team {team_data.team_number} {team_data.name}",
        description = description,
        color = hikari.Color.from_hex_code("#00ff00")
    )
    icon = team_data.icon_url
    if icon is not None: embed.set_thumbnail(icon)
    await ctx.respond(embed)


@bot.command()
@lightbulb.option("teams2", "Comma-separated list of team numbers on alliance #2", str)
@lightbulb.option("teams1", "Comma-separated list of team numbers on alliance #1", str)
@lightbulb.command("predict", "Compares two alliances and predicts the outcome",
                   auto_defer = True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def compare(ctx: lightbulb.Context) -> None:
    try:
        teams1 = [Team(int(x.strip())) for x in ctx.options.teams1.split(",")]
        teams2 = [Team(int(x.strip())) for x in ctx.options.teams2.split(",")]
    except ValueError:
        await error(ctx, "Invalid team number!")
        return
    if len(teams1) != len(teams2):
        await error(ctx, "The alliances have to have the same number of teams!")
        return
    for team in teams1 + teams2:
        if team.data is None:
            await error(ctx, f"There is no team numbered {team.team_number}!")
            return
        if team.norm_epa is None:
            await error(ctx, f"Team {team.team_number} does not have a set EPA!")
            return
    arithmetic_mean = lambda teams: sum(team.norm_epa for team in teams) / len(teams)
    geometric_mean  = lambda teams: \
        functools.reduce(operator.mul, [team.norm_epa for team in teams], 1) ** (1 / len(teams))
    arith1 = arithmetic_mean(teams1)
    arith2 = arithmetic_mean(teams2)
    geo1 = geometric_mean(teams1)
    geo2 = geometric_mean(teams2)
    if geo1 > geo2:
        if not geo2:
            big_ratio = "N/a"
            small_ratio = 0
        else:
            big_ratio = geo1 / geo2
            small_ratio = geo2 / geo1
    else:
        if not geo1:
            big_ratio = "N/a"
            small_ratio = 0 if geo1 else "N/a"
        else:
            big_ratio = geo2 / geo1
            small_ratio = geo1 / geo2
    description = f"""
**Using arithmetic mean:**
Alliance #1 EPA: {round(arith1, 3)}
Alliance #2 EPA: {round(arith2, 3)}
Difference: {round(abs(arith1 - arith2), 3)}
Winner prediction: {'Alliance 1' if arith1 > arith2 else ('Alliance 2' if arith2 > arith1 else 'Exactly even')}

**Using geometric mean:**
Alliance #1 EPA: {round(geo1, 3)}
Alliance #2 EPA: {round(geo2, 3)}
Ratios: {round(big_ratio, 3)}, {round(small_ratio, 3)}
Winner prediction: {'Alliance 1' if geo1 > geo2 else ('Alliance 2' if geo2 > geo1 else 'Exactly even')}
""".strip()
    await ctx.respond(
        hikari.Embed(
            title = "Prediction",
            description = description,
            color = hikari.Color.from_hex_code("#00ff00")
        )
    )


@bot.command()
@lightbulb.option("year", "The year to plot", int)
@lightbulb.command("yearepa", "Plots the year's EPA data based on percentiles",
                   auto_defer = True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def yearepa(ctx: lightbulb.Context) -> None:
    if not os.path.exists(IMAGE_DIR):
        os.mkdir(IMAGE_DIR)
    try: data = sb.get_year(ctx.options.year)
    except UserWarning:
        await error(ctx, f"The EPA data for {ctx.options.year} does not exist.")
        return
    try: our_percentile = sb.get_team_year(OUR_TEAM, ctx.options.year)["country_epa_percentile"] * 100
    except UserWarning: our_percentile = None
    XS = np.array([0, 1, 5, 10, 25, 50, 75])
    KEYS = "epa_max epa_1p epa_5p epa_10p epa_25p epa_median epa_75p".split()
    PREFIXES = ["", "auto_", "teleop_"]
    COLORS = ["#000000", "#ff0000", "#0000ff"]
    NAMES = ["Overall", "Auto", "Teleop"]
    func = lambda x, a, b, c: a * x ** b + c
    for prefix, color, name in zip(PREFIXES, COLORS, NAMES):
        epa = np.array([data[prefix + x] for x in KEYS])
        if None in epa:
            await error(ctx, f"Could not fetch EPA data for {ctx.options.year}!")
            return
        popt, pcov = sp.optimize.curve_fit(func, XS, epa)
        model = lambda x: func(x, *popt)
        polyline = np.linspace(0, 100)
        plt.plot(XS, epa, "o", color=color)
        line, = plt.plot(polyline, model(polyline), color=color)
        line.set_label(name)
    plt.ylim(bottom=0)
    ylim = plt.gca().get_ylim()
    if our_percentile is not None:
        line, = plt.plot([our_percentile, our_percentile], [-1000, 10000], "--", color = COLORS[0])
        line.set_label(f"Team {OUR_TEAM}'s " + NAMES[0])
    plt.xlim([0, 100])
    plt.ylim(ylim)
    plt.legend()
    plt.xlabel("Percentile")
    plt.ylabel("EPA")
    plt.title(f"Year {ctx.options.year}'s EPA")
    plt.grid(which = "both", axis = "both", color = "#cccccc")
    await send_plot(ctx, f"EPA data for {ctx.options.year}")


@bot.command()
@lightbulb.option("teams", "The team numbers to check, separated by commas", str)
@lightbulb.command("teamepa", "Graphs teams' EPA over the years",
                   auto_defer = True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def teamepa(ctx: lightbulb.Context):
    if not os.path.exists(IMAGE_DIR):
        os.mkdir(IMAGE_DIR)
    try:
        teams = [Team(int(x.strip())) for x in ctx.options.teams.split(",")]
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
            try:
                year_data = sb.get_team_year(team.team_number, year)
                epa = year_data["norm_epa_end"]
                if epa is not None:
                    years.append(year)
                    epas.append(epa)
            except UserWarning:
                pass
        line, = plt.plot(years, epas, "o-", color = TEAM_COLORS[i])
        line.set_label(f"Team {team.team_number}")
        year_set = year_set.union(set(years))
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


@bot.command()
@lightbulb.option("rank", "Whether or not to rank by current EPA", bool, required = False, default = False)
@lightbulb.option("year", "The year to check", int, required = False, default = time.localtime().tm_year)
@lightbulb.command("ourteams", "Lists teams we compete against in a given year", auto_defer = True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def our_teams(ctx: lightbulb.Context):
    urls = [f"https://www.thebluealliance.com/event/{ctx.options.year}{event_key}"
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
        if ctx.options.rank:
            teams = [Team(int(t[0])) for t in team_names]
            teams = sorted([team for team in teams if team.norm_epa], key = lambda t: t.norm_epa, reverse = True)
            hiding = len(team_names) - len(teams)
            team_names = [[str(team.team_number), team.name] for team in teams]
        out.append(f"""
**Teams in {title}**{'' if hiding is None else f' (hiding {hiding} teams with unknown EPAs)'}:
{chr(10).join(f'`Team {str(number).rjust(4)}` {team_name}' + (' (us)' if number == str(OUR_TEAM) else '')
              for number, team_name in team_names)}
""".strip())
    embed = hikari.Embed(
        title = f"Teams faced in {ctx.options.year}"
                f"{' (ranked from highest to lowest EPA)' if ctx.options.rank else ''}",
        description = "\n\n".join(out),
        color = "#00ff00"
    )
    await ctx.respond(embed)


# get github
@bot.command()
@lightbulb.command('source_code', "Gets GitHub source code link")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def source_code(ctx: lightbulb.Context):
    github = "https://github.com/LavaWaffle/Matchy"
    await ctx.respond(f"Github: {github}")


@bot.command()
@lightbulb.option('message', 'The message', str)
@lightbulb.command('everyone', 'owo')
@lightbulb.implements(lightbulb.SlashCommand)
async def everyone(ctx: lightbulb.Context):
    print(str(ctx.user.id))
    if ctx.user.id in [425618103062364160, 708440911591243826]:
        message = ctx.options.message
        await ctx.respond(f"@everyone: {message}", mentions_everyone=True)
    else:
        await ctx.respond(f"{ctx.author.mention}, you are not authorized to use this command")


try: bot.run()
except (hikari.errors.HTTPResponseError, KeyError):
    if IS_REPLIT: os.system("kill 9")
    else: print("Please restart me")
