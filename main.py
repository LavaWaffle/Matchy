from dotenv import dotenv_values
from subsystems.Team import Team
from subsystems.exceptions import *
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
@lightbulb.option('team', 'The team you want', int)
@lightbulb.command("average_score", "Gets a team's average score over the season")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def average_score(ctx: lightbulb.Context):
    team_number = ctx.options.team
    try:
        team = Team('frc' + str(team_number), '2022')
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
        avg_score = team.get_average_score()
        embed = hikari.Embed(
            title=f"Team **{team_number}**'s average score was **{round(avg_score, 2)}**",
            description="The average of all their matches from the most recent season.",
            color="#77FF77"
        )
        await ctx.respond(embed)


@bot.command()
@lightbulb.option('team', 'The team you want', int)
@lightbulb.command("percentages", "Gets a team's win, lose, and tie percentages over the season",
                   aliases=["win_percentage", "lose_percentage", "tie_percentage"])
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def percentages(ctx: lightbulb.Context):
    team_number = ctx.options.team
    try:
        team = Team('frc' + str(team_number), '2022')
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
        percent = team.get_percentages()

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
