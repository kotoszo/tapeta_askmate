from flask import Flask, request, render_template, url_for
import file_io
import config
import base64
import logic

app = Flask(__name__)


def base():
    return render_template('base.html')


@app.route('/<theme>', methods=['GET', 'POST'])
@app.route('/<theme>/<item_id>/edit', methods=['GET', 'POST'])
def form(question_id=None, answer_id=None, theme=None, item_id=None):
    answers = logic.display_answers()
    display = logic.display_questions()
    return render_template('form.html', theme=theme, question=display, answers=answers,
                           answer_id=answer_id, question_id=question_id, item_id=item_id)


@app.route('/question/<question_id>')
def question(question_id):
    questions = logic.display_questions()
    answers = logic.display_answers()
    return render_template("question.html", question_id=question_id, questions=questions, answers=answers)


@app.route('/', methods=['GET', 'POST'])
@app.route('/list', methods=['GET', 'POST'])
def index():
    display = logic.display_questions()
    return render_template('index.html', display=display)


if __name__ == '__main__':
    app.run(debug=True)
