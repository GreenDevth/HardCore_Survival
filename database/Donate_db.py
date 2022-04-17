import os
from sqlite3 import Error
from database.db_config import create_connection
from datetime import datetime

db = str(os.path.abspath('./scum_db.db'))


def get_donate_room(discord_id):
    try:
        conn = create_connection(db)
        cur = conn.cursor()
        cur.execute('select channel_id from donate where discord_id=?', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)
