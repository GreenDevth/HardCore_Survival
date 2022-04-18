from database.Member_db import *
import datetime


x = datetime.datetime.now()
create_date = x.strftime("%d/%m/%Y %H:%M:%S")


def get_id(discord):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        row = cur.execute('select donate_id from donation where discord_id=%s', (discord,)).fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def new_donate_player(discord_name, discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = """INSERT INTO donation(discord_name, discord_id, create_date) VALUES (%s,%s,%s)"""
        variable = (discord_name, discord_id, create_date,)
        cur.execute(sql, variable)
        conn.commit()
        print('create new donate players')
    except Error as e:
        print(e)
    finally:
        room_id = get_id(discord_id)
        return room_id


def update_room_id(discord, room_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('update donation set channel_id=%s where discord_id=%s', (room_id, discord,))
        conn.commit()
        cur.close()
        print('update donate room sucessfull!')
    except Error as e:
        print(e)


def update_donate_date(discord):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('update donation set create_date=%s where discord_id=%s', (create_date, discord,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)


def get_channel_id(discord):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        row = cur.execute('select channel_id from donation where discord_id=%s', (discord,)).fetchone()
        while row is not None:
            res = list(row)
            return res[0]
        return None
    except Error as e:
        print(e)
