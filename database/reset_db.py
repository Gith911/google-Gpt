from db import get_connection

def reset_database():
    conn = get_connection()
    with conn:
        conn.execute('DROP TABLE IF EXISTS users')
        conn.execute('DROP TABLE IF EXISTS conversations')
    print("Database has been reset.")
