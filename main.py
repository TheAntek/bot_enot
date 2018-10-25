import telebot
from telebot import types
from bot_enot.constants import my_token

bot = telebot.TeleBot(my_token)
current_state = '0'
current_group = None
students_61 = ['1', '2', '3']
students_62 = ['1', '2', '3']
all_groups = {'ІО-61': students_61, 'ІО-62': students_62}

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
    bot.send_message(message.chat.id, 'Виберіть групу:', reply_markup=menu_group)


@bot.message_handler(commands=['help'])
def handle_start_help(message):
    print('help')
    bot.send_message(message.chat.id, 'Тут краткий гайд по тому, что делает этот бот')


@bot.message_handler(func=lambda message: current_state == '1')
def pick_group(message):
    print('pick group')
    global current_state, current_group

    if message.text in ['ІО-61', 'ІО-62', 'ІО-63', 'ІО-64', 'ІО-65']:
        bot.send_message(message.chat.id, 'Ви вибрали {}\nВиберіть студента (номер в списку групи)'
                         .format(message.text), reply_markup=menu_group_remove)
        current_state = '2'
        current_group = all_groups[message.text]  # example: current_group  = 'ІО-61'
        print(current_state, current_group)

    else:
        bot.send_message(message.chat.id, 'Виберіть групу')


@bot.message_handler(func=lambda message: current_state == '2')
def pick_student(message):
    print('pick student')
    global current_state

    if message.text in current_group:
        print(message.text, 'реально в', current_group)
        bot.send_message(message.chat.id, 'есть такой. теперь введите оценки')
        current_state = '3'

    else:
        print(message.text, 'не в', current_group)
        bot.send_message(message.chat.id, 'нет такого')


@bot.message_handler(func=lambda message: current_state == '3')
def enter_marks(message):
    global current_state
    print('enter marks')
    marks = message.text.split()

    if len(marks) == 6:
        print('right length')
        bot.send_message(message.chat.id, 'Додано в базу даних')
        current_state = '4'
        # добавляем инфу в ексель


if __name__ == '__main__':
    bot.polling(none_stop=True)
