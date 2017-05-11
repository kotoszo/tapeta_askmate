import file_io
import config
import base64
import datetime
import time
import sys


def display_questions():
    questions = file_io.read_from_file(config.questions)
    if len(questions):
        questions = sorted(questions, key=lambda x: -int(x[1]))
        result = format_questions(questions)
    else:
        result = False
    return result


def display_question(id, answers=True):
    questions = file_io.read_from_file(config.questions)
    question_to_show = [line for line in questions if int(line[0]) == int(id)]
    if len(question_to_show):
        if answers is True:
            answers = file_io.read_from_file(config.answers)
            answers = [line for line in answers if int(line[3]) == int(id)]
            answers = sorted(answers, key=lambda x: -int(x[1]))
            result = {'question': format_questions(question_to_show), 'answers': format_answers(answers)}
        elif answers is False:
            result = {'question': format_questions(question_to_show)[0]}
        else:
            raise ValueError
    else:
        result = False
    return result


def get_question_by_answer_id(answer_id):
    answers_table = file_io.read_from_file(config.answers)
    answer = [line for line in answers_table if int(answer_id) == int(line[0])]
    questions_table = file_io.read_from_file(config.questions)
    question = [line for line in questions_table if int(answer[0][3]) == int(line[0])]
    result = {'question': format_questions(question), 'answers': format_answers(answer)}
    print(result, sys.stderr)
    return result


def format_questions(questions, mode='frontend'):
    '''
    Formats questions
    '''
    if mode == 'frontend':
        result = [[line[0], date_convert(line[1]), line[2], line[3], b64_convert(line[4]),
                  b64_convert(line[5]), b64_convert(line[6])] for line in questions]
    elif mode == 'backend':
        result = [[line[0], date_convert(line[1], decode=True), line[2], line[3], b64_convert(line[4], decode=True),
                  b64_convert(line[5], decode=True), b64_convert(line[6], decode=True)]
                  for line in questions]
    else:
        raise ValueError
    return result


def format_answers(answers, mode='frontend'):
    '''
    Formats answers
    '''
    if mode == 'frontend':
        result = [[line[0], date_convert(line[1]), line[2], b64_convert(line[4]),
                  b64_convert(line[5])] for line in answers]
    elif mode == 'backend':
        result = [[line[0], date_convert(line[1], decode=True), line[2], line[3],
                  b64_convert(line[4], decode=True), b64_convert(line[5], decode=True)]
                  for line in answers]
    else:
        raise ValueError
    return result


def process_insert_update(form_data):
    '''
    Handle insert and update requests.
        @param    form_data   POST      Values provided by user.
        @param    questions   boolean   True if processing questions, False if answers
        @return               boolean   True if process is successful, otherwise False
    '''
    status = False
    if int(form_data['typeID']) == 0:
        # questions
        if int(form_data['modID']) == -1:
            if insert_question(form_data):
                status = True
        else:
            if update_question(form_data):
                status = True
    elif int(form_data['typeID']) == 1:
        # answers
        if int(form_data['modID']) == -1:
            if insert_answer(form_data):
                status = True
        else:
            if update_answer(form_data):
                status = True
    else:
        raise ValueError
    return status


def insert_question(form_data):
    table = file_io.read_from_file(config.questions)

    mod_record = [form_data['modID'], str(int(time.time())), '0', '0', b64_convert(form_data['title'], decode=True),
                  b64_convert(form_data['description'], decode=True), '']
    mod_record[0] = str(int(table[len(table) - 1][0]) + 1) if table else 1

    table.append(mod_record)
    status = True if file_io.write_to_file(table, config.questions) else False
    return status


def update_question(form_data):
    table = file_io.read_from_file(config.questions)

    to_be_updated = [line for line in table if int(form_data['modID']) == int(line[0])][0]
    to_be_updated[1] = str(int(time.time()))
    to_be_updated[4] = b64_convert(form_data['title'], decode=True)
    to_be_updated[5] = b64_convert(form_data['description'], decode=True)

    updated_table = [line for line in table if int(form_data['modID']) != int(line[0])]
    updated_table.append(to_be_updated)
    updated_table = sorted(updated_table, key=lambda x: int(x[0]))

    status = True if file_io.write_to_file(updated_table, config.questions) else False
    return status


def insert_answer(form_data):
    table = file_io.read_from_file(config.answers)
    mod_record = [form_data['modID'], str(int(time.time())), '0', form_data['questionID'],
                  b64_convert(form_data['description'], decode=True), '']
    mod_record[0] = str(int(table[len(table) - 1][0]) + 1) if table else 1
    table.append(mod_record)

    status = True if file_io.write_to_file(table, config.answers) else False
    return status


def update_answer(form_data):
    table = file_io.read_from_file(config.answers)

    to_be_updated = [line for line in table if int(form_data['modID']) == int(line[0])][0]
    to_be_updated[1] = str(int(time.time()))
    to_be_updated[4] = b64_convert(form_data['description'], decode=True)

    updated_table = [line for line in table if int(form_data['modID']) != int(line[0])]
    updated_table.append(to_be_updated)
    updated_table = sorted(updated_table, key=lambda x: int(x[0]))

    status = True if file_io.write_to_file(updated_table, config.answers) else False
    return status


def process_delete(id, questions=True):
    '''
    Handle delete requests.
        @param    id          int       The id to be deleted.
        @param    questions   boolean   True if processing questions, False if answers
        @return               boolean   True if process is successful, otherwise False
    '''
    status = False
    if id:
        if questions is True:
            table = file_io.read_from_file(config.questions)
        elif questions is False:
            table = file_io.read_from_file(config.answers)
        else:
            raise ValueError

        # delete record with primary key
        updated_table = [line for line in table if int(line[0]) != int(id)]
        status = True if file_io.write_to_file(
                                              updated_table,
                                              config.questions if questions else config.answers
                                              ) else False
        # delete record(s) with foreign key (cascading delete if deleting questions)
        if questions:
            table_answers = file_io.read_from_file(config.answers)
            updated_answers = [line for line in table_answers if int(line[3]) != int(id)]
            status_answers = True if file_io.write_to_file(updated_answers, config.answers) else False
            status = all(status, status_answers)

    return status


def process_votes(id, questions=True, direction='up'):
    status = False
    if id:
        if direction not in ('up', 'down'):
            raise ValueError

        if questions is True:
            # questions
            table = file_io.read_from_file(config.questions)
            updated_record = [[line[0], line[1], line[2],
                              str(int(line[3]) + 1) if direction == 'up' else str(int(line[3]) - 1),
                              line[4], line[5], line[6]] for line in table if int(id) == int(line[0])]
            updated_table = [line for line in table if int(id) != int(line[0])]
        elif questions is False:
            # answers
            table = file_io.read_from_file(config.answers)
            updated_record = [[line[0], line[1],
                              str(int(line[2]) + 1) if direction == 'up' else str(int(line[2]) - 1),
                              line[3], line[4], line[5]] for line in table if int(id) == int(line[0])]
            updated_table = [line for line in table if int(id) != int(line[0])]
        else:
            raise ValueError

        updated_table.append(updated_record[0])
        updated_table = sorted(updated_table, key=lambda x: int(x[0]))
        status = True if file_io.write_to_file(updated_table,
                                               config.questions if questions else config.answers) else False
    return status


def process_view_number():
    pass


def sort_table(table):
    pass


def file_upload():
    pass


def b64_convert(text, decode=False):
    if decode is True:
        result = base64.b64encode(bytearray(text, encoding="utf-8")).decode("utf-8")
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
