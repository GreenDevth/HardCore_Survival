from database.Member_db import *


def player_bank(discord):
    try:
        conn = create_connection(str(db))
        cur = conn.cursor()
        cur.execute('select discord_name, bank_id, coins from players where discord_id=?', (discord,))
        rows = cur.fetchone()
        res = list(rows)
        return res
    except Error as e:
        print(e)


""" Get Discord id by bank id """


def discord_id(bank_id):
    try:
        conn = create_connection(str(db))
        cur = conn.cursor()
        cur.execute('select discord_id from players where bank_id=?', (bank_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def players(discord):
    try:
        conn = create_connection(str(db))
        cur = conn.cursor()
        cur.execute('select * from players where discord_id=?', (discord,))
        rows = cur.fetchall()
        for row in rows:
            return row
    except Error as e:
        print(e)


print(discord_id(45551))
