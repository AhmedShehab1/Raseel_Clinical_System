from flask import render_template, redirect, url_for
from web_flask import app
from web_flask.forms import LoginForm


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for("index"))
    return render_template("login.html", title="Login - Raseel", form=form)


@app.route("/")
def index():
    return render_template("index.html", title="Home - Raseel")
