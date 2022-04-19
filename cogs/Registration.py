import asyncio
import datetime
import json
import random

import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle

from database.Member_db import steam_check, update_steam_id, member_check, \
    join_server, verify_check, activate_code_check, activate_code, players, update_activate_code

with open('./config/config.json') as config:
    data = json.load(config)
    exclusive = data["exclusive_channel"]
    register = data["register_channel"]


def generate_code(length):
    string_code = 'reallysurvival'
    result = ''.join((random.choice(string_code)) for x in range(length))
    return result.upper()


class RegistartionMember(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='reg')
    @commands.has_permissions(manage_roles=True)
    async def reg_command(self, ctx):
        """เปิดใช้งานปุ่มคำสั่งลงทะเบียนสำหรับผู้เล่น Admin only"""
        await ctx.send(
            "📔 **ขั้นตอนการลงทะเบียน**\n"
            "จากภาพด้านล่างให้ผู้เล่นกดที่ปุ่ม **ลงทะเบียน** โดยระบบจะ\n"
            "แจ้งให้ผู้เล่นกรอกรหัส **Steam64** เพื่อเปิดบัญชีผู้เล่น จากนั้น\n"
            "ระบบจะส่งรหัสปลดล็อค **6** หลัก สำหรับใช้ปลดล๊อคการใช้\n"
            "งาน **Exclusive Members** และรอการแจ้งเตือนจากระบบอีกครั้ง\n"
            "เมื่อทีมงานปรับสิทธิ์การเข้าใช้งานเซิร์ฟเวอร์ให้เรียบร้อย\n",
            file=discord.File('./img/register_new.png'),
            components=[
                [
                    Button(style=ButtonStyle.gray, label='ลงทะเบียน', emoji='📝', custom_id='new_player'),
                    Button(style=ButtonStyle.gray, label='ปลดล๊อคการใช้งาน', emoji='🔓', custom_id='activate_player'),
                    Button(style=ButtonStyle.gray, label='ขอรหัสใหม่', custom_id='new_code')
                ]
            ]
        )
        await ctx.message.delete()


class RegistrationEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        btn = interaction.component.custom_id
        btn_list = [
            "new_player",
            "activate_player",
            "new_code"
        ]

        if btn in btn_list:
            if btn == btn_list[0]:

                if member_check(member.id) == 0:
                    x = datetime.datetime.now()
                    join_date = x.strftime("%d/%m/%Y %H:%M:%S")
                    bank_id = str(member.id)[:5]
                    join_server(member.id, member.name, bank_id, join_date)
                    await interaction.send(f'{member.mention} : 📝 โปรดระบุ SteamID ของคุณเพื่อดำเนินการลงทะเบียน')
                    while True:
                        try:
                            msg = await self.bot.wait_for(
                                'message',
                                check=lambda r: r.author == interaction.author and r.channel == interaction.channel,
                                timeout=300
                            )
                            if msg.content.isdigit():
                                a_string = str(msg.content)
                                length = len(a_string)
                                if length != 17:
                                    print(length != 17)
                                    await interaction.channel.send(
                                        f'{member.mention} : 📢 รูปแบบสตรีมไอดีของคุณไม่ถูกต้องกรุณาลองใหม่อีกครั้ง',
                                        delete_after=3)
                                    await msg.delete()
                                else:
                                    activatecode = generate_code(6)
                                    update_steam_id(member.id, msg.content, activatecode)
                                    await interaction.channel.send(
                                        "🎉 ยินดีต้อนรับอย่างเป็นทางการสู่สังคม Really survival - Hardcore version ",
                                        delete_after=5)
                                    embed = discord.Embed(
                                        title="รหัสปลดล๊อคสำหรับสมัครใช้งาน Exclusive Membes",
                                        description="กรุณากดที่ปุ่ม ACTIVATE MEMBER และกรอกรหัสปลดล็อค 6 หลัก",
                                    )
                                    embed.add_field(name='รหัสปลดล็อค', value=f"```cs\n{activatecode}\n```")
                                    embed.add_field(name='ห้องลงทะเบียน', value=f'<#{register}>')
                                    embed.set_image(
                                        url="https://cdn.discordapp.com/attachments/894251225237848134"
                                            "/961097333876097034/unknown.png")
                                    await discord.DMChannel.send(
                                        member,
                                        embed=embed
                                    )
                                    await msg.delete()
                                    return
                            else:
                                await interaction.channel.send('oh no.', delete_after=3)
                                await msg.delete()
                        except asyncio.TimeoutError:
                            await interaction.send(f'{member.mention} : 📢 คุณใช้เวลาในการลงทะเบียนนานเกินไป '
                                                   f'กรุณาลงทะเบียนใหม่อีกครั้ง')
                elif member_check(member.id) == 1:
                    steam_id = steam_check(member.id)
                    if steam_id is not None:
                        verify = discord.utils.get(interaction.guild.roles, name='Verify Members')
                        embed = discord.Embed(
                            title='คุณได้ลงทะเบียนไว้เรียบร้อยแล้ว',
                            colour=discord.Colour.green()
                        )
                        embed.set_thumbnail(url=member.avatar_url)
                        embed.add_field(name='สตรีมไอดีของคุณ', value=f"```cs\n{steam_id}\n```")
                        embed.add_field(name='status', value='```cs\n🟢\n```')
                        await interaction.respond(embed=embed)
                        if verify not in member.roles:
                            code = activate_code_check(member.id)
                            await discord.DMChannel.send(member, f"โปรดใช้รหัสนี้ **{code}** ปลดล็อคการใช้งานของคุณ")
                            # await member.add_roles(verify)
                        else:
                            pass
                    else:
                        await interaction.send(f'{member.mention} : 📝 โปรดระบุ SteamID ของคุณเพื่อดำเนินการลงทะเบียน')

                        def check(m: discord.Message):
                            return m.author.id == interaction.author.id and m.channel.id == interaction.channel.id

                        while True:
                            try:
                                msg = await self.bot.wait_for(
                                    'message',
                                    check=check, timeout=15
                                )
                                if msg.content.isdigit():
                                    a_string = str(msg.content)
                                    length = len(a_string)
                                    if length != 17:
                                        print(length != 17)
                                        await interaction.channel.send(
                                            f'{member.mention} : 📢 รูปแบบสตรีมไอดีของคุณไม่ถูกต้องกรุณาลองใหม่อีกครั้ง',
                                            delete_after=3)
                                        await msg.delete()
                                    else:
                                        activatecode = generate_code(6)
                                        update_steam_id(member.id, msg.content, activatecode)
                                        await interaction.channel.send(
                                            "🎉 ยินดีต้อนรับอย่างเป็นทางการสู่สังคม ChangThai℠ Really survival ",
                                            delete_after=5)
                                        embed = discord.Embed(
                                            title="รหัสปลดล๊อคสำหรับสมัครใช้งาน Exclusive Membes",
                                            description="กรุณากดที่ปุ่ม ACTIVATE MEMBER และกรอกรหัสปลดล็อค 6 หลัก",
                                        )
                                        embed.add_field(name='รหัสปลดล็อค', value=f"```cs\n{activatecode}\n```")
                                        embed.add_field(name='ห้องลงทะเบียน', value=f'<#{register}>')
                                        embed.set_image(
                                            url="https://cdn.discordapp.com/attachments/894251225237848134"
                                                "/961097333876097034/unknown.png")
                                        await discord.DMChannel.send(
                                            member,
                                            embed=embed
                                        )
                                        await msg.delete()
                                        return
                                else:
                                    await interaction.channel.send(
                                        '📢 รูปแบบสตรีมไอดีของคุณไม่ถูกต้องกรุณาลองใหม่อีกครั้ง',
                                        delete_after=3
                                    )
                                    await msg.delete()
                            except asyncio.TimeoutError:
                                await interaction.send(
                                    f'{member.mention} :'
                                    f' 📢 คุณใช้เวลาในการลงทะเบียนนานเกินไป กรุณาลงทะเบียนใหม่อีกครั้ง')
            if btn == btn_list[1]:
                if member_check(member.id) == 1:
                    steamd_id = steam_check(member.id)
                    if steamd_id is not None:
                        check = verify_check(member.id)

                        def player_ign():
                            ign = players(member.id)[2]
                            if ign is not None:
                                return ign
                            elif ign is None:
                                message = "ยังไม่ระบุชื่อตัวละคร"
                                return message.strip()

                        if check == 1:
                            img = "https://cdn.discordapp.com/attachments/941531376363126814/964896802274967622" \
                                  "/unknown.png "
                            embed = discord.Embed(
                                title='คุณเป็นสมาชิก Exclusive Members แล้ว',
                                colour=discord.Colour.green()
                            )
                            embed.set_thumbnail(url=member.avatar_url)
                            embed.set_image(url=img)
                            embed.add_field(name='IGN', value='```cs\n{}\n```'.format(player_ign()))
                            embed.add_field(name='SteamID', value='```cs\n{}\n```'.format(steam_check(member.id)))
                            await interaction.respond(embed=embed)
                        elif check == 0:
                            await interaction.respond(
                                content='กรุณากรอก **รหัสปลดล็อค** ที่ได้จากเซิร์ฟเวอร์'
                            )

                            def check(m):
                                return m.author == interaction.author and m.channel.id == interaction.channel.id
                            while True:
                                try:
                                    msg = await self.bot.wait_for('message', check=check, timeout=30)
                                    check = activate_code_check(member.id)
                                    if msg.content == check:
                                        await msg.delete()
                                        exclusive_channel = self.bot.get_channel(exclusive)
                                        result = activate_code(check)
                                        steam = steam_check(member.id)
                                        await exclusive_channel.send(
                                            f"📃 **Exclusive Member {member.mention}**\n"
                                            "```=====================================\n"
                                            f"ผู้ลงทะเบียน : {member.display_name}\n"
                                            f"ดิสคอร์ดไอดี : {member.id}\n"
                                            f"สตรีมไอดี : {steam}\n"
                                            "สถานะ : ลงทะเบียนเรียบร้อย ✅\n"
                                            "=====================================\n```"
                                        )
                                        await interaction.channel.send(f"{member.mention}\n{result}", delete_after=5)
                                        await discord.DMChannel.send(member, result)
                                    else:
                                        warning = f'⚠ Error : {member.mention} รหัสปลดล๊อคไม่ถูกต้อง\n' \
                                                  f'กรุณากดที่ปุ่ม ACTIVATE MEMBERS เพื่อทำรายการใหม่อีกครั้ง'
                                        await interaction.channel.send(
                                            warning.strip(),
                                            delete_after=5)
                                        await msg.delete()
                                except asyncio.TimeoutError:
                                    msg = f'⚠ Error : {member.mention} คุณใช้เวลาในการกรอกรหัสปลดล็อคนานเกินไป\n' \
                                          ' กรุณากดที่ปุ่ม ACTIVATE MEMBERS เพื่อทำรายการใหม่อีกครั้ง'
                                    await interaction.channel.send(msg.strip(), delete_after=5)
                                    return
                        elif check == 2:
                            await interaction.respond(
                                content='เราได้รับรหัสปลดล็อคเรียบร้อยแล้ว กรุณารอข้อความยืนยันสิทธิ์จากระบบอีกครั้ง'
                            )

                    else:
                        await interaction.respond(
                            content=f'{member.mention} ไม่พบข้อมูล Steam id ของคุณในระบบ'
                        )
                elif member_check(member.id) == 0:
                    img = "https://cdn.discordapp.com/attachments/941531376363126814/964892521283072050" \
                          "/register_guide.png "
                    embed = discord.Embed(
                        title="โปรดลงทะเบียนเพื่อเปิดการใช้งานคำสั่ง",
                        colour=discord.Colour.red()
                    )
                    embed.set_thumbnail(url=member.avatar_url)
                    embed.set_image(url=img)
                    embed.add_field(name='สถานะการลงทะเบียน', value="ยังไม่ได้ลงทะเบียน 🔴")
                    embed.add_field(name='ห้องลงทะเบียน', value=f'{register}')
                    await interaction.respond(embed=embed)

            if btn == btn_list[2]:
                if member_check(member.id) != 0:
                    verify = verify_check(member.id)

                    def player_ign():
                        ign = players(member.id)[2]
                        if ign is not None:
                            return ign
                        elif ign is None:
                            message = "ยังไม่ระบุชื่อตัวละคร"
                            return message.strip()

                    if verify == 1:
                        img = "https://cdn.discordapp.com/attachments/941531376363126814/964896802274967622/unknown.png"
                        embed = discord.Embed(
                            title='คุณเป็นสมาชิค Exclusive Members แล้ว',
                            colour=discord.Colour.green()
                        )
                        embed.set_thumbnail(url=member.avatar_url)
                        embed.set_image(url=img)
                        embed.add_field(name='IGN', value='```cs\n{}\n```'.format(player_ign()))
                        embed.add_field(name='SteamID', value='```cs\n{}\n```'.format(steam_check(member.id)))
                        await interaction.respond(embed=embed)
                    else:
                        new = activate_code_check(member.id)
                        if new is not None:
                            await interaction.respond(content="อีกสักครู่คุณจะได้รับข้อความจากระบบ")
                            await discord.DMChannel.send(member, f" รหัสปลดล็อคของคุณ คือ {new}")
                            return
                        else:
                            activatecode = generate_code(6)
                            update_activate_code(member.id, activatecode)
                            await interaction.respond(content="อีกสักครู่คุณจะได้รับข้อความจากระบบ")
                            await discord.DMChannel.send(member, f" รหัสปลดล็อคของคุณ คือ {activatecode}")


def setup(bot):
    bot.add_cog(RegistartionMember(bot))
    bot.add_cog(RegistrationEvent(bot))
