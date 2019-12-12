import flask
import random
import model
import string
import hashlib
import uuid
import datetime

from flask import request
from flask import url_for

app = flask.Flask(__name__)
db = model.db

db.create_all()

hasher = hashlib.blake2b()

def hash_password(password):
    hasher = hashlib.sha512()
    password = password.encode('utf-8')
    hasher.update(password)
    return hasher.hexdigest()

N_USERS = 10
N_RECIPES = 10
N_BOOKS = 10

def require_session_token(func):
    """Decorator to require authentication to access routes"""
    def wrapper(*args, **kwargs):
        session_token = flask.request.cookies.get("session_token")
        redirect_url = flask.request.path or '/'
        if not session_token:
            app.logger.error('no token in request')
            return flask.redirect(flask.url_for('login', redirectTo=redirect_url))
        user = db.query(model.User).filter_by(session_token=session_token).filter(model.User.session_expiry_datetime>=datetime.datetime.now()).first()
        if not user:
            app.logger.error(f'token {session_token} not valid')
            return flask.redirect(flask.url_for('login', redirectTo=redirect_url))
        app.logger.info(f'authenticated user {user.username} with token {user.session_token} valid until {user.session_expiry_datetime.isoformat()}')
        flask.request.user = user
        return func(*args, **kwargs)

    # Renaming the function name:
    # wrapper.__name__ = func.__name__
    return wrapper

def create_dummy_users():
    users = []
    for x in range(N_USERS):
        name = "".join(random.choices(string.ascii_lowercase, k=6))
        user = model.User(username=name, email=f"{name}@irgendwas.at", password=hash_password(name))
        users.append(user)

    my_user = model.User(username="admin", email="admin@irgendwas.at", password=hash_password("admin"))
    users.append(my_user)
    test_user = model.User(username="test", email="test@irgendwas.at", password=hash_password("test"))
    users.append(test_user)


    for user in users:
        if not db.query(model.User).filter_by(username=user.username).first():
            db.add(user)

    db.commit()


def create_dummy_recipes():
    recipes = []
    for x in range(N_RECIPES):
        name = "".join(random.choices(string.ascii_lowercase, k=10))
        name = name.capitalize()
        description = "".join(random.choices(string.ascii_lowercase + "   ", k=80))
        taste = "".join(random.choices(string.ascii_lowercase, k=5))
        recipes.append(model.Recipe(name=name, description=description, taste=taste))

    recipe_1 = model.Recipe(name="Apfelstrudel", description="Cut Apple Bake Sweet", taste="sweet")
    recipes.append(recipe_1)
    recipe_2 = model.Recipe(name="Hamburger", description="Fry Meat And Eat", taste="salty")
    recipes.append(recipe_2)
    recipe_3 = model.Recipe(name="Suppe", description="Cut carrots Add Water", taste="sweet")
    recipes.append(recipe_3)

    for r in recipes:
        if not db.query(model.Recipe).filter_by(name=r.name).first():
            db.add(r)

    db.commit()


def create_dummy_books():
    books = []
    for x in range(N_BOOKS):
        title = "".join(random.choices(string.ascii_lowercase, k=10))
        title = title.capitalize()
        author = "".join(random.choices(string.ascii_lowercase + " ", k=20))
        genre = "".join(random.choices(string.ascii_lowercase, k=5))
        books.append(model.Book(title=title, author=author, genre=genre))
    db.add_all(books)
    db.commit()


def add_dummy_data():
    create_dummy_users()
    create_dummy_recipes()


@app.route("/")
def index():
    return flask.render_template("index.html", myname="Stefan")


@app.route("/barber")
def barber():
    return flask.render_template("barber.html")


@app.route("/secret-number-game")
def secret_number_game():
    return flask.render_template("secret-number-game.html", secret_number=random.randint(0, 10))


@app.route("/blog")
def blog():
    db_recipes = db.query(model.Recipe).filter_by(taste="sweet").all()
    return flask.render_template("blog.html", recipes=db_recipes)

@app.route("/register-books", methods = ["GET", "POST"])
def register_books():

    current_request = flask.request

    if current_request.method == "GET":
        return flask.render_template("register-books.html")

    elif current_request.method == "POST":
        #todo: register valid user
        title = current_request.form.get("title")
        author = current_request.form.get("author")
        genre = current_request.form.get("genre")
        title_exist = db.query(model.Book).filter_by(book=books).first()
        if title_exist:
            print("Book already exists")
        else:
            new_book = model.Book(title=title, author=author, genre=genre)
            db.add(new_book)
            db.commit()
            return flask.redirect(flask.url_for("register-books"))

