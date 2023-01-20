from dotenv import dotenv_values
from subsystems.Team import Team
import lightbulb
import hikari

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
This team is in {(team_data.state + ' in ') if team_data.state is not None else ''}{team_data.country}.
Member of {team_data.district_name}
This team had their rookie year in {team_data.rookie_year}.
Wins: {team_data.full_wins} / Losses: {team_data.full_losses} / Ties: {team_data.full_ties}
Win rate: {team_data.full_win_rate * 100}% wins out of {team_data.full_match_count} games
EPA: {team_data.norm_epa} (average is 1500)
""".strip()
    embed = hikari.Embed(
        title = f"Team {team_data.team_number} {team_data.name}",
        description = description,
        color = hikari.Color.from_hex_code("#00ff00")
    )
    icon = team_data.icon_url
    if icon is not None: embed.set_thumbnail(icon)
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
    if ctx.user.id == 425618103062364160:
        message = ctx.options.message
        await ctx.respond(f"@everyone : {message}", mentions_everyone=True)
    else:
        await ctx.respond(f"{ctx.author.mention}, you are not authorized to use this command")


bot.run()
