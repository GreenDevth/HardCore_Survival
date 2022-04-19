from database.Bank_db import remove_coins, mission_fine
from database.Member_db import *

db = str(os.path.abspath('./SQLite/scum_db.db'))


def player_check(discord):
    try:
        conn = create_connection(db)
        cur = conn.cursor()
        rows = cur.execute('select count(*) from player_mission where player_id=?', (discord,)).fetchone()
        res = list(rows)
        return res[0]
    except Error as e:
        print(e)


def mission_status(discord):
    try:
        conn = create_connection(db)
        cur = conn.cursor()
        cur.execute('SELECT mission_status FROM player_mission WHERE player_id=?', (discord,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def new_mission(name, discord, mission, award, exp, img, quest_id, mission_type):
    conn = None

    try:
        conn = create_connection(db)
        cur = conn.cursor()
        cur.execute("INSERT OR REPLACE INTO player_mission(player_name, player_id, mission_name, mission_award, "
                    "mission_exp, mission_img, mission_status, quest_id, mission_type) VALUES (?,?,?,?,?,?,?,?,?)",
                    (name, discord, mission, award, exp, img, 1, quest_id, mission_type,))
        conn.commit()
        print("New recode insert to player_mission")
        cur.close()
    except Error as e:
        print(e)


def get_mission_id(discord):
    try:
        conn = create_connection(db)
        cur = conn.cursor()
        rows = cur.execute('select quest_id, mission_type from player_mission where player_id=?', (discord,)).fetchone()
        while rows is not None:
            res = list(rows)
            return res
    except Error as e:
        print(e)


def new_room_id(discord):
    try:
        conn = create_connection(db)
        cur = conn.cursor()
        row = cur.execute('select mission_id from player_mission where player_id=?', (discord,)).fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def update_room_channel(discord, channel_id):
    conn = None
    try:
        conn = create_connection(db)
        cur = conn.cursor()
        cur.execute('update player_mission set report_room=?, report_status=1 where player_id=?',
                    (channel_id, discord,))
        conn.commit()
        print('Create new report channel sucessfull!')
        cur.close()
    except Error as e:
        print(e)


def mission_info(discord):
    try:
        conn = create_connection(db)
        cur = conn.cursor()
        rows = cur.execute('select * from player_mission where player_id=?', (discord,)).fetchone()
        while rows is not None:
            res = list(rows)
            return res
    except Error as e:
        print(e)


def update_mission_img(discord):
    conn = None
    try:
        conn = create_connection(db)
        cur = conn.cursor()
        cur.execute('update player_mission set upload_status=1 where player_id=?', (discord,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)


def mission_reset(discord):
    conn = None
    try:
        conn = create_connection(db)
        cur = conn.cursor()
        cur.execute('UPDATE player_mission set upload_status=0, report_status=0, mission_status=0 where player_id=?',
                    (discord,))
        conn.commit()
        cur.close()
        print('reset player mission success!')
        msg = "ระบบทำการรีเซ็ตภารกิจของคุณให้เรียบร้อยแล้ว"
        return msg.strip()
    except Error as e:
        print(e)
