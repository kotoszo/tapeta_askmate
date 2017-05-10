from flask import Flask, request, render_template, url_for
import file_io

app = Flask(__name__)


def base():
    return render_template('base.html')


@app.route('/question/<question_id>/edit')
@app.route('/answer/<answer_id>/edit')
@app.route('/new-question')
@app.route('/new-answer')
def form():
    return render_template('form.html')


@app.route('/question/<question_id>')
def question():
    return render_template('question.html')


@app.route('/')
@app.route('/list')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)