from surveys import satisfaction_survey as survey
from flask import Flask, request, render_template, redirect
# from random import randint,  choice, sample
from flask_debugtoolbar import DebugToolbarExtension

    #initialize a variable called responses to be an empty list. As people store their answers

responses = []

app = Flask(__name__)

app.config['SECRET_KEY'] = "potatolife"
debug = DebugToolbarExtension(app)



@app.route("/")
def index():
    "Set up home page"
    return render_template("home.html", survey=survey)

@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the response list & begin survey """
    responses.clear()
    return redirect("/question/0")

@app.route("/question/<int:qid>")
def questions(qid):
    """Show each survey question on an individual page"""
    question = survey.question[qid]
    return render_template("question.html", question_num=qid, question=question, survey=survey)