from flask import Flask, render_template, request, redirect, url_for
import lms_core

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

# ✅ Add Book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        publisher = request.form['publisher']
        genre = request.form['genre']
        quantity = int(request.form['quantity'])
        lms_core.add_book(title, author, publisher, genre, quantity)
        return redirect(url_for('view_books'))
    return render_template('add_book.html')

# ✅ View Books (Sorted)
@app.route('/view_books')
def view_books():
    books = lms_core.get_all_books()
    sorted_books = lms_core.bubble_sort_books(books)
    return render_template('view_books.html', books=sorted_books)

# ✅ Search Book by Title
@app.route('/search_book', methods=['GET', 'POST'])
def search_book():
    books = []
    if request.method == 'POST':
        title = request.form['title']
        books = lms_core.search_books_by_title(title)
    return render_template('search_book.html', books=books)

# ✅ Delete Book
@app.route('/delete_book', methods=['GET', 'POST'])
def delete_book():
    if request.method == 'POST':
        book_id = int(request.form['book_id'])
        lms_core.delete_book(book_id)
        return redirect(url_for('view_books'))
    books = lms_core.get_all_books()
    return render_template('delete_book.html', books=books)

# ✅ Add Member
@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        lms_core.add_member(name, contact)
        return redirect(url_for('view_members'))
    return render_template('add_member.html')

# ✅ View Members
@app.route('/view_members')
def view_members():
    members = lms_core.get_all_members()
    return render_template('view_members.html', members=members)

# ✅ Issue Book
@app.route('/issue_book', methods=['GET', 'POST'])
def issue_book():
    if request.method == 'POST':
        book_id = int(request.form['book_id'])
        member_id = int(request.form['member_id'])
        lms_core.issue_book(book_id, member_id)
        return redirect(url_for('view_books'))
    books = lms_core.get_all_books()
    members = lms_core.get_all_members()
    return render_template('issue_book.html', books=books, members=members)

# ✅ Return Book
@app.route('/return_book', methods=['GET', 'POST'])
def return_book():
    issued = [i for i in lms_core.get_issued_books() if i[4] is None]
    if request.method == 'POST':
        issue_id = int(request.form['issue_id'])
        lms_core.return_book(issue_id)
        return redirect(url_for('view_issued_books'))
    return render_template('return_book.html', issued=issued)

# ✅ View Currently Issued Books
@app.route('/view_issued_books')
def view_issued_books():
    issued = [i for i in lms_core.get_issued_books() if i[4] is None]
    return render_template('view_issued_books.html', issued=issued)

# ✅ View Issue & Return History
@app.route('/view_history')
def view_history():
    history = lms_core.get_issued_books()
    return render_template('view_history.html', history=history)

if __name__ == '__main__':
    lms_core.setup_db()  # Make sure DB tables exist!
    app.run(debug=True)