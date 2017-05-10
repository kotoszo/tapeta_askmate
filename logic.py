import file_io
import config
import base64
import datetime
import time


def display_questions():
    questions = file_io.read_from_file(config.questions)
    if len(questions):
        questions = sorted(questions, key=lambda x: -int(x[1]))
        result = format_questions(questions)
    else:
        result = False
    return result


def display_question(id):
    questions = file_io.read_from_file(config.questions)
    question_to_show = [line for line in questions if int(line[0]) == int(id)]
    if len(question_to_show):
        answers = file_io.read_from_file(config.answers)
        answers = [line for line in answers if int(line[3]) == int(id)]
        answers = sorted(answers, key=lambda x: -int(x[1]))
        result = {'question': format_questions(question_to_show), 'answers': format_answers(answers)}
    else:
        result = False
    return result


def format_questions(questions):
    result = [[line[0], date_convert(line[1]), line[2], line[3], b64_convert(line[4]),
              file_io.change_eol(b64_convert(line[5])), b64_convert(line[6])] for line in questions]
    return result


def format_answers(answers):
    result = [[line[0], date_convert(line[1]), line[2], file_io.change_eol(b64_convert(line[4])), b64_convert(line[5])]
              for line in answers]
    return result


def sort_table(table):
    pass


def file_upload():
    pass


def b64_convert(text, decode=False):
    if decode is True:
        result = base64.b64encode(text.encode("utf-8"))
    elif decode is False:
        result = base64.b64decode(text).decode("utf-8")
    else:
        raise ValueError
    return result


def date_convert(text, decode=False):
    if decode is True:
        result = int(time.mktime(text.timetuple()))
    elif decode is False:
        result = datetime.datetime.fromtimestamp(int(text)).strftime("%Y-%m-%d %H:%M:%S")
    else:
        raise ValueError
    return result


def main():
    pass

if __name__ == '__main__':
    main()
