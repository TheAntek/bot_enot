import telebot
from telebot import types
from bot_enot.constants import my_token
from bot_enot.spreadsheet import add_to_database

bot = telebot.TeleBot(my_token)
current_state = '0'
current_group = None
current_student = None

# создаем кнопки. хз нужно ли. можно будет убрать
menu_group = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
group_61 = types.KeyboardButton('ІО-61')
group_62 = types.KeyboardButton('ІО-62')
group_63 = types.KeyboardButton('ІО-63')
group_64 = types.KeyboardButton('ІО-64')
group_65 = types.KeyboardButton('ІО-65')
menu_group.add(group_61, group_62, group_63, group_64, group_65)
menu_group_remove = types.ReplyKeyboardRemove()


@bot.message_handler(commands=['start', 'reset'])
def handle_start_help(message):
    global current_state
    current_state = '1'
    bot.send_message(message.chat.id, 'Виберіть групу', reply_markup=menu_group)


@bot.message_handler(commands=['help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, 'Тут краткий гайд по тому, что делает этот бот')


@bot.message_handler(func=lambda message: current_state == '1')
def pick_group(message):
    global current_state, current_group

    if message.text in ['ІО-61', 'ІО-62', 'ІО-63', 'ІО-64', 'ІО-65']:
        bot.send_message(message.chat.id, 'Введіть прізвище студента'.format(message.text),
                         reply_markup=menu_group_remove)
        current_state = '2'
        current_group = message.text

    else:
        bot.send_message(message.chat.id, 'Виберіть групу')


@bot.message_handler(func=lambda message: current_state == '2')
def pick_student(message):
    global current_state, current_student
    current_state = '3'
    current_student = message.text

    bot.send_message(message.chat.id, 'Введіть оцінки')


@bot.message_handler(func=lambda message: current_state == '3')
def enter_marks(message):
    global current_state
    marks = message.text.split()

    if check_len(marks) and check_int(marks) and check_between(marks):
        # делаем проверки правильности оценок и добавляем инфу в бд, если все ок
        current_state = '4'

        marks.insert(0, current_student)
        adding(current_group, marks)
        add_to_database(current_group, marks)

        bot.send_message(message.chat.id, 'Додано в базу даних')
    else:
        bot.send_message(message.chat.id, 'Некоректні оцінки')


def adding(group, values):
    print(group)
    print(values)


def check_len(marks):
    # проверка на правильное количество оценок
    if len(marks) == 6:
        return True
    else:
        return False


def check_int(marks):
    # проверка на целые числа
    for i in marks:
        try:
            int(i)
        except ValueError:
            return False
    return True


def check_between(marks):
    # проверка на верность данных оценки ( >60 & <100 )
    for i in marks:
        if int(i) > 100 or int(i) < 60:
            return False

    return True


if __name__ == '__main__':
    bot.polling(none_stop=True)
