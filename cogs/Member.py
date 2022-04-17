import asyncio
import json

import discord
from discord.ext import commands

from database.Bank_db import player_bank, discord_id, plus_coin, minus_coin
from database.Member_db import member_check, players

with open('./config/config.json') as config:
    data = json.load(config)
    reg = data["register_channel"]
    cmd = data["commands_channel"]


class ServerMembers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='bank')
    @commands.has_any_role("Verify Members", "Admin")
    async def bank_command(self, ctx):
        """ แสดงยอดเงินสะสมของผู้เล่น : Verify Members only"""
        role = discord.utils.get(ctx.guild.roles, name="Admin")
        if ctx.channel.id == cmd or role in ctx.author.roles:
            check = member_check(ctx.author.id)
            if check == 1:
                bank = player_bank(ctx.author.id)
                coin = "${:,d}".format(bank[2])
                embed = discord.Embed(
                    title="BANK STATEMENT",
                    color=discord.Colour.green()
                )
                embed.set_thumbnail(url=f'{ctx.author.avatar_url}')
                embed.add_field(name='Bank Account', value=f"```cs\n{bank[0]}\n```")
                embed.add_field(name='Bank ID', value=f"```cs\n{bank[1]}\n```")
                embed.add_field(name='Bank Balance', value=f"```cs\n{coin}\n```")
                await ctx.reply(
                    embed=embed,
                    mention_author=False)
            else:
                msg = f"You don't have a bank account on the discord server. visit <#{reg}> channel"
                await ctx.reply(msg.strip(), mention_author=False)
        else:
            msg = f"กรุณาพิมพ์คำสั่งที่ห้อง <#{cmd}> เท่านั้น"
            await ctx.reply(msg.strip(), mention_author=False, delete_after=5)
            await ctx.message.delete()

    @bank_command.error
    async def bank_command_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.reply(error.args[0], mention_author=False)

    @commands.command(name='dmbank')
    @commands.has_any_role("Verify Members", "Admin")
    async def dmbank_command(self, ctx):
        """ แสดงยอดเงินสะสมของผู้เล่น (ข้อความส่วนตัว) : Verify Members only"""
        role = discord.utils.get(ctx.guild.roles, name="Admin")
        if ctx.channel.id == cmd or role in ctx.author.roles:
            check = member_check(ctx.author.id)
            if check == 1:
                bank = player_bank(ctx.author.id)
                coin = "${:,d}".format(bank[2])
                embed = discord.Embed(
                    title="BANK STATEMENT",
                    color=discord.Colour.green()
                )
                embed.set_thumbnail(url=f'{ctx.author.avatar_url}')
                embed.add_field(name='Bank Account', value=f"```cs\n{bank[0]}\n```")
                embed.add_field(name='Bank ID', value=f"```cs\n{bank[1]}\n```")
                embed.add_field(name='Bank Balance', value=f"```cs\n{coin}\n```")
                await ctx.reply('อีกสักครู่คุณจะได้รับข้อความจากระบบ', mention_author=False)
                await discord.DMChannel.send(ctx.author, embed=embed)
            else:
                msg = f"You don't have a bank account on the discord server. visit <#{reg}> channel"
                await ctx.reply(msg.strip(), mention_author=False)
        else:
            msg = f"กรุณาพิมพ์คำสั่งที่ห้อง <#{cmd}> เท่านั้น"
            await ctx.reply(msg.strip(), mention_author=False, delete_after=5)
            await ctx.message.delete()

    @dmbank_command.error
    async def dmbank_command_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.reply(error.args[0], mention_author=False)

    @commands.command(name='transfer')
    @commands.has_any_role('Verify Members', 'Admin')
    async def transfer_command(self, ctx, coin: int, bank: int):
        """ โอนเงินระหว่างผู้เล่น : Verify Members only"""
        role = discord.utils.get(ctx.guild.roles, name="Admin")
        if ctx.channel.id == cmd or role in ctx.author.roles:
            check = member_check(ctx.author.id)
            if check == 1:

                receiver_id = discord_id(bank)
                if receiver_id is not None:
                    sender = player_bank(ctx.author.id)
                    if coin <= sender[2]:
                        receiver = player_bank(receiver_id)
                        user = await self.bot.fetch_user(receiver_id)  # get receiver member by id
                        msg = 'ระบบกำลังดำเนินการโอนเงินจำนวน ${:,d} ให้กับ {}'.format(coin, receiver[0])
                        await ctx.reply(msg, mention_author=False)
                        plus = plus_coin(receiver_id, coin, ctx.author.id)
                        await discord.DMChannel.send(user, plus)
                        minus = minus_coin(ctx.author.id, coin)
                        await discord.DMChannel.send(ctx.author, minus)
                        await asyncio.sleep(2)
                        if plus and minus is not None:
                            await ctx.channel.send(f'{ctx.author.mention} โอนเงินสำเร็จ',
                                                   mention_author=False, delete_after=5)
                        else:
                            await ctx.reply('เกิดข้อผิดพลาด กรุณาทำรายการใหม่อีกครั้ง')
                            return

                    elif sender[2] < coin:
                        await ctx.reply('ขออภัยเงินยอดของคุณไม่เพียงพอ')
                    else:
                        await ctx.reply('เกิดข้อผิดพลาด กรุณาทำรายการใหม่อีกครั้ง')
                        return

                elif receiver_id is None:
                    await ctx.reply('ไม่พบบัญชีผู้รับเงินปลายทาง กรุณาตรวจสอบอีกครั้ง')
                else:
                    await ctx.reply('เกิดข้อผิดพลาด กรุณาทำรายการใหม่อีกครั้ง')
                    return
            else:
                msg = f"ไม่พบข้อมูลของคุณในระบบ"
                await ctx.reply(msg.strip(), mention_author=False)
        else:
            msg = f"กรุณาพิมพ์คำสั่งที่ห้อง <#{cmd}> เท่านั้น"
            await ctx.reply(msg.strip(), mention_author=False, delete_after=5)
            await ctx.message.delete()

    @transfer_command.error
    async def transfter_command_error(self, ctx, error):
        msg = None
        if isinstance(error, commands.MissingAnyRole):
            msg = error.args[0]
        if isinstance(error, commands.MissingRequiredArgument):
            msg = error.args[0]
        await ctx.reply(msg.strip(), mention_author=False)

    @commands.command(name='player')
    @commands.has_any_role("Verify Members", "Admin")
    async def player_command(self, ctx):
        member = ctx.author

        role = discord.utils.get(ctx.guild.roles, name="Admin")
        if ctx.channel.id == cmd or role in ctx.author.roles:
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
                title='YOUR DATA INFORMATION',
                colour=discord.Colour.green()
            )
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(
                name='Player informaion',
                value=f"```cs\n{msg}\n```"
            )
            await ctx.reply(embed=embed, mention_author=False)
        else:
            msg = f"กรุณาพิมพ์คำสั่งที่ห้อง <#{cmd}> เท่านั้น"
            await ctx.reply(msg.strip(), mention_author=False, delete_after=5)
            await ctx.message.delete()

    @player_command.error
    async def player_command_error(self, ctx, error):
        msg = None
        if isinstance(error, commands.MissingAnyRole):
            msg = error.args[0]
        await ctx.reply(msg)


def setup(bot):
    bot.add_cog(ServerMembers(bot))
