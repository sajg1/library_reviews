from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library-reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# SQLAlchemy class for book table
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=True)
    author = db.Column(db.String(250), nullable=True)
    rating = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<Book {self.title} >"

# used initially to create the database
# db.create_all()


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    if len(all_books) > 0:
        return render_template('index.html', library=all_books, empty=False)
    else:
        return render_template('index.html', empty=True)


@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        newBook = Book(title=request.form['title'],
                       author=request.form['author'],
                       rating=request.form['rating'])
        db.session.add(newBook)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route("/edit/<id>", methods=['POST', 'GET'])
def edit_rating(id):
    book = Book.query.get(id)
    if request.method == 'GET':
        return render_template('edit.html', book=book)
    book.rating = request.form['new-rating']
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

