import sqlite3

connection = sqlite3.connect("my_db.db", check_same_thread=False)
try:
    connection.execute("PRAGMA FOREIGN_KEYS=ON;")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS user(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login varchar(25) UNIQUE NOT NULL,
            count_of_message INTEGER DEFAULT 0
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS chat(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message text NOT NULL,
            publish_date date NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
            user_id INTEGER NOT NULL,
            count_of_likes INTEGER DEFAULT 0,
            
            FOREIGN KEY(user_id) REFERENCES user(id),
            CONSTRAINT NE_message CHECK ( message not in ('fuck', 'dick')),
            CONSTRAINT GT_message CHECK ( LENGTH(message) >= 3 )
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS chat_user(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            
            FOREIGN KEY (chat_id) REFERENCES chat(id),
            FOREIGN KEY (user_id) REFERENCES user(id),
            
            CONSTRAINT UC_chat_user UNIQUE (chat_id, user_id)
        )
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_id_user_id
        ON chat(id, user_id)
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_user_id
        ON chat(user_id)
    """)

    connection.execute("""
        CREATE VIEW IF NOT EXISTS chat_data AS
        SELECT user.login, chat.publish_date, chat.message, chat.id, COALESCE(likes_table.likes, 0), chat.count_of_likes
            --CASE 
            --    WHEN likes_table.likes IS NULL THEN 0 
            --    ELSE likes_table.likes 
            --END AS likes
        FROM chat
        JOIN user
        ON user.id=chat.user_id
        LEFT JOIN (
            SELECT chat_id, COUNT(*) AS likes 
            FROM chat_user 
            GROUP BY chat_id
            ) likes_table
        ON likes_table.chat_id=chat.id
        ORDER BY chat.publish_date DESC
    """)

    connection.execute("""
        CREATE TRIGGER IF NOT EXISTS increase_count_of_message_after_insert
           AFTER INSERT ON chat
        BEGIN
            UPDATE user
            SET count_of_message=(
                SELECT COUNT(*)
                FROM chat
                WHERE chat.user_id=NEW.user_id
            )
            WHERE user.id=NEW.user_id;
        END;
    """)

    connection.execute("""
            CREATE TRIGGER IF NOT EXISTS decrease_count_of_message_after_delete
               AFTER DELETE ON chat
            BEGIN
                UPDATE user
                SET count_of_message=(
                    SELECT COUNT(*)
                    FROM chat
                    WHERE chat.user_id=OLD.user_id
                )
                WHERE user.id=OLD.user_id;
            END;
        """)

    connection.execute("""
        CREATE TRIGGER IF NOT EXISTS increase_count_of_likes
            AFTER INSERT ON chat_user
        BEGIN
            UPDATE chat
            SET count_of_likes=chat.count_of_likes + 1
            WHERE chat.id=NEW.chat_id;
        END;
    """)

    connection.execute("""
        CREATE TRIGGER IF NOT EXISTS decrease_count_of_likes
            AFTER DELETE ON chat_user
        BEGIN
            UPDATE chat
            SET count_of_likes=chat.count_of_likes - 1
            WHERE chat.id=OLD.chat_id;
        END;
    """)
except Exception:
    connection.rollback()
    raise
else:
    connection.commit()
