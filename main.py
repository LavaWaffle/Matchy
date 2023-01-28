from dotenv import dotenv_values
from utils import *
from constants import *
from keep_alive import keep_alive
import commands
import lightbulb
import hikari
import os
import inspect

if os.path.exists(IMAGE_DIR):
    for file in os.listdir(IMAGE_DIR):
        os.remove(os.path.join(IMAGE_DIR, file))

# discord bot stuff goes here

if IS_REPLIT:
    bot = lightbulb.BotApp(
        os.getenv("DISCORD-BOT-TOKEN"),
        prefix = "."
    )
    keep_alive()
else:
    env_vars = dotenv_values('.env')

    bot = lightbulb.BotApp(
        token=env_vars['DISCORD-BOT-TOKEN'],
        prefix="."
    )


def make_command(cmd, decorators, options):
    async def wrapper(ctx: lightbulb.Context):
        await cmd.run(ctx, *[getattr(ctx.options, option) for option in options])
    for decorator in decorators:
        wrapper = decorator(wrapper)


for pcmd in dir(commands):
    cmd = getattr(commands, pcmd)
    if not hasattr(cmd, "run"): continue
    impl = lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
    if getattr(cmd, "SLASH_ONLY", False):
        impl = lightbulb.implements(lightbulb.SlashCommand)
    decorators = [
        impl,
        lightbulb.command(cmd.NAME, cmd.DESCRIPTION, auto_defer = True)
    ]
    args = list(inspect.signature(cmd.run).parameters.values())[1:]
    for arg in args:
        these_args = [arg.name, arg.annotation[0], arg.annotation[1]]
        these_kwargs = {}
        if arg.default != inspect._empty:
            these_kwargs["required"] = False
            these_kwargs["default"] = arg.default
        decorators.append(lightbulb.option(*these_args, **these_kwargs))
    decorators.append(bot.command())
    make_command(cmd, decorators, [arg.name for arg in args])

try: bot.run()
except (hikari.errors.HTTPResponseError, KeyError):
    if IS_REPLIT: os.system("kill 9")
    else: print("Please restart me")