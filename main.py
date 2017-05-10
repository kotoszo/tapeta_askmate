from flask import Flask, request, render_template, url_for
import file_io
import config
import base64
import logic

app = Flask(__name__)


def base():
    return render_template('base.html')


@app.route('/question/<question_id>/edit', methods=['POST'])
@app.route('/answer/<answer_id>/edit', methods=['POST'])
@app.route('/new-question', methods=['POST'])
@app.route('/new-answer', methods=['POST'])
def form():
    answers = file_io.read_from_file(config.answers)
    questions = file_io.read_from_file(config.questions)
    return render_template('form.html', answer=answers, question=questions)


@app.route('/question/<question_id>')
def question():
    questions = file_io.read_from_file(config.questions)
    answers = file_io.read_from_file(config.answers)
    return render_template('question.html', question=questions, answer=answers)


@app.route('/', methods=['GET', 'POST'])
@app.route('/list', methods=['GET', 'POST'])
def index():
    display = logic.display_questions()
    return render_template('index.html', display=display)


if __name__ == '__main__':
    app.run(debug=True)
