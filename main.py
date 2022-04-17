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

bot = commands.Bot(command_prefix='.', intents=intents)
bot.remove_command('help')
DiscordComponents(bot)


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
