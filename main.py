from dotenv import dotenv_values
env_vars = dotenv_values('.env')
from subsystems.Team import Team

# testing
# t293 = Team('frc293', '2022')
# print(t293.getWinPercentage())

# discord bot stuff goes here
import lightbulb

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
    team_number = ctx.options.team # hi ty im just doing stuff to hide the api key rn lol
    team = Team('frc' + str(team_number), '2022')
    avg_score = team.getAverageScore()
    await ctx.respond(f"Team **{team_number}**'s average score is: {avg_score}")

# get github
@bot.command()
@lightbulb.command('source_code', "Gets github source code link")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def source_code(ctx: lightbulb.Context):
    github = "https://github.com/LavaWaffle/Waffle-Bot"
    await ctx.respond(f"Github: {github}")

bot.run()