@app.route("/books")
def books():
    all_books = db.query(model.Book).all()
    return flask.render_template("books.html", books=all_books)

@app.route("/books/<book_id>/delete", methods=["GET", "POST"])
def books_delete(book_id):
    book_to_delete = db.query(model.Book).get(book_id)
    if book_to_delete is None:
        return flask.redirect(flask.url_for('books'))

    current_request = flask.request
    if current_request.method == "GET":
        return flask.render_template("books-delete.html", book=book_to_delete)
    elif current_request.method == "POST":
        db.delete(book_to_delete)
        db.commit()
        return flask.redirect(flask.url_for('books'))
    else:
        return flask.redirect(flask.url_for('books'))

@app.route("/register", methods = ["GET", "POST"])
def register():

    current_request = flask.request

    if current_request.method == "GET":
        return flask.render_template("register.html")

    elif current_request.method == "POST":
        #todo: register valid user
        email = current_request.form.get("email")
        username = current_request.form.get("username")
        password = current_request.form.get("password")
        user_exist = db.query(model.User).filter_by(username=username).first()
        email_exist = db.query(model.User).filter_by(email=email).first()
        if user_exist:
            print("User already exists")
        elif email_exist:
            print("Email already exists")
        else:
            new_user = model.User(username=username, email=email, password=hash_password(password))
            db.add(new_user)
            db.commit()
            return flask.redirect(flask.url_for("register"))

@app.route("/accounts")
@require_session_token
def accounts():
    all_user = db.query(model.User).all()
    return flask.render_template("accounts.html", accounts=all_user)

@app.route("/accounts/<account_id>/delete", methods=["GET", "POST"])
def accounts_delete(account_id):
    user_to_delete = db.query(model.User).get(account_id)
    if user_to_delete is None:
        return flask.redirect(flask.url_for('accounts'))

    current_request = flask.request
    if current_request.method == "GET":
        return flask.render_template("accounts-delete.html", account=user_to_delete)
    elif current_request.method == "POST":
        db.delete(user_to_delete)
        db.commit()
        return flask.redirect(flask.url_for('accounts'))
    else:
        return flask.redirect(flask.url_for('accounts'))

@app.route("/accounts/<account_id>/edit", methods=["GET", "POST"])
def accounts_edit(account_id):
    user_to_edit = db.query(model.User).get(account_id)

    if user_to_edit is None:
        return flask.redirect(flask.url_for('accounts'))

    current_request = flask.request
    if current_request.method == "GET":
        return flask.render_template("accounts-edit.html", account=user_to_edit)
    elif current_request.method == "POST":
        email = current_request.form.get('email')
        username = current_request.form.get('username')

        user_to_edit.email = email
        user_to_edit.username = username

        db.add(user_to_edit)
        db.commit()
        return flask.redirect(flask.url_for('accounts'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    current_request = flask.request
    if current_request.method=='GET':
        return flask.render_template('login.html')
    elif current_request.method == 'POST':
        email = current_request.form.get('email')
        password = current_request.form.get('password')
        user = db.query(model.User).filter_by(email=email).first()
        if user is None:
            print("User does not exist")
            return flask.redirect(flask.url_for('login'))
        else:
            if hash_password(password) == user.password:
                #find redirect method from request argument
                redirect_url = current_request.args.get('redirectTo', '/')

                #generate token and expiry time in 1 hour from now
                session_token = str(uuid.uuid4())
                session_expiry_datetime = datetime.datetime.now() + datetime.timedelta(seconds=3600)
                #update user with new session token and expiry
                user.session_token = session_token
                user.session_expiry_datetime = session_expiry_datetime
                #save in DB
                db.add(user)
                db.commit()

                #make response and add cookie with session token
                response = flask.make_response(flask.redirect(redirect_url))
                response.set_cookie('session_token', session_token)
                return response
            else:
                return flask.redirect(flask.url_for('forbidden'))


@app.route("/forbidden")
def forbidden():
    return flask.render_template("forbidden.html")


@app.route("/logout")
def logout():
    #get session token
    current_request = flask.request
    session_token = current_request.cookies.get('session_token')
    if not session_token:
        #todo: use redirect url to get back to this page after login
        return flask.redirect(flask.url_for('login'))
    user = db.query(model.User).filter_by(session_token=session_token).first()
    if not user:
        return flask.redirect(flask.url_for('login'))
    if user and not user.session_expiry_datetime>datetime.datetime.now():
        return flask.redirect(flask.url_for('login'))

    #return token from db and browser cookie
    user.session_token = None
    user.session_expiry_datetime = None
    db.add(user)
    db.commit()

    return flask.redirect(flask.url_for('login'))


if __name__ == '__main__':
    add_dummy_data()
    app.run()
