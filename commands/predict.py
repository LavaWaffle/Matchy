from subsystems.Team import Team
import hikari
import functools
import operator

NAME = "predict"
DESCRIPTION = "Compares two alliances and predicts the outcome"

async def run(
    ctx,
    teams1: ("Comma-separated list of team numbers on alliance #1", str),
    teams2: ("Comma-separated list of team numbers on alliance #2", str)
):
    try:
        teams1 = [Team(int(x.strip())) for x in teams1.split(",")]
        teams2 = [Team(int(x.strip())) for x in teams2.split(",")]
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