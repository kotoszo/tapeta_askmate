from flask import Flask, request, render_template, url_for
import config
import logic

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/list', methods=['GET', 'POST'])
def index():
    display = logic.display_questions()
    return render_template('index.html', display=display)


@app.route('/question/<int:question_id>')
def question(question_id):
    questions = logic.display_question(question_id)
    return render_template("question.html", questions=questions)

'''
@app.route('/<theme>', methods=['GET', 'POST'])
@app.route('/<theme>/<question_id>/edit', methods=['GET', 'POST'])
def form(question_id=None, theme=None):
    display = logic.display_questions()
    if question_id is not None:
        answered = logic.display_question(question_id)
    return render_template('form.html', theme=theme, question=display, question_id=question_id, answered=answered)
'''


@app.route('/new-question', methods=['GET', 'POST'])
@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
def show_form(question_id=None):
    if question_id:
        theme = 'question'
        data = logic.display_question(question_id, answers=False)
    else:
        data = None
        theme = 'new-question'
    return render_template('form.html', theme=theme, question=data)


@app.errorhandler(404)
def page_not_found(error):
    return 'Oops, page not found!', 404


if __name__ == '__main__':
    app.run(debug=True)
