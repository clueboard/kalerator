# coding=UTF-8
from flask import Flask


app = Flask(__name__)

# Import any views we have here
from . import views  # noqa


# A simple "is the app up" URL
@app.route("/healthcheck")
def healthcheck():
    return "GOOD"
