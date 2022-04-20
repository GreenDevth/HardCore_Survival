import asyncio
import datetime
import json
import os
import random
import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle
from database.Member_db import players
from database.Award import exp_process
from database.Bank_db import add_coins, mission_fine
from database.Mission_db import new_mission, mission_status, get_mission_id, mission_info, update_room_channel, \
    update_mission_img, mission_reset, create_table

fishing_id_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
farmer_id_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
hunter_id_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

report_id = os.getenv("PLAYER_QUEST_REPORT")


def select(missionlist):
    quest = None
    if missionlist == "fishing":
        quest = fishing_id_list
        return quest
    if missionlist == "hunter":
        quest = hunter_id_list
        return quest
    if missionlist == "farmer":
        quest = farmer_id_list
        return quest


with open('./config/guild.json') as config_channel:
    channel_list = json.load(config_channel)
    farm = channel_list['quest']['farmer_channel']
    hunt = channel_list['quest']['hunter_channel']
    fish = channel_list['quest']['fishing_channel']


def resport():
    with open('./config/guild.json') as config:
        result = json.load(config)
        report = result['quest']['report']
        return report


def mission_list(mission_id, mission_type):
    with open(f'./mission/{mission_type}.json', encoding='UTF8') as mission:
        data = json.load(mission)
        return data[str(mission_id)]


def mission_subject(mission_id):
    with open('./mission/mission_subject.json', encoding='UTF8') as subjects:
        data = json.load(subjects)
        return data[str(mission_id)]


class MissionCenter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.bot.user.name + " Connected.")
        create_table()

    @commands.command(name='center')
    async def group_mission_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/mission_ban.png')
        )
        await ctx.send(
            '\nผู้เล่นจะต้องนำส่งสินค้าที่ได้จากการกดรับภารกิจมาส่ง ที่ '
            '\nสถานีขนส่ง ตำแหน่ง A4N3 (สนามบิน)'
            '\nโดยจำนวนสินค้า ชนิด และรางวัลประจำภารกิจจะถูกระบุไว้'
            '\nในภาพที่ได้จากการกดรับภารกิจ ',
            file=discord.File('./img/guild.png')
        )
        await ctx.send(
            "📃**รายชื่อห้องรับภารกิจ**\n"
            f"<#{farm}>\n"
            f"<#{hunt}>\n"
            f"<#{fish}>\n"
        )

    @commands.command(name='hunter')
    async def hunter_mission_command(self, ctx):
        mission = mission_subject("hunter")

        embed = discord.Embed(
            title=f"{mission['Title']} : {mission['Name']}",
            description=mission['Description']
        )

        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text=f"Develop by : {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        embed.set_image(url=mission['ImageURL'])
        await ctx.send(
            embed=embed,
            components=[
                [
                    Button(style=ButtonStyle.green, label="GET QUEST", emoji='🥩', custom_id='hunter'),
                    Button(style=ButtonStyle.blue, label="REPORT QUEST", emoji='✉', custom_id='mission_report'),
                    Button(style=ButtonStyle.red, label="RESET QUEST", emoji='⏱', custom_id='mission_reset')
                ]
            ]
        )
        await ctx.message.delete()

    @commands.command(name='fishing')
    async def fishing_mission_command(self, ctx):
        mission = mission_subject("fishing")

        embed = discord.Embed(
            title=f"{mission['Title']} : {mission['Name']}",
            description=mission['Description']
        )

        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text=f"Develop by : {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        embed.set_image(url=mission['ImageURL'])
        await ctx.send(
            embed=embed,
            components=[
                [
                    Button(style=ButtonStyle.green, label="GET QUEST", emoji='🐟', custom_id='fishing'),
                    Button(style=ButtonStyle.blue, label="REPORT QUEST", emoji='✉', custom_id='mission_report'),
                    Button(style=ButtonStyle.red, label="RESET QUEST", emoji='⏱', custom_id='mission_reset')
                ]
            ]
        )
        await ctx.message.delete()

    @commands.command(name='farmer')
    async def farmer_mission_command(self, ctx):
        mission = mission_subject("farmer")

        embed = discord.Embed(
            title=f"{mission['Title']} : {mission['Name']}",
            description=mission['Description']
        )

        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text=f"Develop by : {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        embed.set_image(url=mission['ImageURL'])
        await ctx.send(
            embed=embed,
            components=[
                [
                    Button(style=ButtonStyle.green, label="GET QUEST", emoji='🍅', custom_id='farmer'),
                    Button(style=ButtonStyle.blue, label="REPORT QUEST", emoji='✉', custom_id='mission_report'),
                    Button(style=ButtonStyle.red, label="RESET QUEST", emoji='⏱', custom_id='mission_reset')
                ]
            ]
        )
        await ctx.message.delete()

    @commands.command(name='get_mission')
    async def get_mission(self, ctx, name: str):
        mission_id = random.choice(select(name))
        mission = mission_list(mission_id, name)

        embed = discord.Embed(
            title=f"{mission['Title']}",
            description=f'{mission["Description"]}',
            colour=discord.Colour.green()
        )
        embed.set_image(url=f"{mission['ImageURL']}")
        embed.add_field(name='Award', value=f"{mission['Award']}")
        await ctx.reply(embed=embed, mention_author=False)


class GetMissionEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        report_channel = interaction.guild.get_channel(int(report_id))
        btn = interaction.component.custom_id
        btn_list = ["farmer", "hunter", "fishing"]
        btn_cmd = ["mission_report", "mission_reset", "upload_img", "solf_reset", "hard_reset"]

        player = players(member.id)
        if player[18] == 1:

            if btn in btn_list:
                if mission_status(member.id) is None or mission_status(member.id) == 0:
                    mission_id = random.choice(select(btn))
                    mission = mission_list(mission_id, str(btn))
                    embed = discord.Embed(
                        title=f"{mission['Title']} : {mission['Name']}",
                        description=f"{mission['Description']}",
                        color=discord.Colour.red()
                    )
                    embed.set_thumbnail(url=member.avatar_url)
                    coins = "${:,d}".format(mission['Award'])
                    embed.add_field(name="ผู้รับภารกิจ", value=f"```cs\n{member.name}\n```", inline=False)
                    embed.add_field(name='จำนวน', value=f"```cs\n{mission['Quantity']}\n```")
                    embed.add_field(name='💵 เงินรางวัล', value=f"```cs\n{coins}\n```")
                    embed.add_field(name='🎖 ค่าประสบการณ์', value=f"```cs\n{mission['Award']} exp.\n```")
                    embed.set_image(url=mission['ImageURL'])
                    await interaction.respond(embed=embed)
                    await report_channel.send(f"{member.mention}", embed=embed)
                    new_mission(member.name, member.id, mission['Name'], mission['Award'], mission['Exp'],
                                mission['ImageURL'], mission_id, str(btn))
                elif mission_status(member.id) == 1:
                    if get_mission_id(member.id)[0] is not None:
                        mission_id = get_mission_id(member.id)[0]
                        mission_type = get_mission_id(member.id)[1]
                        mission = mission_list(mission_id, str(mission_type))
                        embed = discord.Embed(
                            title=f"คุณยังทำภารกิจ {mission['Name']} ่ไม่สำเร็จ",
                            color=discord.Colour.red()
                        )
                        embed.set_image(url=mission['ImageURL'])
                        await interaction.respond(embed=embed)
                    else:
                        await interaction.respond(content='มีข้อผิดพลาด, กรุณาติดต่อทีมงานเพื่อดำเนินการตรวจสอบให้')
                    return
                return
            if btn in btn_cmd:
                if btn == "mission_report":
                    if mission_status(member.id) is None or mission_status(member.id) == 0:
                        await interaction.respond(content='คุณยังไม่มีภารกิจให้ต้องส่ง')
                        return
                    elif mission_status(member.id) == 1:
                        def check():
                            try:
                                if mission_info(member.id)[7] is None:
                                    channel_id = 0000000000000000
                                    return channel_id
                                elif mission_info(member.id)[7] is not None:
                                    # print(mission_info(member.id)[7])
                                    channel_id = int(mission_info(member.id)[7])
                                    return channel_id
                            except Exception as e:
                                print(e)

                        channel_name = interaction.guild.get_channel(check())
                        if channel_name is None:
                            mission_id = get_mission_id(member.id)[0]
                            mission_type = get_mission_id(member.id)[1]
                            mission = mission_list(mission_id, str(mission_type))
                            await interaction.respond(
                                content='โปรดรอสักครู่ '
                                        'ระบบกำลังสร้างห้องสำหรับส่งภารกิจ **{}** ให้กับคุณ'.format(mission["Name"]))
                            categorys = discord.utils.get(interaction.guild.categories,
                                                          name='SERVER QUEST')
                            overwrites = {
                                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False,
                                                                                            connect=False),
                                member: discord.PermissionOverwrite(read_messages=True)
                            }
                            await categorys.edit(overwrites=overwrites)
                            report_channel = f'ห้องส่งภารกิจ-{mission_info(member.id)[0]}'
                            await interaction.guild.create_text_channel(report_channel, category=categorys)
                            channel = discord.utils.get(interaction.guild.channels, name=str(report_channel))
                            update_room_channel(member.id, channel.id)
                            include = self.bot.get_channel(channel.id)
                            embed = discord.Embed(
                                title='ภารกิจของ {}'.format(mission_info(member.id)[1]),
                                description='ภารกิจ {} ผู้เล่นต้องนำสินค้าใส่ไว้ในตู้ที่จัดเตรียมไว้'
                                            'ให้และล็อคกุญแจให้เรียบร้อย หากเกิดกรณีไม่พบสินค้าผู้เล่นอาจ'
                                            'จะเสียสิทธิ์ในการรับเงินรางวัล และยึดค่าประสบการณ์คืน'.format(
                                    mission_info(member.id)[3]),
                                color=discord.Colour.green()
                            )
                            embed.set_author(name=member.name, icon_url=member.avatar_url)
                            embed.set_thumbnail(url=member.avatar_url)
                            embed.set_image(url=mission_info(member.id)[6])
                            embed.set_footer(text='หากพบการทุจริตในการส่งสินค้า ต้องรับโทษปรับสูงสุด')
                            await include.send(
                                '{}\nศึกษาคู่มือการใช้งานได้ที่ <#932164700479828008>'.format(member.mention),
                            )
                            await include.send(
                                embed=embed,
                                components=[
                                    [
                                        Button(style=ButtonStyle.green,
                                               label='MISSION AWARD ${:,d}'.format(mission_info(member.id)[4]),
                                               emoji='💵',
                                               disabled=True),
                                        Button(style=ButtonStyle.blue, label='UPLOAD MISSION IMAGE', emoji='📷',
                                               custom_id='upload_img')
                                    ]
                                ]
                            )
                            await interaction.channel.send('🛣 ไปยังห้องส่งภารกิจของคุณที่ <#{}>'.format(channel.id),
                                                           delete_after=5)
                            return
                        elif channel_name is not None:
                            await interaction.respond(
                                content='🛣 ไปยังห้องส่งภารกิจของคุณที่ <#{}>'.format(mission_info(member.id)[7]))

                elif btn == "upload_img":
                    await interaction.edit_origin(
                        components=[]
                    )
                    await interaction.channel.send(
                        f'{member.mention} : 📷 กรูณาอัพโหลดภาพสินค้าที่อยู่ในตู้ของคุณ '
                        f'เพื่อให้ระบบตรวจสอบและนำจ่ายเงินรางวัล')

                    def check(res):
                        attachments = res.attachments
                        if len(attachments) == 0:
                            return False
                        attachment = attachments[0]
                        file_type = attachment.filename.endswith(('.jpg', '.png', 'jpeg'))
                        return res.author == interaction.author and res.channel == interaction.channel and file_type

                    try:
                        msg = await self.bot.wait_for('message', check=check, timeout=60)
                        if msg is not None:
                            player = mission_info(member.id)
                            report_channel = interaction.guild.get_channel(resport())
                            embed = discord.Embed(
                                title=f'ภารกิจ {mission_info(member.id)[3]} สำเร็จ 🟢',
                                description='☢ คำเตือน ! หากตรวจพบการทุจริต จะทำการยึดเงินและค่าประสบการณ์ทั้งหมดทันที',
                                colour=discord.Colour.green(),
                                timestamp=datetime.datetime.utcnow()
                            )
                            embed.set_thumbnail(url=member.avatar_url)
                            embed.set_image(url=msg.attachments[0])
                            embed.add_field(name='ผู้ส่งภารกิจ', value=member.mention)
                            embed.set_footer(text='ส่งภารกิจเมื่อ')
                            await report_channel.send(embed=embed)
                            update_mission_img(member.id)
                            result_coins = add_coins(member.id, player[4])
                            result_exp = exp_process(member.id, player[5])
                            await interaction.channel.send(
                                f"{result_coins}\n{result_exp}",
                                components=[
                                    Button(style=ButtonStyle.red, label='Reset mission and close this channel',
                                           emoji='🏁',
                                           custom_id='solf_reset')]
                            )
                            await discord.DMChannel.send(member, f"```cs\n{result_coins}\n{result_exp}\n```")
                            statement = self.bot.get_channel(resport())
                            msg = await statement.send(
                                "📃 **Mission Statement {}**\n"
                                "```=====================================\n"
                                "ผู้ทำภารกิจ : {}\n"
                                "ภารกิจ : {}\n"
                                "เงินรางวัล : ${:,d}\n"
                                "ค่าประสบการณ์ : {} exp\n"
                                "สถานะ : จ่ายแล้ว ✅\n"
                                "=====================================\n```".format(member.display_name,
                                                                                    member.display_name,
                                                                                    player[3], player[4],
                                                                                    player[5])
                            )
                            await msg.add_reaction("💰")
                            await asyncio.sleep(1.2)
                            await msg.add_reaction("✅")

                    except asyncio.TimeoutError:
                        await interaction.channel.send('คุณดำเนินการล่าช้า โปรดกดปุ่มอัพโหลดรูปภาพอีกครั้ง')
                elif btn == 'solf_reset':
                    result = mission_reset(member.id)
                    overwrites = {
                        interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        member: discord.PermissionOverwrite(read_messages=False)
                    }
                    await interaction.edit_origin(
                        components=[]
                    )
                    await interaction.channel.edit(overwrites=overwrites)
                    await interaction.channel.send(f'{result}')
                elif btn == 'hard_reset':
                    result = mission_fine(member.id, 100)
                    await interaction.respond(content=f"{result['reset']}")
                    await discord.DMChannel.send(member, f"```cs\n{result['fine']}\n```")
                elif btn == 'mission_reset':
                    if mission_status(member.id) is None or mission_status(member.id) == 0:
                        await interaction.respond(content='คุณยังไม่มีภารกิจให้รีเซ็ต')
                        return
                    else:
                        await interaction.respond(content="การรีเซ็ตภารกิจมีค่าบริการจำนวน $100\n"
                                                          " กดปุ่ม YES หากต้องการรีเซ็ตภารกิจใหม่",
                                                  components=[Button(style=ButtonStyle.red, label='YES', emoji='⚠',
                                                                     custom_id='hard_reset')])
                else:
                    await interaction.respond(content=member.name + f"click {btn}")

        else:
            await interaction.respond(content='คุณยังไม่ได้ทำการปลดล็อคการใช้งานคำสั่งนี้ <#950952899519868978>')


class PlayerMission(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='player_mission')
    @commands.has_permissions(manage_roles=True)
    async def player_mission_commnad(self, ctx):
        await ctx.reply('ok', mention_author=False)


def setup(bot):
    bot.add_cog(MissionCenter(bot))
    bot.add_cog(GetMissionEvent(bot))
    bot.add_cog(PlayerMission(bot))
