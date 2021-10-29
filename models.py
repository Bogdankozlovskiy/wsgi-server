import sqlite3

connection = sqlite3.connect("my_db.db", check_same_thread=False)
try:
    connection.execute("PRAGMA FOREIGN_KEYS=ON;")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS user(
            id INTEGER PRIMARY KEY DEFAULT (randomblob(16)),
            login varchar(25) UNIQUE NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS chat(
            id INTEGER PRIMARY KEY DEFAULT (randomblob(16)),
            message text NOT NULL,
            publish_date date NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
            user_id INTEGER NOT NULL,
            
            FOREIGN KEY(user_id) REFERENCES user(id),
            CONSTRAINT NE_message CHECK ( message <> 'fuck')
        )
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_user_id
        ON chat(id, user_id)
    """)

    connection.execute("""
        CREATE VIEW IF NOT EXISTS chat_data AS
        SELECT user.login, chat.publish_date, chat.message, chat.id
        FROM chat 
        JOIN user
        ON user.id=chat.user_id
        ORDER BY chat.publish_date desc
    """)
except Exception:
    connection.rollback()
    raise
else:
    connection.commit()
