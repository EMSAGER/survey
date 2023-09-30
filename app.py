from surveys import satisfaction_survey as survey
from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension

    #initialize a variable called responses to be an empty list. As people store their answers

RESPONSES = []

app = Flask(__name__)

app.config['SECRET_KEY'] = "potatolife"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)



@app.route("/")
def index():
    "Set up home page"
    return render_template("home.html", survey=survey)

@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the response list & begin survey """
    RESPONSES.clear()
    return redirect("/question/0")


@app.route("/answer", methods=["POST"])
def record_answer():
    """Store each question's answer in the RESPONSE list"""
    choice = request.form['answer']
    RESPONSES.append(choice)
        #two options for the survey: either its completed or it needs to load the next question. 
    if (len(RESPONSES) == len(survey.questions)):
            #survey is complete
        return render_template("/complete.html")
    else:
        #load the next survey question
            #how to get the next questions based on location
            #use the length of responses to determine the question number & f statements
        return redirect(f"/question/{len(RESPONSES)}")
    
@app.route("/question/<int:qid>")
def questions(qid):
    """Show each survey question on an individual page"""
    if RESPONSES is None:
        return render_template("/")

    if (len(RESPONSES) == len(survey.questions)):
            #survey is complete
        return render_template("/complete.html")
    
    if(len(RESPONSES)) != qid:
        flash(f"Question skipping is not allowed. Invalid question id: {qid}.", 'error')
        return redirect(f"/question/{len(RESPONSES)}")
  
    questions = survey.questions[qid]
    return render_template("question.html", question_num=qid, question=questions)

@app.route("/complete")
def completed_survey():
    return render_template("complete.html")