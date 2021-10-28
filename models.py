import sqlite3

connection = sqlite3.connect("my_db.db")


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
        publish_date date NOT NULL,
        user_id INTEGER NOT NULL,
        
        FOREIGN KEY(user_id) REFERENCES user(id)
    )
""")
