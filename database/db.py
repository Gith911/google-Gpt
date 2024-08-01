import sqlite3

DATABASE_NAME = 'chatbot.db'

def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def initialize_db():
    conn = get_connection()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                message_count INTEGER DEFAULT 0
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                user_id INTEGER,
                message TEXT,
                reply TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
