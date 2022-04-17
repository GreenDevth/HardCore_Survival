import os

import datetime
from sqlite3 import Error
from database.db_config import create_connection

database = os.path.abspath('./scum_db.db')


def member_check(discord):
    try:
        conn = create_connection(str(database))
        cur = conn.cursor()
        cur.execute("select count(*) from players where discord_id=?", (discord,))
        row = cur.fetchone()
        res = list(row)
        return res[0]
    except Error as e:
        print(e)


def players(discord):
    try:
        conn = create_connection(str(database))
        cur = conn.cursor()
        cur.execute('select * from players where discord_id=?', (discord,))
        rows = cur.fetchall()
        for row in rows:
            return row
    except Error as e:
        print(e)


def join_server(discord_name, discord_id, bank_id, join_date):
    try:
        conn = create_connection(database)
        cur = conn.cursor()
        cur.execute("INSERT INTO players(discord_name, discord_id, bank_id, join_date) VALUES (?,?,?,?)",
                    (discord_id, discord_name, bank_id, join_date,))
        conn.commit()
        cur.close()
        print('New player recode to database successfull!')
        msg = 'Welcome to Really Surivival'
        return msg.strip()
    except Error as e:
        print(e)


def leave_server(discord_id):
    x = datetime.datetime.now()
    leave_date = x.strftime("%d/%m/%Y %H:%M:%S")
    try:
        conn = create_connection(database)
        cur = conn.cursor()
        cur.execute("UPDATE players SET player_status='Leave', leave_date=? WHERE discord_id=?",
                    (leave_date, discord_id,))
        conn.commit()
        cur.close()
        print('Update Player status and leave date successfully!')
        msg = 'ไว้กลับมาเล่นด้วยกันใหม่ครับ '
        return msg.strip()
    except Error as e:
        print(e)


def welcome_back(discord_id):
    x = datetime.datetime.now()
    comeback_date = x.strftime("%d/%m/%Y %H:%M:%S")

    try:
        conn = create_connection(database)
        cur = conn.cursor()
        cur.execute("UPDATE players SET player_status='Joined', join_date=? WHERE discord_id=?",
                    (comeback_date, discord_id,))
        conn.commit()
        cur.close()
        print('Update Player comeback date successfully!')
        msg = 'ยินดีต้อนรับกลับ '
        return msg.strip()
    except Error as e:
        print(e)


def steam_check(discord):
    try:
        conn = create_connection(str(database))
        cur = conn.cursor()
        cur.execute('select steam_id from players where discord_id=?', (discord,))
        row = cur.fetchone()
        res = list(row)
        return res[0]
    except Error as e:
        print(e)


def update_steam_id(discord, steam, code):
    conn = None
    try:
        conn = create_connection(str(database))
        cur = conn.cursor()
        cur.execute('update players set steam_id=?, activate_code=? where discord_id=?', (steam, code, discord,))
        conn.commit()
        cur.close()
        msg = "โปรดนำรหัสปลดล็อคนี้ `` {} `` ใช้สำหรับการปลดล็อคการเข้าใช้งานเซิร์ฟของคุณ".format(code)
        return msg.strip()
    except Error as e:
        print(e)


def verify_check(discord_id):
    try:
        conn = create_connection(str(database))
        cur = conn.cursor()
        cur.execute('select verify_status from players where discord_id=?', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
        return None
    except Error as e:
        print(e)


def activate_code_check(discord_id):
    try:
        conn = create_connection(str(database))
        cur = conn.cursor()
        cur.execute('select activate_code from players WHERE discord_id = ?', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
        return None
    except Error as e:
        print(e)


def update_activate_code(discord, code):
    conn = None
    try:
        conn = create_connection(str(database))
        cur = conn.cursor()
        cur.execute('update players set activate_code=? where discord_id=?', (code, discord,))
        conn.commit()
        cur.close()
        msg = f"รหัสปลดล๊อคใหม่ของคุณคือ {code}"
        return msg.strip()
    except Error as e:
        print(e)


def activate_code(activatecode):
    conn = None
    try:
        conn = create_connection(str(database))
        cur = conn.cursor()
        cur.execute('UPDATE players SET verify_status = 2 WHERE activate_code = ?', (activatecode,))
        conn.commit()
        cur.close()
        msg = "🎉 Activate your player successfull " \
              "คุณจะได้รับข้อความตอบกลับหลังจากระบบได้ปรับสิทธิการใช้งานเซิร์ฟให้เรียบร้อยแล้ว"
        return msg.strip()
    except Error as e:
        print(e)


def verify_member(discord):
    conn = None

    try:
        conn = create_connection(str(database))
        cur = conn.cursor()
        cur.execute('UPDATE players SET verify_status = 1, member_type=? WHERE discord_id = ?', ("Exclusive", discord,))
        conn.commit()
        cur.close()
        msg = "🎉 Verify your player successfull! : Server IP [143.244.33.48:7102] "
        return msg.strip()
    except Error as e:
        print(e)


def player_award(discord):
    try:
        conn = create_connection(str(database))
        cur = conn.cursor()
        cur.execute('select discord_name, player_exp, player_level from players where discord_id=?', (discord,))
        rows = cur.fetchone()
        res = list(rows)
        return res

    except Error as e:
        print(e)


def insert_player(discord, name, steam, bank, coin, plevel, pexp, mtype, jdate, code, vstatus):
    conn = None
    try:
        conn = create_connection(str(database))
        cur = conn.cursor()
        query = "insert into players(discord_name, discord_id, steam_id, bank_id, coins, player_level, player_exp, " \
                "member_type, join_date, activate_code, player_status, verify_status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?) "
        values = (discord, name, steam, bank, coin, plevel, pexp, mtype, jdate, code, vstatus)
        cur.execute(query, values)
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
