import matplotlib.pyplot as plt
import lightbulb
import hikari
import os
import random
import string
import statbotics
from subsystems.Cache import Cache


IS_REPLIT = os.getenv("IS-REPLIT")


def random_filename():
    while True:
        output = "".join(random.choice(string.ascii_letters) for i in range(10))
        if not os.path.exists("images") or not any(x.startswith(output) for x in os.listdir("images")):
            return output


async def send_plot(ctx: lightbulb.Context, title: str) -> None:
    path = os.path.join("images", random_filename() + ".png")
    plt.savefig(path)
    plt.clf()
    embed = hikari.Embed(
        title=title,
        color="#00ff00"
    )
    embed.set_image(hikari.File(path))
    await ctx.respond(embed)
    os.remove(path)

cache = Cache()

def get_team_year(team_number, year):
    key = f"teamyear/{team_number},{year}"
    if cache.is_outdated(key):
        try: cache[key] = sb.get_team_year(team_number, year)
        except UserWarning: cache[key] = None
    return cache[key]


async def error(ctx, text):
    await ctx.respond(hikari.Embed(title = "Error", description = text, color = "#ff0000"))


sb = statbotics.Statbotics()