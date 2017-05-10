import file_io
import config
import base64
import datetime
import time


def display_questions():
    result = []
    questions = file_io.read_from_file(config.questions)
    if len(questions):
        questions = sorted(questions, key=lambda x: -int(x[1]))
        for line in questions:
            result = [[line[0], date_convert(line[1]), line[2], line[3], b64_convert(line[4]),
                      file_io.change_eol(b64_convert(line[5]))] for line in questions]
    else:
        result = False

    return result


def display_question(id):
    pass


def sort_table():
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
    print(display_questions())
    '''
    dt = date_convert(1284101485, mode=2)
    print(dt)
    dt2 = date_convert(dt, mode=1)
    print(dt2)
    '''

