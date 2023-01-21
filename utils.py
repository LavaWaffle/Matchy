import matplotlib.pyplot as plt
import lightbulb
import hikari
import os
import random
import string


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