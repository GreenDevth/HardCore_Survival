from discord.ext import commands
from database.Store_db import create_table


class DiscordStore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.bot.user.name + " has been online.")
        create_table()


def setup(bot):
    bot.add_cog(DiscordStore(bot))
