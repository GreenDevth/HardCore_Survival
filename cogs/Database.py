from discord.ext import commands


class DatabaseManage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(DatabaseManage(bot))
