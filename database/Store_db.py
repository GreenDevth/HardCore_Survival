from database.Member_db import *


def create_table():
    conn = None
    try:
        conn = create_connection(db)
        cur = conn.cursor()

        """Create Shopping_cart Table"""
        list_of_table = cur.execute(
            """SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='SHOPPING_CART';""").fetchall()

        if not list_of_table:
            cur.execute(
                """CREATE TABLE shopping_cart(
                    ORDER_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    DISCORD_ID TEXT NULL,
                    DISCORD_NAME TEXT NULL,
                    STEAM_ID TEXT NULL,
                    ORDER_NUMBER TEXT NULL,
                    ITEM_ID INTEGER
                )""")
            print("Shopping cart table has been created!")
            conn.commit()
            cur.close()
        else:
            pass
    except Error as e:
        print(e)
