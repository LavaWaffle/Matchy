from dotenv import dotenv_values

from subsystems.TeamTotalData import TeamTotalData
from subsystems.TeamYearData import TeamYearData
from subsystems.exceptions import *
import lightbulb
import hikari

# discord bot stuff goes here

env_vars = dotenv_values('.env')

bot = lightbulb.BotApp(
    token=env_vars['DISCORD-BOT-TOKEN'],
    prefix="."
)

sp_command = lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)

@bot.command()
@lightbulb.command("ping", "Prints pong")
@sp_command
async def ping(ctx: lightbulb.Context):
    await ctx.respond("pong")


@bot.command()
@lightbulb.option('team', 'The team you want', int)
@lightbulb.command("average_score", "Gets a team's average score over the season")
@sp_command
async def average_score(ctx: lightbulb.Context):
    team_number = ctx.options.team
    try:
        team = TeamYearData(str(team_number), '2022')
    except TeamFetchException as e:
        # an error occurred while getting the team's data
        error_msg = e.args[0]
        embed = hikari.Embed(
            title="Error",
            description=f"An error occurred while getting data from **{team_number}**. \n ```{error_msg}```",
            color="#FF5555"
        )
        await ctx.respond(embed)
    else:
        # no error occurred
        avg_score = team.average_score()
        embed = hikari.Embed(
            title=f"Team **{team_number}**'s average score was **{round(avg_score, 2)}**",
            description="The average of all their matches from the most recent season.",
            color="#77FF77"
        )
        await ctx.respond(embed)

@bot.command()
@lightbulb.option("team", "The team you want", int)
@lightbulb.command("awards", "Gets a list of a team's awards")
@sp_command
async def awards(ctx: lightbulb.Context):
    team_number = ctx.options.team
    try:
        team = TeamTotalData(str(team_number))
    except TeamFetchException as e:
        error_msg = e.args[0]
        embed = hikari.Embed(
            title = "Error",
            description = f"An error occurred while getting data from **{team_number}**. \n ```{error_msg}```",
            color = "#FF5555"
        )
        await ctx.respond(embed)
    else:
        output = "\n".join(f"{award.year}: {award.name}" for award in team.awards)
        embed = hikari.Embed(
            title = f"Awards for Team **{team_number}**",
            description = output,
            color = "#77FF77"
        ).add_field("Award count", f"{len(team.awards)}", inline = True)
        await ctx.respond(embed)

@bot.command()
@lightbulb.option('team', 'The team you want', int)
@lightbulb.command("percentages", "Gets a team's win, lose, and tie percentages over the season",
                   aliases=["win_percentage", "lose_percentage", "tie_percentage"])
@sp_command
async def percentages(ctx: lightbulb.Context):
    team_number = ctx.options.team
    try:
        team = TeamYearData(str(team_number), '2022')
    except TeamFetchException as e:
        # an error occurred while getting the team's data
        error_msg = e.args[0]
        embed = hikari.Embed(
            title="Error",
            description=f"An error occurred while getting data from **{team_number}**. \n ```{error_msg}```",
            color="#FF5555"
        )
        await ctx.respond(embed)
    else:
        # no error occurred
        percent = team.percentages()

        embed = (
            hikari.Embed(
                title=f"From all of Team **{team_number}**'s matches from the most recent season:",
                description="",
                color="#77FF77"
            )
            .add_field("Win percentage", f"{percent.win_percentage}%", inline=True)
            .add_field("Lose percentage", f"{percent.loss_percentage}%", inline=True)
            .add_field("Tie percentage", f"{percent.tie_percentage}%", inline=True)
        )
        await ctx.respond(embed)


# get github
@bot.command()
@lightbulb.command('source_code', "Gets GitHub source code link")
@sp_command
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
