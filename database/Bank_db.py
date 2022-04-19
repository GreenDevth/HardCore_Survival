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


def try_reset(discord):
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


def mission_fine(discord, amount):
    amount = int(amount)
    player_coin = int(player_bank(discord)[2])

    def check():
        if player_coin < int(amount):
            c = 0
            return c
        elif int(amount) <= player_coin:
            c = int(player_coin) - int(amount)
            return c

    coins = check()

    if int(coins) == 0:
        msg = "ยอดเงินของคุณไม่เพียงพอสำหรับจ่ายค่ารีเซ็ตภารกิจ"
        return msg.strip()
    else:
        coins_update(discord, int(coins))
        tozero = try_reset(discord)
        player_coin = player_bank(discord)[2]
        msg = "ระบบทำการหักเงินของคุณจำนวน" \
              " **${:,d}** ยอดเงินปัจจุบันคือ **${:,d}**".format(int(amount), int(player_coin))
        data = {
            "reset": tozero,
            "fine": msg
        }
        return data
