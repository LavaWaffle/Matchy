from dotenv import dotenv_values
env_vars = dotenv_values('.env')

from bot_container import BotContainer
import lightbulb
import hikari

class Bot: 
    m_botContainer: BotContainer   
    def __init__(self):
        self.bot = lightbulb.BotApp(
            token=env_vars['DISCORD-BOT-TOKEN'],
            prefix="."
        )
        m_botContainer = BotContainer(self.bot)
        self.run()

    def run(self):
        self.bot.run()