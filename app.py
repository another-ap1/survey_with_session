from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey

RESPONSES_KEY="responses"

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "anchoviesIsTheSecretSauce"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template("home.html", title=title, instructions=instructions)

@app.route('/start', methods=['POST'])
def start_survey():
    session[RESPONSES_KEY] = []
    return redirect('/question/0')

@app.route('/question/<int:numq>')
def show_question(numq):
    
    responses = session.get(RESPONSES_KEY)
    
    if responses is None:
        redirect('/')
    if len(responses) == len(satisfaction_survey.questions):
        return render_template("finished.html", responses=RESPONSES_KEY)
    if len(responses) != numq:
        flash("INVALD: number outside of range")
        return redirect(f'/questions/{len(responses)}')
    else:
        question = satisfaction_survey.questions[numq]
        return render_template("question.html", question=question, question_num = numq)

@app.route('/answer', methods=['POST'])
def get_answer(): 
    choice = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/finished')
    else:
        return redirect(f"/question/{len(responses)}")
    
@app.route('/finished')
def fin():
    return render_template('finished.html')