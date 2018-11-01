from telebot import types

menu_group = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
group_61 = types.KeyboardButton('61')
group_62 = types.KeyboardButton('62')
group_63 = types.KeyboardButton('63')
group_64 = types.KeyboardButton('64')
group_65 = types.KeyboardButton('65')
menu_group.add(group_61, group_62, group_63, group_64, group_65)
menu_group_remove = types.ReplyKeyboardRemove()

menu_choose = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
choose_1 = types.KeyboardButton('Да')
choose_2 = types.KeyboardButton('Нет')
menu_choose.add(choose_1, choose_2)
menu_choose_remove = types.ReplyKeyboardRemove()

menu_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
choose_1 = types.KeyboardButton('Добавить студента')
choose_2 = types.KeyboardButton('Посмотреть студента')
menu_1.add(choose_1, choose_2)
menu_1_remove = types.ReplyKeyboardRemove()
