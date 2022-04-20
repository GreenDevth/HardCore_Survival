import discord
from discord.ext import commands


class ServerInformation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info")
    @commands.has_permissions(manage_roles=True)
    async def info_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/info.png')
        )
        await ctx.send(
            "- อัตราการ spawn item เท่ากับ 3\n"
            "- จำกัดผู้เล่น 2 คน ต่อ 1 squad\n"
            "- ครอบครอง ธง ได้เพียง 1 ธง และวางระเบิดภายในเขตธงเท่านั้น\n"
            "- มีหุ่นยนต์ darmage 0.5 ซอมบี้ darmage 3\n"
            "- การเลือกเกิด Random 100 FP, Sector 200 FP, Shlter 50 FP\n"
            "- ไม่มีแผนที่ ไม่มีอาวุธจำหน่ายใน Outpost\n"
            "- Spawn ยานพาหนะ ตามจำนวนชนิด\n"
            "- ใช้การลงทะเบียเพื่อปรับสิทธิ์การใช้งานเซิร์ฟ\n"
            "- Server IP : 143.244.33.48:7102"
        )

def setup(bot):
    bot.add_cog(ServerInformation(bot))
