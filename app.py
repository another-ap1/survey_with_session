from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "anchoviesIsTheSecretSauce"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def home_page():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template("home.html", title=title, instructions=instructions)

@app.route('/question/<int:numq>')
def show_question(numq):
    if len(responses) == len(satisfaction_survey.questions):
        return render_template("finished.html", responses=responses)
    if numq > len(satisfaction_survey.questions):
        responses.clear()
        flash("INVALD: number outside of range")
        return redirect('/')
    else:
        question = satisfaction_survey.questions[numq]
        return render_template("question.html", question=question, question_num = numq)

@app.route('/answer', methods=['POST'])
def get_answer(): 
    choice = request.form['answer']
    responses.append(choice)
    return redirect(f"/question/{len(responses)}")