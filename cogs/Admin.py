import json

import discord
import requests
from discord.ext import commands, tasks

from database.Award import exp_process
from database.Bank_db import add_coins, remove_coins
from database.Member_db import verify_member, players, player_award

with open('./config/guild.json') as config:
    data = json.load(config)
    admin = data['roles']['admin']


class DiscordAdminCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='verify')
    @commands.has_role(admin)
    async def verify_command(self, ctx, member: discord.Member):

        verify = discord.utils.get(ctx.guild.roles, name='Verify Members')
        role = discord.utils.get(ctx.guild.roles, name='Joiner')
        member_name = players(member.id)[1]
        if member_name == member.name:
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
        player = player_award(member.id)
        await ctx.reply(f"ทำการเพิ่มค่าประสบการณ์จำนวน **{exp}** ให้กับ {member.display_name} สำเร็จ",
                        mention_author=False)
        result = exp_process(member.id, exp)
        await discord.DMChannel.send(member, result)

    @commands.command(name='id')
    async def id(self, ctx, *, user_id: int, steam, bank, coins, ):
        user = discord.utils.get(self.bot.get_all_members(), id=user_id)
        if user is not None:
            # Found the user
            await ctx.send(user)
        else:
            # Can't find the user
            await ctx.send("**Try that again**, this time add a user's id(**of this server**)")


class ScumServerStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_presence.start()

    @tasks.loop(seconds=15)
    async def change_presence(self):
        def get_players():
            try:
                response = requests.get('https://api.battlemetrics.com/servers/13458708')
                status = response.status_code
                if status == 200:
                    print(response.json()['data']['attributes']['players'])
                    player = response.json()['data']['attributes']['players']
                    msg = f"{player}/20 Prisoner"
                    return msg.strip()
                elif status != 200:
                    msg = "stay offline"
                    return msg.strip()
                else:
                    msg = "wait for online"
                    return msg.strip()
            except Exception as e:
                print(e)
                return 0

        result = get_players()
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(type=discord.ActivityType.watching, name=result)
        )

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


def setup(bot):
    bot.add_cog(DiscordAdminCommand(bot))
    bot.add_cog(ScumServerStatus(bot))
