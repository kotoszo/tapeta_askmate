import file_io
import config
import base64


def display_questions():
    order_by = 1
    questions = file_io.read_from_file(config.questions)
    if len(questions):
        result = sorted(file_io.read_from_file(config.questions), key=lambda x: -int(x[1]))
    else:
        result = False
    return result


def display_question():
    pass


def sort_table():
    pass


def b64_convert(text, mode=1):
    if mode == 1:
        result = base64.b64encode(text.encode("utf-8"))
    elif mode == 2:
        result = base64.b64decode(text).decode("utf-8")
    else:
        raise ValueError
    return result


def main():
    pass

if __name__ == '__main__':
    main()
