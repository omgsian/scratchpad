from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import (
    login_user,
    LoginManager,
    UserMixin,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = (
    "mysql+mysqlconnector://omgwhut:{password}@{hostname}/{databasename}".format(
        username="omgwhut",
        password="mrh1990x",
        hostname="omgwhut.mysql.pythonanywhere-services.com",
        databasename="omgwhut$comments",
    )
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = "cats_best"
login_manager = LoginManager()
login_manager.init_app(app)

# comments = ["hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello", "hello2", ]


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
    posted = db.Column(db.DateTime, default=datetime.now)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template(
            "main_page.html", comments=Comment.query.all(), timestamp=datetime.now()
        )

    if not current_user.is_authenticated:
        return redirect(url_for("index"))

    comment = Comment(content=request.form["contents"])
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html", error=False)

    user = load_user(request.form["username"])
    if user is None:
        return render_template("login_page.html", error=True)

    if not user.check_password(request.form["password"]):
        return render_template("login_page.html", error=True)

    login_user(user)
    return redirect(url_for("index"))


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/header/")
def show_header():
    return render_template("header.html")


if __name__ == "__main__":
    app.run(debug=True)
