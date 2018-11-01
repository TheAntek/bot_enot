# Work with google spreadsheets:
# https://github.com/burnash/gspread
# https://gspread.readthedocs.io/en/latest/

import telebot
from bot_enot.constants import my_token
from bot_enot.spreadsheet import *
from bot_enot.checks import *
from bot_enot.pickle_users_id import *
from bot_enot.markups import *
from statistics import mean

bot = telebot.TeleBot(my_token)


@bot.message_handler(commands=['start', 'reset'])
def handle_start(message):

    new_user(message.from_user.id)

    bot.send_message(message.chat.id, 'Что хотите сделать?', reply_markup=menu_1)


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, '*Краткое руководство*\n\n> Добавьте студента\n> Посмотрите статистику\n> '
                                      'Плачьте\n\nВсе данные хранятся в [Google Таблице](https://docs.google.com/'
                                      'spreadsheets/d/1d9u1CD0zkkRPkDP0AyJHAeGYcKfYN9BSp8GyoyHbj7g/edit#gid=0)',
                     parse_mode='Markdown')


@bot.message_handler(func=lambda message: check_user_state(message.from_user.id) == '0')
def handle_start_choose(message):

    if message.text == 'Добавить студента':
        edit_user_state(message.from_user.id, '1')
        bot.send_message(message.chat.id, 'Выберите группу', reply_markup=menu_group)

    elif message.text == 'Посмотреть студента':
        edit_user_state(message.from_user.id, 'watch_1')
        bot.send_message(message.chat.id, 'Выберите группу', reply_markup=menu_group)


@bot.message_handler(func=lambda message: check_user_state(message.from_user.id) == '1' or
                                          check_user_state(message.from_user.id) == 'watch_1')
def pick_group(message):
    if message.text in ['61', '62', '63', '64', '65']:
        bot.send_message(message.chat.id, 'Введите фамилию и инициалы студента\n_(Верба О. А.)_'.
                         format(message.text), reply_markup=menu_group_remove, parse_mode='Markdown')

        edit_user_inf(message.from_user.id, message.text)  # записываем номер группы

        if check_user_state(message.from_user.id) == '1':
            edit_user_state(message.from_user.id, '2')

        elif check_user_state(message.from_user.id) == 'watch_1':
            edit_user_state(message.from_user.id, 'watch_2')

    else:
        bot.send_message(message.chat.id, 'Выберите коректную группу')


@bot.message_handler(func=lambda message: check_user_state(message.from_user.id) == 'watch_2')
def pick_student(message):

    if student_exist(check_all_info(message.from_user.id)[1], message.text):
        edit_user_inf(message.from_user.id, message.text)
        all_student_marks = get_marks(check_all_info(message.from_user.id)[1], message.text)  # все оценки студента
        avg_group_marks = average_marks(check_all_info(message.from_user.id)[1])

        bot.send_message(message.chat.id, f'*Студент:* {message.text}\n*Оценки:* {all_student_marks[0]}\n*Средний балл:'
                                          f'* {all_student_marks[1]}\n*Позиция в группе:* '
                                          f'{avg_group_marks.index(all_student_marks[1])+1} из {len(avg_group_marks)}'
                                          f'\n\n/start - начать сначала', parse_mode='Markdown')
        edit_user_state(message.from_user.id, None)
    else:
        bot.send_message(message.chat.id, 'Такого студента нет в таблице')


@bot.message_handler(func=lambda message: check_user_state(message.from_user.id) == '2')
def pick_student(message):

    if student_exist(check_all_info(message.from_user.id)[1], message.text):
        bot.send_message(message.chat.id, 'Студент уже в базе данных')

    elif name_check(message.text):
        edit_user_inf(message.from_user.id, message.text)  # записываем Фамилия И. О.
        edit_user_state(message.from_user.id, '3')
        bot.send_message(message.chat.id, 'Введите номер студента в списке группы')

    else:
        bot.send_message(message.chat.id, 'Введите коректные данные')


@bot.message_handler(func=lambda message: check_user_state(message.from_user.id) == '3')
def pick_id(message):

    if id_check(message.text):  # проверка коректности номера в списке
        if id_exist(check_all_info(message.from_user.id)[1], message.text):
            bot.send_message(message.chat.id, 'Студент с таким номером уже существует')
        else:
            edit_user_inf(message.from_user.id, message.text)  # записываем номер студента
            edit_user_state(message.from_user.id, '4')
            bot.send_message(message.chat.id, 'Введите оценки')
    else:
        bot.send_message(message.chat.id, 'Введите коректный номер студента в списку группы')


@bot.message_handler(func=lambda message: check_user_state(message.from_user.id) == '4')
def enter_marks(message):
    marks = message.text.split()

    if check_len(marks) and check_int(marks) and check_between(marks):
        # делаем проверки правильности оценок и добавляем инфу в бд, если все ок
        edit_user_inf(message.from_user.id, marks)
        edit_user_state(message.from_user.id, '5')
        result = check_all_info(message.from_user.id)
        bot.send_message(message.chat.id, 'Следующие данные будут добавлены:\n\nГруппа: ІО-{}\nСтудент: {}\nНомер: {}\n'
                                          'Оценки: {}'.format(result[1], result[2], result[3], ' '.join(result[4])),
                         reply_markup=menu_choose)
    else:
        bot.send_message(message.chat.id, 'Введите коректные оценки')


@bot.message_handler(func=lambda message: check_user_state(message.from_user.id) == '5')
def final(message):

    if message.text == 'Да':
        result = check_all_info(message.from_user.id)  # result = [ 'state', 'ФИО', 'id', [n marks] ]
        student_name_and_marks = list(map(lambda x: int(x), result[4]))  # преобразовываем str в int в списке
        student_name_and_marks.append(round(mean(student_name_and_marks), 2))  # добавялем в конец списка AVG mark
        student_name_and_marks.insert(0, result[2])  # добавляем в начало списка ФИО

        # добавляем:  № группы | № студента | [Фамилия И. О., 60, 75 ... AVG]
        add_to_database(result[1], result[3], student_name_and_marks)
        bot.send_message(message.chat.id, 'Добавлено в базу данных\n\n/start - начать сначала',
                         reply_markup=menu_choose_remove)
        edit_user_state(message.from_user.id, 'added')
    elif message.text == 'Нет':
        edit_user_state(message.from_user.id, None)
        bot.send_message(message.chat.id, '/start - начать сначала', reply_markup=menu_choose_remove)
    else:
        bot.send_message(message.chat.id, 'Введите коректные данные')


if __name__ == '__main__':
    bot.polling(none_stop=True)
