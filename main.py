import asyncio
import os

import discord
from discord.ext import commands
from discord_components import DiscordComponents
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')
DiscordComponents(bot)


@bot.event
async def on_ready():
    print(bot.user.name + " has been connected to Discord server!")
    members = 0
    for guild in bot.guilds:
        members += guild.member_count - 1
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(type=discord.ActivityType.watching, name=f'{members} Discord members')
    )


@bot.command()
@commands.has_permissions(manage_roles=True)
async def clear(ctx, number: int):
    """คำสั่งสำหรับลบข้อความ Admin only"""
    await ctx.reply(f'**{number}** messages are being deleted.', mention_author=False)
    await asyncio.sleep(1.5)
    await ctx.channel.purge(limit=number + 2)


@clear.error
async def clear_error(ctx, error):
    msg = None
    if isinstance(error, commands.MissingPermissions):
        msg = f"{error.args[0]}"
    if isinstance(error, commands.MissingRequiredArgument):
        msg = f"{error.args[0]}"
    await ctx.reply(msg.strip(), mention_author=False)


if __name__ == '__main__':
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
    bot.run(token)
