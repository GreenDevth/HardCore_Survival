import asyncio
import random

import discord
import requests
from discord.ext import commands


def get_players():
    try:
        # res = requests.get(url, headers=head)
        response = requests.get('https://api.battlemetrics.com/servers/13458708')
        status = response.status_code
        if status == 200:
            print(response.json()['data']['attributes']['players'])
            player = response.json()['data']['attributes']['players']
            return player
        else:
            return 0
    except Exception as e:
        print(e)
        return 0


class CountMembers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} is online')
        while True:
            status_type = random.randint(0, 1)
            if status_type == 0:
                player = get_players()
                print(player)
                await self.bot.change_presence(
                    status=discord.Status.online,
                    activity=discord.Activity(type=discord.ActivityType.watching, name=f"ผู้รอดชีวิต {player}/20 คน"))
            else:
                player = get_players()
                print(player)
                await self.bot.change_presence(
                    status=discord.Status.online,
                    activity=discord.Activity(type=discord.ActivityType.watching, name=f'ผู้รอดชีวิต {player}/20 คน'))
            await asyncio.sleep(15)


def setup(bot):
    bot.add_cog(CountMembers(bot))
