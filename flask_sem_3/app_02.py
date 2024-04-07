# Задание №2
# Создать базу данных для хранения информации о книгах в библиотеке.
# База данных должна содержать две таблицы: "Книги" и "Авторы".
# В таблице "Книги" должны быть следующие поля: id, название, год издания,
# количество экземпляров и id автора.
# В таблице "Авторы" должны быть следующие поля: id, имя и фамилия.
# Необходимо создать связь между таблицами "Книги" и "Авторы".
# Написать функцию-обработчик, которая будет выводить список всех книг с
# указанием их авторов.
from flask import Flask, render_template
from models_02 import db, Author, Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db.init_app(app)

@app.route('/')
def index():


    return 'Привет'

@app.cli.command('init-db')
def init_db():


    db.create_all()

@app.cli.command("fill-db")
def fill_tables():
    for book_id in range(1, 100):
        title = f"Название {book_id}"
        year = 1920 + book_id
        copies = 10 + book_id
        author_id = book_id

        author = Author(firstname=f"Имя {author_id}", lastname=f"Фамилия {author_id}")
        db.session.add(author)
        db.session.commit()

        book = Book(title=title, year=year, copies=copies, author_id=author.id)
        db.session.add(book)
        db.session.commit()


@app.route('/books/')
def get_books_with_authors():
    books = Book.query.all()
    result = []
    for book in books:
        result.append({
            'title': book.title,
            'author': f'{book.author.first_name} {book.author.last_name}',
            'year': book.year,
            'copies': book.copies
        })
    return render_template('books.html', books=result)

if __name__ == '__main__':
    app.run(debug=True)