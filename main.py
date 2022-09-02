from dotenv import dotenv_values
env_vars = dotenv_values('.env')
from subsystems.Team import Team

# testing
# t293 = Team('frc293', '2022')
# print(t293.getWinPercentage())

# discord bot stuff goes here
import lightbulb
import hikari

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
    team = Team('frc' + str(team_number), '2022')
    
    if team.error:
        # an error occurred while getting the team's data
        embed = hikari.Embed(
            title = "Error", 
            description = f"An error occurred while getting data from **{team_number}**. \n ```{team.error_msg}```",
            color = "#FF5555"
        )
        await ctx.respond(embed)
    else:
        # no error occurred
        average_score = team.getAverageScore()
        embed = hikari.Embed(
            title = f"Team **{team_number}**'s average score was **{round(average_score, 2)}**", 
            description = "The average of all their matches from the most recent season.",
            color="#77FF77"
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
    if (ctx.user.id == 425618103062364160):
        message = ctx.options.message 
        await ctx.respond(f"@everyone : {message}", mentions_everyone=True)
    else:
        await ctx.respond(f"{ctx.author.mention}, you are not authorized to use this command")

bot.run()