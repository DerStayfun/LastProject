import flask
import random
import model

app = flask.Flask(__name__)


@app.route("/")
def index():
    return flask.render_template("index.html", myname="Stefan")

@app.route("/barber")
def barber():
    return flask.render_template("barber.html")

@app.route("/secret-number-game")
def secret_number_game():
    return flask.render_template("secret-number-game.html", secret_number=random.randint(0,10))

@app.route("/blog")
def blog():
    recipe_1 = model.Recipe("Apfelstrudel", "Sweet", "Cut Apple Bake Sweet")
    recipe_2 = model.Recipe("Hamburger", "Fat", "Fry Meat and eat")
    recipe_3 = model.Recipe("Soup", "Tasty", "Cut carrots add water")

    return flask.render_template("blog.html", recipes=[recipe_1, recipe_2, recipe_3])


if __name__ == '__main__':
    app.run()