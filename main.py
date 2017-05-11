from flask import Flask, request, render_template, url_for
import config
import logic
import sys


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/list', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        if not logic.process_insert_update(request.form):
            error = 'An error occured while updating the database!'
    display = logic.display_questions()
    return render_template('index.html', display=display, error=error)


@app.route('/question/<int:question_id>')
def question(question_id):
    questions = logic.display_question(question_id)
    return render_template("question.html", questions=questions)


@app.route('/new-question', methods=['GET', 'POST'])
@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
def show_question_form(question_id=None):
    if question_id:
        theme = 'question'
        data = logic.display_question(question_id, answers=False)
    else:
        data = None
        theme = 'new-question'
    return render_template('form.html', theme=theme, question=data)


@app.route('/question/<int:question_id>/new-answer', methods=['GET', 'POST'])
@app.route('/answer/<int:answer_id>/edit', methods=['GET', 'POST'])
def show_answer_form(answer_id=None, question_id=None):
    if answer_id:
        theme = 'answer'
        data = logic.get_question_by_answer_id(answer_id)
    else:
        data = None
        theme = 'new-answer'
    return render_template('form.html', theme=theme, question=data, question_id=question_id)


@app.errorhandler(404)
def page_not_found(error):
    return 'Oops, page not found!', 404


if __name__ == '__main__':
    app.run(debug=True)
