import sqlite3
from datetime import datetime

DB_NAME = 'library.db'

def connect_db():
    return sqlite3.connect(DB_NAME)

def setup_db():
    conn = connect_db()
    cur = conn.cursor()

    # Books table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        publisher TEXT,
        genre TEXT,
        quantity INTEGER NOT NULL
    )
    """)

    # Members table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS members (
        member_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact TEXT
    )
    """)

    # Issued books table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS issued_books (
        issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        member_id INTEGER,
        issue_date TEXT,
        return_date TEXT,
        FOREIGN KEY (book_id) REFERENCES books(book_id),
        FOREIGN KEY (member_id) REFERENCES members(member_id)
    )
    """)

    conn.commit()
    conn.close()

# BOOK OPERATIONS
def add_book(title, author, publisher, genre, quantity):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO books (title, author, publisher, genre, quantity)
        VALUES (?, ?, ?, ?, ?)
    """, (title, author, publisher, genre, quantity))
    conn.commit()
    conn.close()

def get_all_books():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    conn.close()
    return books

# ✅ YOUR OWN Bubble Sort
def bubble_sort_books(books):
    n = len(books)
    for i in range(n):
        for j in range(0, n - i - 1):
            if books[j][1].lower() > books[j + 1][1].lower():
                books[j], books[j + 1] = books[j + 1], books[j]
    return books

def search_books_by_title(title):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM books WHERE title LIKE ?", ('%' + title + '%',))
    results = cur.fetchall()
    conn.close()
    return results

def delete_book(book_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
    conn.commit()
    conn.close()

# MEMBER OPERATIONS
def add_member(name, contact):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO members (name, contact) VALUES (?, ?)", (name, contact))
    conn.commit()
    conn.close()

def get_all_members():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM members")
    members = cur.fetchall()
    conn.close()
    return members

# ISSUE & RETURN OPERATIONS
def issue_book(book_id, member_id):
    conn = connect_db()
    cur = conn.cursor()

    # Check if book exists and quantity > 0
    cur.execute("SELECT quantity FROM books WHERE book_id = ?", (book_id,))
    book = cur.fetchone()
    if not book or book[0] <= 0:
        conn.close()
        return False

    # Reduce quantity by 1
    cur.execute("UPDATE books SET quantity = quantity - 1 WHERE book_id = ?", (book_id,))

    # Insert issue record
    issue_date = datetime.now().strftime("%Y-%m-%d")
    cur.execute("""
        INSERT INTO issued_books (book_id, member_id, issue_date)
        VALUES (?, ?, ?)
    """, (book_id, member_id, issue_date))

    conn.commit()
    conn.close()
    return True

def return_book(issue_id):
    conn = connect_db()
    cur = conn.cursor()

    # Get issued book
    cur.execute("SELECT book_id FROM issued_books WHERE issue_id = ?", (issue_id,))
    result = cur.fetchone()
    if not result:
        conn.close()
        return False

    book_id = result[0]

    # Set return date
    return_date = datetime.now().strftime("%Y-%m-%d")
    cur.execute("UPDATE issued_books SET return_date = ? WHERE issue_id = ?", (return_date, issue_id))

    # Increase book quantity by 1
    cur.execute("UPDATE books SET quantity = quantity + 1 WHERE book_id = ?", (book_id,))

    conn.commit()
    conn.close()
    return True

def get_issued_books():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT issued_books.issue_id, books.title, members.name, issued_books.issue_date, issued_books.return_date
        FROM issued_books
        JOIN books ON issued_books.book_id = books.book_id
        JOIN members ON issued_books.member_id = members.member_id
    """)
    issued = cur.fetchall()
    conn.close()
    return issued