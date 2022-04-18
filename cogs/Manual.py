import discord
from discord.ext import commands


class DiscordTutorial(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='howto')
    async def howto_command(self, ctx):
        await ctx.send(
            "📔 **ขั้นตอนการลงทะเบียน**\n"
            "จากภาพด้านล่างให้ผู้เล่นกดที่ปุ่ม **ลงทะเบียน** โดยระบบจะ\n"
            "แจ้งให้ผู้เล่นกรอกรหัส Steam64 เพื่อเปิดบัญชีผู้เล่น จากนั้น\n"
            "ระบบจะส่งรหัสปลดล็อค 6 หลัก สำหรับใช้ปลดล๊อคการใช้\n"
            "งานExclusive Members และรอการแจ้งเตือนจากระบบ\n"
            "อีกครั้งเมื่อทีมงาน Verify สิทธิ์การใช้งานเซิร์ฟเวอร์เรียบร้อย\n",
            file=discord.File('./img/howto/register.png')

        )


def setup(bot):
    bot.add_cog(DiscordTutorial(bot))
