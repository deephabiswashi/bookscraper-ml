# app/main.py
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, render_template, request
import sqlite3
from model.book_model import process_description

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'books.db')

def get_book_description(title):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT description FROM books WHERE title = ?", (title,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

@app.route('/', methods=['GET', 'POST'])
def index():
    overview = None
    if request.method == 'POST':
        user_title = request.form.get('title')
        mode = request.form.get('mode')  # processing mode: summarization, classification, sentiment
        if user_title:
            description = get_book_description(user_title)
            if description:
                overview = process_description(description, mode=mode)
            else:
                overview = "Book not found in database."
    return render_template('index.html', overview=overview)

if __name__ == '__main__':
    app.run(debug=True)
