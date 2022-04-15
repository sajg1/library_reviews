from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

all_books = []


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        newBook = {
            "title": request.form['title'],
            "author": request.form['author'],
            "rating": request.form['rating']
        }
        all_books.append(newBook)
        print(all_books)
        return render_template('add.html')
    else:
        return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)

