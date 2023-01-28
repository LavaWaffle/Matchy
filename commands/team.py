from subsystems.Team import Team
import hikari

NAME = "team"
DESCRIPTION = "Gets team information"

async def run(ctx, team_number: ("The team number", int)):
    team_data = Team(team_number)
    if team_data.data is None:
        await error(ctx, f"There is no team numbered {team_number}!")
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