from dotenv import dotenv_values
from subsystems.Team import Team
import lightbulb
import hikari
import functools
import operator

# discord bot stuff goes here

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
        await ctx.respond(
            hikari.Embed(
                title = "Error",
                description = f"There is no team numbered {ctx.options.team_number}!",
                color = hikari.Color.from_hex_code("#ff0000")
            )
        )
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
@lightbulb.command("predict", "Compares two alliances and predicts the outcome")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def compare(ctx: lightbulb.Context) -> None:
    try:
        teams1 = [Team(int(x.strip())) for x in ctx.options.teams1.split(",")]
        teams2 = [Team(int(x.strip())) for x in ctx.options.teams2.split(",")]
    except ValueError:
        await ctx.respond(
            hikari.Embed(
                title = "Error",
                description = "Invalid team number!",
                color = hikari.Color.from_hex_code("#ff0000")
            )
        )
        return
    if len(teams1) != len(teams2):
        await ctx.respond(
            hikari.Embed(
                title = "Error",
                description = "The alliances have to have the same number of teams!",
                color = hikari.Color.from_hex_code("#ff0000")
            )
        )
        return
    for team in teams1 + teams2:
        if team.data is None:
            await ctx.respond(
                hikari.Embed(
                    title = "Error",
                    description = f"There is no team numbered {team.team_number}!",
                    color = hikari.Color.from_hex_code("#ff0000")
                )
            )
            return
        if team.norm_epa is None:
            await ctx.respond(
                hikari.Embed(
                    title = "Error",
                    description = f"Team {team.team_number} does not have a set EPA!",
                    color = hikari.Color.from_hex_code("#ff0000")
                )
            )
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

** Using geometric mean:**
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
    if ctx.user.id == 425618103062364160:
        message = ctx.options.message
        await ctx.respond(f"@everyone : {message}", mentions_everyone=True)
    else:
        await ctx.respond(f"{ctx.author.mention}, you are not authorized to use this command")


bot.run()
