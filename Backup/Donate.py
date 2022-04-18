import asyncio
import json

import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle
from database.Donate_db import *

x = datetime.datetime.now()
create_date = x.strftime("%d/%m/%Y %H:%M:%S")

with open('./config/guild.json') as config:
    data = json.load(config)
    admin = data['roles']['admin']
    donate_room = data['roles']['donate_id']


class ServerDonation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """ Create Donation Commands """

    @commands.command(name='donate')
    @commands.has_role(admin)
    async def donate_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/donate/donate_t.png')
        )
        await ctx.send(
            "การสนับสนุนเซิร์ฟเป็นเพียงการช่วยเหลือค่าใช้จ่ายของเซิร์ฟ\n"
            "ผู้สนับสนุนจะไม่ได้อภิสิทธิ์ใดๆ นอกเหนื่อจากผู้เล่นคนอื่นๆ \n"
            "เว้นแต่จะได้รับการช่วยเหลือตามความจำเป็น และสิทธิ์ในการ\n"
            "เข้าใช้งานเซิร์ฟกรณีเซิร์ฟเต็ม\n"
        )
        await ctx.send(
            file=discord.File('./img/donate/donate.png'),
            components=[
                Button(style=ButtonStyle.red, label='สนับสนุนเซิร์ฟ', emoji='💳', custom_id='donate')
            ]
        )
        await ctx.message.delete()

    @donate_command.error
    async def donate_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply(error.args[0], mention_author=False)


class DonateEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        btn = interaction.component.custom_id

        if btn == 'donate':
            check = get_id(member.id)
            if check is None:
                room_create = new_donate_player(member.name, member.id)

            if check is not None:
                update_donate_date(member.id)

            current_channel = int(get_channel_id(member.id))
            channel_name = interaction.guild.get_channel(current_channel)
            if channel_name is None:
                await interaction.respond(content='โปรดรอสักครู่ระบบกำลังเปิดห้องให้กับคุณ')
                categorys = discord.utils.get(interaction.guild.categories, name="SERVER DONATION")
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False),
                    member: discord.PermissionOverwrite(read_messages=True)
                }
                """CREATE NEW ROW OR UPDATE EXISTS ROW"""
                room_id = get_id(member.id)
                new_channel = f'ห้องสนับสนุน-{int(room_id)}'
                await categorys.edit(overwrites=overwrites)
                await interaction.guild.create_text_channel(new_channel, category=categorys)
                channel = discord.utils.get(interaction.guild.channels, name=str(new_channel))
                update_room_id(member.id, channel.id)
                send_channel = interaction.guild.get_channel(channel.id)
                embed = discord.Embed(
                    title="ช่องทางสำหรับการสนับสนุนค่าใช้จ่ายเซิร์ฟ",
                    description="ชื่อบัญชี นายธีรพงษ์ บัวงาม",
                    color=discord.Colour.green(),
                )
                embed.add_field(name="บัญชีธนาคารกสิกรไทย", value="035-8-08192-4")
                embed.add_field(name="หมายเลข Promtpay", value="0951745515")
                await send_channel.send(
                    "**ช่องทางในการสนับสนุนค่าใช้จ่ายเซิร์ฟ**\n"
                    "\nชื่อบัญชี นายธีรพงษ์ บัวงาม ธนาคารกสิกรไทย"
                    "\nเลขที่ **035-8-08192-4**"
                    "\nหมายเลขพร้อมเพย์"
                    "\n**0951745515**"
                )
                await send_channel.send(
                    file=discord.File('./img/donate/upload_img.png'),
                    components=[
                        Button(style=ButtonStyle.blue, label='อัพโหลดสลิป', emoji='📸', custom_id='donate_img')]
                )
                await interaction.channel.send(f'ไปยังห้องของคุณ <#{channel.id}>', delete_after=5)

            elif channel_name is not None:
                await interaction.respond(content=f'ไปยังห้องของคุณ <#{current_channel}>')

        if btn == 'donate_img':
            donate = self.bot.get_channel(int(donate_room))
            await interaction.respond(content='กรุณาอัพโหลดสลิปของคุณ')

            def check(res):
                attachments = res.attachments
                if len(attachments) == 0:
                    return False
                attachment = attachments[0]
                file_type = attachment.filename.endswith(('.jpg', '.png', 'jpeg'))
                return res.author == interaction.author and res.channel == interaction.channel and file_type

            msg = await self.bot.wait_for('message', check=check)
            if msg is not None:
                await interaction.channel.send(f'{member.mention}\nขอบคุณสำหรับการสนับสนุนเซิร์ฟในครั้งนี้',
                                               delete_after=10)
            image = msg.attachments[0]
            embed = discord.Embed(
                title=f'ผู้สนับสนุนเซิร์ฟ {member.name}',
                description='ขอขอบคุณเป็นอย่างยิ่งสำหรับการสนับสนุนค่าใช้จ่ายเซิร์ฟในครั้งนี้ ',
                color=discord.Colour.green(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=f'{member.name}', icon_url=member.avatar_url)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_image(url=image)
            embed.add_field(name='ผู้สนับสนุนเซิร์ฟ', value=member.mention, inline=False)
            owner = interaction.guild.get_member(499914273049542677)
            await discord.DMChannel.send(owner, embed=embed)
            send = await interaction.channel.send(embed=embed, delete_after=10)
            await send.add_reaction("😍")
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(read_messages=False)
            }
            await interaction.channel.edit(overwrites=overwrites)
            await donate.send(embed=embed)
            await asyncio.sleep(10)
            await msg.delete()


def setup(bot):
    bot.add_cog(ServerDonation(bot))
    bot.add_cog(DonateEvent(bot))
