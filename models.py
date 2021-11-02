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
        
        FOREIGN KEY(user_id) REFERENCES user(id),
        CONSTRAINT fuck_checker CHECK ( message not like '%fuck%'),
        CONSTRAINT length_checker CHECK ( length(message) > 5 )
    )
""")


connection.execute("""
    CREATE INDEX IF NOT EXISTS user_id_and_id_index
    ON chat(user_id, id)
""")
