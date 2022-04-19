from discord.ext import commands


class DatabaseManage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('ok')


def setup(bot):
    bot.add_cog(DatabaseManage(bot))
