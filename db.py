import datetime

import aiosqlite


DB_NAME = "anonkemsu.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        create table if not exists messages (
            id integer primary key autoincrement,
            author varchar,
            message varchar not null,
            user_id integer,
            is_posted boolean not null,
            is_deny boolean not null,
            admin_subtext varchar,
            who_posted integer,
            time_created datetime,
            time_updated datetime
        );
        """)
        await db.commit()

async def save_message(author, message, user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
                insert into messages (author, message, user_id, is_posted, is_deny, time_created) 
                    values(?, ?, ?, ?, ?, datetime('now','localtime'))
            """, (author, message, user_id, 0, 0))
        await db.commit()


async def get_all_message(limit, offset):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
                select id, author, message from messages 
                where is_posted = 0 and is_deny = 0
                LIMIT ? OFFSET ?
            """, (limit, offset))
        result = await cursor.fetchall()
    return result


async def drop_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("Drop table messages")
        await db.commit()



async def get_message(id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
                select id, author, message from messages 
                where id = ? and is_posted = 0 and is_deny = 0
                
            """, (id, ))
        result = await cursor.fetchone()
    return result

async def update_subtext(id, text, admin_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
                update messages 
                set admin_subtext = ? , 
                    is_posted = 1, 
                    who_posted = ? ,
                    time_updated =  TIME('now','localtime')
                where id = ?
                
            """, (text, admin_id, id))
        await db.commit()

async def update_message_to_deny(id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
                update messages 
                set is_deny = 1, 
                    time_updated =  TIME('now','localtime')
                where id = ?
                
            """, (id, ))
        await db.commit()

#-------- ФУНКЦИЯ ДОСТАЕТ ПОСЛЕДНЕЕ СМС И ПРОВЕРЯЕТ ПРОШЛО ЛИ БОЛЬШЕ 15 МИНУТ -------------
async def get_last_message(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            SELECT time_created, id 
            FROM messages 
            WHERE user_id = ? 
            ORDER BY id DESC 
            LIMIT 1;
            """, (user_id, ))
        content = await cursor.fetchone() 
    time_created, id = content
    if time_created is None:
        return True
    today = datetime.datetime.now()
    date_obj = datetime.datetime.strptime(time_created, '%Y-%m-%d %H:%M:%S')
    diff = (today - date_obj).total_seconds() // 60
    if diff > 15:
        return True
    else: 
        return False      