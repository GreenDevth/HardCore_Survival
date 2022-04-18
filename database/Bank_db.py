from database.Member_db import *


def coins_update(discord, coin):
    conn = None
    try:
        conn = create_connection(db)
        cur = conn.cursor()
        cur.execute('update players set coins=? where discord_id=?', (coin, discord,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)


def player_bank(discord):
    try:
        conn = create_connection(db)
        cur = conn.cursor()
        cur.execute('select discord_name, bank_id, coins from players where discord_id=?', (discord,))
        rows = cur.fetchone()
        res = list(rows)
        return res
    except Error as e:
        print(e)


def discord_id(bank_id):
    try:
        conn = create_connection(db)
        cur = conn.cursor()
        cur.execute('select discord_id from players where bank_id=?', (bank_id,))
        row = cur.fetchone()
        res = list(row)
        return res[0]
    except Error as e:
        print(e)


def plus_coin(receiver, coin, senders):
    receiver_coins = player_bank(receiver)[2]  # get current coins receiver
    sender = player_bank(senders)[0]  # get name sender
    coins = int(receiver_coins) + int(coin)
    transfer = "${:,d}".format(coin)
    conn = None
    try:
        conn = create_connection(db)
        cur = conn.cursor()
        cur.execute('update players set coins=? where discord_id=?', (coins, receiver,))
        conn.commit()
        print("update coins successfull!")
        cur.close()
        msg = "คุณได้รับเงินจำนวน **{}** จาก **{}** ยอดเงินปัจจุบันคือ : **${:,d}**".format(transfer, sender, coins)
        return msg.strip()
    except Error as e:
        print(e)


def minus_coin(discord, coin):
    player_coin = player_bank(discord)[2]  # get current player coins
    coins = int(player_coin) - int(coin)
    conn = None
    try:
        conn = create_connection(db)
        cur = conn.cursor()
        cur.execute('update players set coins=? where discord_id=?', (coins, discord,))
        conn.commit()
        cur.close()
        msg = "ระบบได้หักเงินจำนวน **${:,d}** จากบัญชีของคุณ ยอดเงินปัจจุบันคือ **${:,d}**".format(coin, coins)
        return msg.strip()
    except Error as e:
        print(e)


def add_coins(discord, coin):
    player_coin = player_bank(discord)[2]
    coins = int(player_coin) + int(coin)
    conn = None
    try:
        conn = create_connection(db)
        cur = conn.cursor()
        cur.execute('update players set coins=? where discord_id=?', (coins, discord,))
        conn.commit()
        cur.close()
        print('add coin successfull!')
    except Error as e:
        print(e)
    finally:
        receipt = "${:,d}".format(int(coin))
        total = "${:,d}".format(coins)
        msg = f"คุณได้รับโอนเงินจากระบบจำนวน {receipt} ยอดเงินปัจจุบันคือ {total}"
        return msg.strip()


def remove_coins(discord, coin):
    player_coin = player_bank(discord)[2]

    def check():
        if player_coin < int(coin):
            c = 0
            return c
        elif int(coin) <= player_coin:
            c = int(player_coin) - int(coin)
            return c

    coins = check()
    conn = None
    try:
        conn = create_connection(db)
        cur = conn.cursor()
        cur.execute('update players set coins=? where discord_id=?', (coins, discord,))
        conn.commit()
        cur.close()
        msg = "ระบบทำการหักเงินของคุณจำนวน **${:,d}** ยอดเงินปัจจุบันคือ **${:,d}**".format(int(coin), coins)
        return msg.strip()
    except Error as e:
        print(e)
