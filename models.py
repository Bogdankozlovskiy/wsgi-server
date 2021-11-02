import sqlite3

connection = sqlite3.connect("my_db.db", check_same_thread=False)


connection.execute("PRAGMA foreign_keys = ON;")

connection.execute("""
    CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login varchar(25) UNIQUE NOT NULL
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
        CONSTRAINT fuck_checker CHECK ( message not like '%fuck%'),
        CONSTRAINT length_checker CHECK ( length(message) > 5 )
    )
""")


connection.execute("""
    CREATE TABLE IF NOT EXISTS chat_to_user_like(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        chat_id INTEGER NOT NULL,
        
        CONSTRAINT user_chat_unique UNIQUE (user_id, chat_id)
    )
""")

connection.execute("""
    CREATE TRIGGER IF NOT EXISTS increase_count_of_like
    AFTER INSERT ON chat_to_user_like
    BEGIN
        UPDATE chat 
        SET count_of_likes=chat.count_of_likes + 1
        WHERE chat.id=NEW.chat_id;
    END;
""")

connection.execute("""
    CREATE TRIGGER IF NOT EXISTS decrease_count_of_like
    AFTER DELETE ON chat_to_user_like
    BEGIN
        UPDATE chat 
        SET count_of_likes=chat.count_of_likes - 1
        WHERE chat.id=OLD.chat_id;
    END;
""")

connection.execute("""
    CREATE INDEX IF NOT EXISTS user_id_and_id_index
    ON chat_to_user_like(user_id, chat_id)
""")

connection.execute("""
    CREATE INDEX IF NOT EXISTS user_id_and_id_index
    ON chat(user_id, id)
""")


connection.execute("""
    CREATE VIEW IF NOT EXISTS chat_data as
    SELECT user.login, chat.publish_date, chat.message, chat.id, chat.count_of_likes
    FROM chat
    JOIN user
    ON user.id=chat.user_id
    ORDER BY chat.publish_date desc
""")
