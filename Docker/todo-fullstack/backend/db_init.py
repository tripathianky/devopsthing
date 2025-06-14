import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres")

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS todos (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title TEXT NOT NULL,
    done BOOLEAN DEFAULT FALSE
);
''')

conn.commit()
cur.close()
conn.close()

print("Database initialized.")
