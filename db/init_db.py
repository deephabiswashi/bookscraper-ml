# db/init_db.py
import sqlite3
import csv
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'books.db')
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'books_data.csv')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price TEXT,
            availability TEXT,
            rating TEXT,
            detail_url TEXT,
            description TEXT
        )
    ''')

    # Clear out old data if you re-run
    cursor.execute('DELETE FROM books')

    # Insert data from CSV
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row['title']
            price = row['price']
            availability = row['availability']
            rating = row['rating']
            detail_url = row['detail_url']
            description = row['description']  # now from the CSV

            cursor.execute('''
                INSERT INTO books (title, price, availability, rating, detail_url, description)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, price, availability, rating, detail_url, description))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
