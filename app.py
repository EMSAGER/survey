from surveys import Survey
from flask import Flask, request, render_template,  redirect, flash,  jsonify, session
from random import randint,  choice, sample
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = "potatolife"
debug = DebugToolbarExtension(app)

RESPONSES = []

@app.route('/')
def index():
    "Set up home page"
    title = Survey.title
    instructions = Survey.instructions
    return render_template("home.html", title=title, instructions=instructions)