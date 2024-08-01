import sqlite3

def init_db():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS conversations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT,
                        message TEXT,
                        response TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                      )''')
    conn.commit()
    conn.close()

def update_conversation(user_id, message, response):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO conversations (user_id, message, response) VALUES (?, ?, ?)",
                   (user_id, message, response))
    conn.commit()
    conn.close()

def reset_db():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS conversations")
    conn.commit()
    init_db()
    conn.close()

if __name__ == "__main__":
    reset_db()
