from database.Member_db import *


def exp_update(discord_id, exp):
    player = players(discord_id)
    player_level = player[7]
    player_exp = player[8]
    exp_plus = player_exp + exp
    default_level = 100000
    msg = None
    if default_level <= exp_plus:
        exp_after = exp_plus - default_level
        level_update(discord_id, player_level + 1)
        update_exp(discord_id, exp_after)
        level = players(discord_id)
        if level != 0:
            reset_exp(discord_id)
        exps = players(discord_id)[8]
        msg = f'🎉 **Congratulation Your Level up to {level[7]}**\n' \
              f"ระบบได้ทำการรีเซ็ตค่าประสบการณ์ใหม่เรียบร้อยแล้ว ค่าประสบการณ์ปัจจุบันคือ **{exps}**"
    elif exp_plus < default_level:
        update_exp(discord_id, exp_plus)
        exps = players(discord_id)[8]
        msg = f"คุณได้รับค่าประสบการณ์เพิ่ม จำนวน **{exp}** ค่าประสบการณ์ปัจจุบันของคุณคือ **{exps}**"
    return msg


def exp_process(discord, exp):
    result = exp_update(discord, exp)
    y_int = isinstance(result, int)
    if y_int is True:
        exp = result
        return exp
    else:
        exp = result
        return exp


def level_update(discord_id, level):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('update players set player_level = %s where discord_id = %s', (level, discord_id,))
        conn.commit()
        print('Level update successfull.')
        cur.close()
        return
    except Error as e:
        print(e)


def update_exp(discord_id, exp):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('update players set player_exp = %s where discord_id = %s', (exp, discord_id,))
        conn.commit()
        print('Exp update successfull.')
        cur.close()
        return
    except Error as e:
        print(e)


def reset_exp(discord):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute("UPDATE players SET player_exp = 0 WHERE discord_id=%s", (discord,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
