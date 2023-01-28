NAME = "source_code"
DESCRIPTION = "Gets GitHub source code link"

async def run(ctx):
    github = "https://github.com/LavaWaffle/Matchy"
    await ctx.respond(f"Github: {github}")