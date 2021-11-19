# pylint: disable = C0413, E0401, E1101, W1508

"""
Provides all the functions such as creating a model to store data in the database,
sign up, sign in, sign out, load popular movies / top rated movies, search, detail,
store comment, load comments, calulate avg rating according to each user.
"""
import os
import json
import sys
import flask

sys.path.append("./process")

from flask_login import login_user, current_user, LoginManager, logout_user
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

from tmdb import get_popular_movie, get_top_rated_movie
from search import get_search
from detail import get_detail

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = flask.Flask(__name__, static_folder="./build/static")
# This tells our Flask app to look at the results of `npm build` instead of the
# actual files in /templates when we're looking for the index page file. This allows
# us to load React code into a webpage. Look up create-react-app for more reading on
# why this is necessary.
bp = flask.Blueprint("bp", __name__, template_folder="./build")
# Point SQLAlchemy to your Heroku database
db_url = os.getenv("DATABASE_URL")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = b"I am a secret key!"  # don't defraud my app ok?


##### MODELS #####
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    """
    Initialize the User model to store the registered user.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __repr__(self):
        return f"<User {self.username}>"

    def get_username(self):
        """
        Returns the username value.
        """
        return self.username


class Comment(db.Model):
    """
    Initialize the Comments model to store the comments and ratings that the user
    has commented and rated.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1000))
    date = db.Column(db.String(100))
    hour = db.Column(db.String(100))
    rating = db.Column(db.Integer)

    def __repr__(self):
        return f"<Rating {self.comment}>"

    def get_rating(self):
        """
        Returns the rating value.
        """
        return self.rating


db.create_all()


### ROUTES ###
@bp.route("/index")
def index():
    """
    Get all information about popular movies / top rated movies.
    """
    (
        id_movie,
        poster_path,
        title,
        vote_average,
        release_date,
        popularity,
    ) = get_popular_movie()

    popular_movie = [
        {
            "id_movie": id_movie,
            "poster_path": poster_path,
            "title": title,
            "vote_average": vote_average,
            "release_date": release_date,
            "popularity": popularity,
        }
        for id_movie, poster_path, title, vote_average, release_date, popularity in zip(
            id_movie, poster_path, title, vote_average, release_date, popularity
        )
    ]

    (
        id_movie,
        poster_path,
        title,
        vote_average,
        release_date,
        popularity,
    ) = get_top_rated_movie()

    top_rated_movie = [
        {
            "id_movie": id_movie,
            "poster_path": poster_path,
            "title": title,
            "vote_average": vote_average,
            "release_date": release_date,
            "popularity": popularity,
        }
        for id_movie, poster_path, title, vote_average, release_date, popularity in zip(
            id_movie, poster_path, title, vote_average, release_date, popularity
        )
    ]

    movie_data = {
        "popular_movie": popular_movie,
        "top_rated_movie": top_rated_movie,
        "username": current_user.username,
    }
    data = json.dumps(movie_data)

    return flask.render_template(
        "index.html",
        data=data,
    )


app.register_blueprint(bp)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_name):
    """
    Load user given an id.
    """
    return User.query.get(user_name)


@app.route("/signout", methods=["POST"])
def logout():
    """
    Log out of the current account and return to the login page.
    """
    logout_user()
    return flask.redirect(flask.url_for("login"))


@app.route("/signup")
def signup():
    """
    Render a signup page.
    """
    return flask.render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    """
    Get username from input text, check if this username is registered or not.
    If registered, do not allow that username to be saved to the database.
    Otherwise, allow that username to be saved to the database.
    Finally, it will go to the login page.
    """
    username = flask.request.form.get("username")
    email = flask.request.form.get("email")
    password = flask.request.form.get("password")
    user = User.query.filter_by(email=email).first()
    if user:
        pass
    else:
        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password, method="sha256"),
        )
        db.session.add(user)
        db.session.commit()

    return flask.redirect(flask.url_for("login"))


@app.route("/login")
def login():
    """
    Render a login page.
    """
    return flask.render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    """
    Get email and password from input text, check if this email and this password are registered
    or not. If registered, it will go to the index page. Otherwise, show error message.
    """
    email = flask.request.form.get("email")
    password = flask.request.form.get("password")
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return flask.redirect(flask.url_for("bp.index"))
    return flask.jsonify({"status": 401, "reason": "Username or Password Error"})


@app.route("/")
def main():
    """
    If the user has logged in before, it will go to the index page.
    Otherwise, it will stay at the login page.
    """
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("bp.index"))
    return flask.redirect(flask.url_for("login"))


@app.route("/detail", methods=["POST"])
def detail():
    """
    Get all details of a movie.
    """
    data = get_detail(current_user.username)
    return flask.jsonify({"status": 200, "detail": data})


@app.route("/search", methods=["POST"])
def search():
    """
    Search for information of a movie through keyword.
    """
    data = get_search()
    print(data)
    return flask.jsonify({"status": 200, "search": data})


@app.route("/comment", methods=["POST"])
def save_comment():
    """
    Store all information of comments that belong to a movie from the database.
    """
    username = current_user.username
    movie_id = flask.request.json.get("movie_id")
    comment_movie = flask.request.json.get("comment_movie")
    date_comment = flask.request.json.get("date")
    hour_comment = flask.request.json.get("hour")
    rating = flask.request.json.get("rating")

    db.session.add(
        Comment(
            username=username,
            movie_id=movie_id,
            comment=comment_movie,
            date=date_comment,
            hour=hour_comment,
            rating=rating,
        )
    )
    db.session.commit()

    return flask.jsonify({"status": 200, "message": "Successful"})


@app.route("/all_comment", methods=["POST"])
def get_all_comment():
    """
    Get all information of comments that belong to a movie from the database.
    """
    movie_id = flask.request.json.get("movie_id")

    query_comment = Comment.query.filter_by(movie_id=movie_id).all()

    name = []
    comment = []
    date = []
    hour = []
    rating = []

    for item in query_comment:
        name.append(item.username)
        comment.append(item.comment)
        date.append(item.date)
        hour.append(item.hour)
        rating.append(item.rating)

    all_comment = [
        {
            "name": name,
            "date": date,
            "hour": hour,
            "comment": comment,
            "rating": rating,
        }
        for name, date, hour, comment, rating in zip(name, date, hour, comment, rating)
    ]
    comment_data = {"comment": all_comment}
    data = json.dumps(comment_data)

    return flask.jsonify({"status": 200, "all_comment": data})


@app.route("/avg_rating", methods=["POST"])
def get_avg_rating():
    """
    Get all ratings that belong to a movie from the database, then calculate its average value.
    This value will be rounded.
    """
    movie_id = flask.request.json.get("movie_id")

    query_comment = Comment.query.filter_by(movie_id=movie_id).all()

    rating = []

    for item in query_comment:
        rating.append(item.rating)

    if len(rating) > 0:
        avg_rating = round(sum(rating) / len(rating))
    else:
        avg_rating = 0

    return flask.jsonify({"status": 200, "avg_rating": avg_rating})


app.run(
    host=os.getenv("IP", "0.0.0.0"),
    port=int(os.getenv("PORT", 8081)),
)
