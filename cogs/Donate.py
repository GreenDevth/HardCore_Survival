import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle
from database.Donate_db import *

now = datetime.now()
create_at = now.strftime("%H:%M:%S")


def create_donate_table():
    try:
        cxn = create_connection(db)
        cur = cxn.cursor()
        list_of_tabales = cur.execute("""
            SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='donate';
        """).fetchall()

        if not list_of_tabales:
            print('table not found')
        else:
            print('table found')

    except Error as e:
        print(e)


class ServerDonation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        create_donate_table()

    """ Create Donation Commands """

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        donate_btn = interaction.component.custom_id

    @commands.command(name='donate')
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


class DonateEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(ServerDonation(bot))
    bot.add_cog(DonateEvent(bot))
