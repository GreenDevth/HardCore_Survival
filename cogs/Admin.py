import asyncio
import json
import os
import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

from database.Admin_db import exclusive_lists
from database.Award import exp_process
from database.Bank_db import add_coins, remove_coins
from database.Member_db import verify_member, players, steam_to_info

load_dotenv()
admin = os.getenv('ADMIN')


def cmd_channel():
    with open('./config/config.json') as config:
        result = json.load(config)
        cmd = result["commands_channel"]
        return cmd


with open('./config/Server.json') as Roles:
    data = json.load(Roles)
    admin_role = data['roles']['admin']


class DiscordAdminCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='verify')
    @commands.has_role(admin)
    async def verify_command(self, ctx, member: discord.Member):

        verify = discord.utils.get(ctx.guild.roles, name='Verify Members')
        role = discord.utils.get(ctx.guild.roles, name='Joiner')
        member_id = players(member.id)[3]
        if int(member_id) == member.id:
            await ctx.reply(f'✅ {member.display_name} is verified', mention_author=False)
            if role in member.roles:
                await member.remove_roles(role)
                await member.add_roles(verify)
            elif role not in member.roles:
                await member.add_roles(verify)
            else:
                pass
            verified = verify_member(member.id)
            await discord.DMChannel.send(member, verified)
        else:
            await ctx.reply(f"{member_id} \n {member.id}")

    @verify_command.error
    async def verify_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply(error.args[0], mention_author=False)

    @commands.command(name='addcoins')
    @commands.has_role(admin)
    async def add_coins(self, ctx, coins, member: discord.Member):
        await ctx.reply(f"ทำการโอนเงินจำวน **{coins}** ให้กับ {member.display_name} สำเร็จ", mention_author=False)
        result = add_coins(member.id, coins)
        await discord.DMChannel.send(member, result)

    @add_coins.error
    async def add_coin_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply(error.args[0], mention_author=False)

    @commands.command(name='removecoins')
    @commands.has_role(admin)
    async def remove_coins(self, ctx, coins, member: discord.Member):
        await ctx.reply(f"ทำการหักเงินจำวน **{coins}** จาก {member.display_name} สำเร็จ", mention_author=False)
        result = remove_coins(member.id, coins)
        await discord.DMChannel.send(member, result)

    @remove_coins.error
    async def remove_coin_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply(error.args[0], mention_author=False)

    @commands.command(name='addexp')
    @commands.has_role(admin)
    async def add_exp(self, ctx, exp: int, member: discord.Member):
        await ctx.reply(f"ทำการเพิ่มค่าประสบการณ์จำนวน **{exp}** ให้กับ {member.display_name} สำเร็จ",
                        mention_author=False)
        result = exp_process(member.id, exp)
        await discord.DMChannel.send(member, result)

    @commands.command(name='id')
    async def id(self, ctx, *, user_id: int):
        user = discord.utils.get(self.bot.get_all_members(), id=user_id)
        if user is not None:
            await ctx.send(user)
        else:
            await ctx.send("**Try that again**, this time add a user's id(**of this server**)")


class ScumServerStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='server')
    @commands.has_role("Verify Members")
    async def server_command(self, ctx):
        response = requests.get("https://api.battlemetrics.com/servers/13458708")
        res_text = response.text
        json.loads(res_text)
        json_obj = response.json()
        scum_server = json_obj['data']['attributes']['name']
        scum_ip = json_obj['data']['attributes']['ip']
        scum_port = json_obj['data']['attributes']['port']
        scum_player = json_obj['data']['attributes']['players']
        scum_player_max = json_obj['data']['attributes']['maxPlayers']
        scum_rank = json_obj['data']['attributes']['rank']
        scum_status = json_obj['data']['attributes']['status']
        scum_time = json_obj['data']['attributes']['details']['time']
        scum_version = json_obj['data']['attributes']['details']['version']
        role = discord.utils.get(ctx.guild.roles, name="Admin")
        if ctx.channel.id == 925559937323659274 or role in ctx.author.roles:
            await ctx.reply(
                "📃 **SERVER INFORMATION DATA**"
                "```============================================="
                f"\nServer: {scum_server} "
                f"\nIP: {scum_ip}:{scum_port} "
                f"\nPWD: 7314412 "
                f"\nStatus: {scum_status} "
                f"\nTime in Game: {scum_time} "
                f"\nPlayers: {scum_player}/{scum_player_max} "
                f"\nRanking: #{scum_rank} "
                f"\nGame version: {scum_version}\n "
                f"\nServer Restarts Every 6 hours "
                f"\nDay 3.8 hours, Night 1 hours\n"
                f"=============================================```",
                mention_author=False
            )
        else:
            await ctx.reply("กรุณาพิมพ์คำสั่งนี้ที่้ห้อง <#925559937323659274> เท่านั้น", mention_author=False,
                            delete_after=5)
        await ctx.message.delete()

    @server_command.error
    async def server_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply('You have not verified your membership. Please visit <#878878305296728095>',
                            mention_author=False)
            await ctx.message.delete()

    @commands.command(name='steam')
    @commands.has_role(admin_role)
    async def check_steam_command(self, ctx, steam):
        """ Check Player by steam id"""
        info = steam_to_info(steam)
        name = info[0]
        discord_id = info[1]
        steam_id = info[2]
        message = f"```cs\nAccount : {discord_id}, Name : '{name}', Steam ID : {steam_id}\n```"
        await ctx.send(message)

    @check_steam_command.error
    async def check_steam_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply(error.args[0], mention_author=False)

    @commands.command(name='exclusive_list')
    @commands.has_role(admin_role)
    async def exclusive_list_command(self, ctx):
        exclusive_lists()
        await asyncio.sleep(1.5)
        await ctx.send(
            file=discord.File('./Exclusive/exclusive_data.csv')
        )

    @commands.command(name='players')
    @commands.has_permissions(manage_roles=True)
    async def player_command(self, ctx, member: discord.Member):

        player = players(member.id)
        player_coin = "${:,d}".format(player[6])

        def ign():
            player_ign = player[2]
            if player_ign is not None:
                return player_ign
            elif player_ign is None:
                return "ยังไม่ระบุ"

        msg = f"ID : {player[0]}\n" \
              f"NAME : '{player[1]}'\n" \
              f"IGN : '{ign()}'\n" \
              f"BANK ID : {player[5]}\n" \
              f"COIN : {player_coin}\n" \
              f"LEVEL : {player[7]}\n" \
              f"EXP : {player[8]}\n" \
              f"STATUS : '{player[9]}'"
        embed = discord.Embed(
            title=f'DATA INFORMATION OFF {player[1]}',
            colour=discord.Colour.green()
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(
            name='Player informaion',
            value=f"```cs\n{msg}\n```"
        )
        await ctx.reply(embed=embed, mention_author=False)

    @player_command.error
    async def player_command_error(self, ctx, error):
        msg = None
        if isinstance(error, commands.MissingPermissions):
            msg = error.args[0]
        await ctx.reply(msg)


def setup(bot):
    bot.add_cog(DiscordAdminCommand(bot))
    bot.add_cog(ScumServerStatus(bot))
