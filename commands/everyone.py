from constants import *

NAME = "everyone"
DESCRIPTION = "owo"
SLASH_ONLY = True

async def run(ctx, message: ("The message", str)):
    if ctx.user.id in OWNER_IDS:
        await ctx.respond(f"@everyone: {message}", mentions_everyone=True)
    else:
        await ctx.respond(f"{ctx.author.mention}, you are not authorized to use this command")