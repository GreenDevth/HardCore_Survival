from discord.ext import commands


class DiscordStore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.bot.user.name + " has been online.")


def setup(bot):
    bot.add_cog(DiscordStore(bot))
