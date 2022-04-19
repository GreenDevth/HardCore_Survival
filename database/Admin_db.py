import os.path
from sqlite3 import Error
import pandas as pd
from database.db_config_SQLite import create_connection

db = str(os.path.abspath('./SQLite/scum_db.db'))
exclusive = str(os.path.abspath('./Exclusive'))


def exclusive_lists():
    try:
        conn = create_connection(db)
        cur = conn.cursor()
        sql_query = pd.read_sql(
            """SELECT steam_id, discord_name, discord_id, member_type FROM players WHERE member_type='Exclusive' 
            order by player_id""", conn)
        df = pd.DataFrame(sql_query)
        df.to_csv('./Exclusive/exclusive_data.csv', index=False)
        print("Export Exclusive_data file successfull!")
        cur.close()
        msg = "exclusive_data.csv"
        return msg.strip()
    except Error as e:
        print()


def create_new_table(tbname):
    conn = None
    try:
        conn = create_connection(db)
        cur = conn.cursor()

        cur.execute("SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name=?", (tbname,))
        list_of_tables = cur.fetchall()
        if not list_of_tables:
            print('Table not found!')
        else:
            print('Table found!')
    except Error as e:
        print(e)
