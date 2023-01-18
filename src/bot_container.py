import lightbulb
import hikari

from subsystems.stats import Stats

class BotContainer:
    bot: lightbulb.BotApp
    stats: Stats
    def __init__(self, bot: lightbulb.BotApp):
        self.bot = bot
        self.stats = Stats()

        @self.bot.command()
        @lightbulb.command("ping", "Prints pong")
        @lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
        async def ping(ctx: lightbulb.Context):
            await ctx.respond("pong")

        @self.bot.command()
        @lightbulb.option('team', 'The team you want', int)
        @lightbulb.command("team", "Gets a team's data")
        @lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
        async def team(ctx: lightbulb.Context):
            team_number = ctx.options.team
            try:
                team = self.stats.get_team(team_number)
                embed = hikari.Embed(
                    title=f"**{team.name} {team.team}**",
                    description="",
                    # description=f"**Wins:** {team.wins} \n **Losses:** {team.losses} \n **Ties:** {team.ties} \n **EPA:** {team.norm_epa}",
                    color="#77FF77"
                )
                embed.add_field("Wins", team.wins, inline=True)
                embed.add_field("Losses", team.losses, inline=True)
                embed.add_field("Ties", team.ties, inline=True)
                embed.add_field("EPA", team.norm_epa, inline=False)
                embed.add_field("Win rate", team.winrate, inline=True)
                await ctx.respond(embed)
            except UserWarning:
                embed = hikari.Embed(
                    title="Error",
                    description=f"An error occurred while getting data from team: **{team_number}**. \n ```{team['error']}```",
                    color="#FF5555"
                )
                await ctx.respond(embed)
                
        @self.bot.command()
        @lightbulb.option('team', 'The team you want', int)
        @lightbulb.command("history", "Gets a team's history")
        @lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
        async def history(ctx: lightbulb.Context):
            team_number = ctx.options.team
            try:
                team = self.stats.get_team(team_number)
                embed = hikari.Embed(
                    title=f"**{team.name} {team.team} History**",
                    description="",
                    # description=f"**Wins:** {team.wins} \n **Losses:** {team.losses} \n **Ties:** {team.ties} \n **EPA:** {team.norm_epa}",
                    color="#77FF77"
                )
                if team.country != None:
                    embed.add_field("Country", team.country, inline=True)
                if team.state != None:
                    embed.add_field("State", team.state, inline=True)
                if team.district != None:
                    embed.add_field("District", team.district, inline=True)
                if team.rookie_year != None:
                    embed.add_field("Rookie Year", team.rookie_year, inline=False)
                if team.active != None:
                    embed.add_field("Is Active", team.active, inline=True)
                await ctx.respond(embed)
            except UserWarning:
                embed = hikari.Embed(
                    title="Error",
                    description=f"An error occurred while getting data from team: **{team_number}**. \n ```{team['error']}```",
                    color="#FF5555"
                )
                await ctx.respond(embed)


