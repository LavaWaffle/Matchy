from utils import *
from constants import *

NAME = "clear-cache"
DESCRIPTION = "Clears the cache of data"
SLASH_ONLY = True

async def run(ctx):
    if ctx.user.id in OWNER_IDS:
        cache.clear()
        await ctx.respond("Cleared cache.")
    else:
        await ctx.respond(f"{ctx.author.mention}, you are not authorized to use this command.")