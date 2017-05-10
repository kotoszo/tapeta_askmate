from flask import Flask, request, render_template, url_for
import file_io
import config
import base64

app = Flask(__name__)


def base():
    return render_template('base.html')


@app.route('/question/<question_id>/edit')
@app.route('/answer/<answer_id>/edit')
@app.route('/new-question')
@app.route('/new-answer')
def form():
    answers = file_io.read_from_file(config.answers)
    questions = file_io.read_from_file(config.questions)
    return render_template('form.html', answer=answers, question=questions)


@app.route('/question/<question_id>')
def question():
    questions = file_io.read_from_file(config.questions)
    answers = file_io.read_from_file(config.answers)
    return render_template('question.html', question=questions, answer=answers)


@app.route('/')
@app.route('/list')
def index():
    questions = file_io.read_from_file(config.questions)
    return render_template('index.html', questions=questions)


if __name__ == '__main__':
    # app.run(debug=True)
    encoded = base64.b64encode("This is something, you wont read again.".encode())
    print(encoded)
    decoded = base64.b64decode(encoded.decode())
    print(decoded)
