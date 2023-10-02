from surveys import satisfaction_survey as survey
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

    #initialize a variable called responses to be an empty list. As people store their answers

RESPONSES_TODOS = "responses"

app = Flask(__name__)

app.config['SECRET_KEY'] = "potatolife"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def index():
    "Set up home page"
    return render_template("/home.html", survey=survey)

@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the response list & begin survey """
    #RESPONSES.clear()
    session[RESPONSES_TODOS] = []
    
    return redirect("/question/0")


@app.route("/answer", methods=["POST"])
def record_answer():
    """Store the response in the session and redirect to the next question"""
        #get the response and save it to a variable
    choice = request.form['answer']

    responses = session[RESPONSES_TODOS]
    responses.append(choice)
    session[RESPONSES_TODOS] = responses
        #two options for the survey: either its completed or it needs to load the next question. 
    if (len(responses) == len(survey.questions)):
            #survey is complete
        return render_template("/complete.html")
    else:
        #load the next survey question
            #how to get the next questions based on location
            #use the length of responses to determine the question number & f statements
        return redirect(f"/question/{len(responses)}")
    
@app.route("/question/<int:qid>")
def questions(qid):
    """Show each survey question on an individual page"""
    responses = session.get(RESPONSES_TODOS)

    if (responses is None):
        return redirect("/home.html")

    if (len(responses) == len(survey.questions)):
            #survey is complete
        return render_template("/complete.html")
    
    if(len(responses)) != qid:
        flash(f"Question skipping is not allowed. Invalid question id: {qid}.", 'error')
        return redirect(f"/question/{len(responses)}")
  
    questions = survey.questions[qid]
    return render_template("question.html", question_num=qid, question=questions)

@app.route("/complete")
def completed_survey():
    return render_template("complete.html")