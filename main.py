from flask import Flask, request, render_template, url_for

app = Flask(__name__)


@app.route('/')
def base():
    return render_template('base.html')


@app.route('/')
def form():
    return render_template('form.html')


@app.route('/')
def question():
    return render_template('question.html')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)