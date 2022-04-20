import os

import discord
from discord.ext import commands
from discord_components import DiscordComponents
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('HARDCORE')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!$', intents=intents)
DiscordComponents(bot)


@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.watching, name='Discord Mission'
        )
    )


if __name__ == '__main__':
    for filename in os.listdir('./quests'):
        if filename.endswith('.py'):
            bot.load_extension(f'quests.{filename[:-3]}')
    bot.run(token)
