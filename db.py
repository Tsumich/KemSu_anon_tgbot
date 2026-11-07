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
            admin_subtext varchar
        );
        """)
        await db.commit()

async def save_message(author, message, user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
                insert into messages (author, message, user_id, is_posted, is_deny) 
                    values(?, ?, ?, ?, ?)
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



async def get_message(id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
                select id, author, message from messages 
                where id = ?
                
            """, (id, ))
        result = await cursor.fetchone()
    return result

async def update_subtext(id, text):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
                update messages 
                set admin_subtext = ? , is_posted = 1
                where id = ?
                
            """, (id, text))
        result = await cursor.fetchone()
    return result
      