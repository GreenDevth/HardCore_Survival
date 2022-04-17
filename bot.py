import asyncio
import json
import os

import discord
from discord.ext import commands
from discord_components import DiscordComponents

with open('./config/config.json') as config:
    data = json.load(config)
    token = data["token"]

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)
DiscordComponents(bot)

if __name__ == '__main__':
    for filename in os.listdir('./store'):
        if filename.endswith('.py'):
            bot.load_extension(f'store.{filename[:-3]}')
    bot.run(token)
