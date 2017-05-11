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


def format_questions(questions, mode='frontend'):
    '''
    Formats questions
    '''
    if mode == 'frontend':
        result = [[line[0], date_convert(line[1]), line[2], line[3], b64_convert(line[4]),
                  file_io.change_eol(b64_convert(line[5])), b64_convert(line[6])] for line in questions]
    elif mode == 'backend':
        result = [[line[0], date_convert(line[1], decode=True), line[2], line[3], b64_convert(line[4], decode=True),
                  file_io.change_eol(b64_convert(line[5], decode=True), mode=1), b64_convert(line[6], decode=True)]
                  for line in questions]
    else:
        raise ValueError
    return result


def format_answers(answers, mode='frontend'):
    '''
    Formats answers
    '''
    if mode == 'frontend':
        result = [[line[0], date_convert(line[1]), line[2], file_io.change_eol(b64_convert(line[4])),
                  b64_convert(line[5])] for line in answers]
    elif mode == 'backend':
        result = [[line[0], date_convert(line[1], decode=True), line[2], line[3],
                  file_io.change_eol(b64_convert(line[4], decode=True), mode=1), b64_convert(line[5], decode=True)]
                  for line in answers]
    else:
        raise ValueError
    return result


def process_insert_update(form_data, questions=True):
    '''
    Handle insert and update requests.
        @param    form_data   POST      Values provided by user.
        @param    questions   boolean   True if processing questions, False if answers
        @return               boolean   True if process is successful, otherwise False
    '''
    if questions is True:
        # questions
        table = file_io.read_from_file(config.questions)
        #### CHANGE FIELD NAMES!!!!!!!!!!!!!!!!!
        names = ['modID', 'storyTitle', 'userStory', 'criteria', 'businessValue', 'estimation', 'status']
    elif questions is False:
        # answers
        table = file_io.read_from_file(config.answers)
        #### CHANGE FIELD NAMES!!!!!!!!!!!!!!!!!
        names = ['modID', 'storyTitle', 'userStory', 'criteria', 'businessValue', 'estimation', 'status']
    else:
        raise ValueError

    form_data['submission_time'] = int(time.time())
    mod_record = [form_data[name] for name in names]
    mod_record = format_questions(mod_record) if questions else format_answers(mod_record)

    if int(form_data['modID']) == -1:
        # insert
        mod_record[0] = str(int(table[len(table) - 1][0]) + 1) if table else 1
        table.append(mod_record)
        updated_table = table
    else:
        # update
        updated_table = [record for record in table if record[0] != mod_record[0]]
        updated_table.append(mod_record)
        updated_table = sorted(updated_table, key=lambda x: int(x[0]))

    status = True if fileio.write_to_file(updated_table, config.questions) else False
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
            table = fileio.read_from_file(config.questions)
        elif questions is False:
            table = fileio.read_from_file(config.answers)
        else:
            raise ValueError

        # delete record with primary key
        updated_table = [line for line in table if int(line[0]) != int(id)]
        status = True if fileio.write_to_file(
                                              updated_table,
                                              config.questions if questions else config.answers
                                              ) else False

        # delete record(s) with foreign key (cascading delete if deleting questions)
        if questions:
            table_answers = fileio.read_from_file(config.answers)
            updated_answers = [line for line in table_answers if int(line[3]) != int(id)]
            status_answers = True if file_io.write_to_file(updated_answers, config.answers) else False
            status = all(status, status_answers)

    return status


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
