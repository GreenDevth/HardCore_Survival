import json

import discord
from discord.ext import commands
from database.Member_db import *

with open('./config/survival.json') as config:
    data = json.load(config)
    guild_id = data["guild_id"]
    join = data["join_channel"]
    leave = data["leave_channel"]


class MemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_channel = self.bot.get_channel(int(join))
        guild = self.bot.get_guild(int(guild_id))
        joiner = discord.utils.get(guild.roles, name='Joiner')
        if joiner not in member.roles:
            await member.add_roles(joiner)
        x = datetime.datetime.now()
        join_date = x.strftime("%d/%m/%Y %H:%M:%S")
        bank_id = str(member.id)[:5]
        player = member_check(member.id)

        if player != 0:
            result = welcome_back(member.id)
            await welcome_channel.send(f'{result} **{member.name}**')
            return
        else:
            joiner = join_server(member.id, member.name, bank_id, join_date)
            await welcome_channel.send(f'**{member.name}** {joiner}')
            return

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        check = member_check(member.id)
        leave_channel = self.bot.get_channel(int(leave))
        if check != 0:
            player_leave = leave_server(member.id)
            await leave_channel.send(f'{player_leave} **{member.name}**')
        else:
            await leave_channel.send(f'Good Bye **{member.name}**')


def setup(bot):
    bot.add_cog(MemberJoin(bot))
