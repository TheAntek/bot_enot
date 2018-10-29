import pickle


def new_user(user_id):
    # добавить нового пользователя в словарь
    pickle_file_read = open('users.pickle', 'rb')
    dictionary = pickle.load(pickle_file_read)

    dictionary[user_id] = ['0', None, None, None, None]

    pickle_file_write = open('users.pickle', 'wb')
    pickle.dump(dictionary, pickle_file_write)
    pickle_file_write.close()


def edit_user_state(user_id, new_state):
    # редактировать фазу пользователя
    pickle_file_read = open('users.pickle', 'rb')
    dictionary = pickle.load(pickle_file_read)

    dictionary[user_id][0] = new_state

    pickle_file_write = open('users.pickle', 'wb')
    pickle.dump(dictionary, pickle_file_write)
    pickle_file_write.close()


def edit_user_inf(user_id, inf):
    # редактировать (добавить) значение группы / ФИО/ id/ оценки
    pickle_file_read = open('users.pickle', 'rb')
    dictionary = pickle.load(pickle_file_read)

    for i in range(1, 5):
        if check_user_state(user_id)[-1] == str(i):  # '1'[-1] = 1;  'watch_1'[-1] = 1
            dictionary[user_id][i] = inf

    pickle_file_write = open('users.pickle', 'wb')
    pickle.dump(dictionary, pickle_file_write)
    pickle_file_write.close()


def check_user_state(user_id):
    # проверить в какой фазе пользователь и существует ли он
    pickle_file_read = open('users.pickle', 'rb')
    dictionary = pickle.load(pickle_file_read)

    if user_id in dictionary:
        current_state = dictionary[user_id][0]
        return current_state

    return False


def check_all_info(user_id):
    # вытянуть все данные, которые ввёл пользователь
    pickle_file_read = open('users.pickle', 'rb')
    dictionary = pickle.load(pickle_file_read)

    return dictionary[user_id]
