# Work with google spreadsheets:
# https://github.com/burnash/gspread
# https://gspread.readthedocs.io/en/latest/

import telebot
from telebot import types
from bot_enot.constants import my_token
from bot_enot.spreadsheet import add_to_database
from bot_enot.checks import *

bot = telebot.TeleBot(my_token)
current_state = '0'
current_group = None
current_student = None
current_id = None
marks = None

# создаем кнопки. хз нужно ли. можно будет убрать
menu_group = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
group_61 = types.KeyboardButton('61')
group_62 = types.KeyboardButton('62')
group_63 = types.KeyboardButton('63')
group_64 = types.KeyboardButton('64')
group_65 = types.KeyboardButton('65')
menu_group.add(group_61, group_62, group_63, group_64, group_65)
menu_group_remove = types.ReplyKeyboardRemove()

# больше кнопочек
menu_choose = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
choose_1 = types.KeyboardButton('Да')
choose_2 = types.KeyboardButton('Нет')
menu_choose.add(choose_1, choose_2)
menu_choose_remove = types.ReplyKeyboardRemove()


@bot.message_handler(commands=['start', 'reset'])
def handle_start_help(message):
    global current_state
    current_state = '1'
    bot.send_message(message.chat.id, 'Добавляете студента в БД?', reply_markup=menu_choose)


@bot.message_handler(commands=['help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, 'Чтобы добавить студента в БД:\n'
                                      '1) Выберите группу\n'
                                      '2) Введите фамилию и инициалы\n'
                                      '3) Введите номер в списке\n'
                                      '4) Введите оценки\n'
                                      '5) Подтвердите добавление')


@bot.message_handler(func=lambda message: current_state == '1')
def handle_start_help(message):
    global current_state

    if message.text == 'Да':
        current_state = '2'
        bot.send_message(message.chat.id, 'Выберите группу', reply_markup=menu_group)
    elif message.text == 'Нет':
        current_state = 'w'
        bot.send_message(message.chat.id, 'Другие функции появятся вскоре', reply_markup=menu_choose_remove)


@bot.message_handler(func=lambda message: current_state == '2')
def pick_group(message):
    global current_state, current_group

    if message.text in ['61', '62', '63', '64', '65']:
        bot.send_message(message.chat.id, 'Введите фамилию и инициалы студента\n(Верба О. А.)'.
                         format(message.text), reply_markup=menu_group_remove)
        current_state = '3'
        current_group = message.text

    else:
        bot.send_message(message.chat.id, 'Выберите коректную группу')


@bot.message_handler(func=lambda message: current_state == '3')
def pick_student(message):
    global current_state, current_student

    if name_check(message.text):
        current_state = '4'
        current_student = message.text
        bot.send_message(message.chat.id, 'Введите номер студента в списке группы'.format(message.text))
    else:
        bot.send_message(message.chat.id, 'Введите коректные данные')


@bot.message_handler(func=lambda message: current_state == '4')
def pick_id(message):
    global current_state, current_id

    if id_check(message.text):
        # проверка коректности номера в списке
        current_id = int(message.text)
        current_state = '5'
        bot.send_message(message.chat.id, 'Введите оценки')
    else:
        bot.send_message(message.chat.id, 'Введите коректный номер студента в списку группы')


@bot.message_handler(func=lambda message: current_state == '5')
def enter_marks(message):
    global current_state, marks
    marks = message.text.split()

    if check_len(marks) and check_int(marks) and check_between(marks):
        # делаем проверки правильности оценок и добавляем инфу в бд, если все ок
        current_state = '6'
        bot.send_message(message.chat.id, 'Следующие данные будут добавлены:\n\nГруппа: ІО-{}\nСтудент: {}\nНомер: {}\n'
                                          'Оценки: {}'.format(current_group, current_student, current_id, message.text),
                         reply_markup=menu_choose)
    else:
        bot.send_message(message.chat.id, 'Введите коректные оценки')


@bot.message_handler(func=lambda message: current_state == '6')
def final(message):
    global current_state, marks

    if message.text == 'Да':
        marks.insert(0, current_student)
        add_to_database(current_group, current_id, marks)
        bot.send_message(message.chat.id, 'Добавлено в базу данных', reply_markup=menu_choose_remove)
        current_state = 'added'
    elif message.text == 'Нет':
        current_state = '0'
    else:
        bot.send_message(message.chat.id, 'Введите коректные данные')


if __name__ == '__main__':
    bot.polling(none_stop=True)
