import pickle


def new_user(user_id):
    # добавить нового пользователя в словарь
    pickle_file_read = open('users.pickle', 'rb')
    dictionary = pickle.load(pickle_file_read)

    dictionary[user_id] = '0'

    pickle_file_write = open('users.pickle', 'wb')
    pickle.dump(dictionary, pickle_file_write)
    pickle_file_write.close()


def edit_user_state(user_id, new_state):
    # редактировать фазу пользователя
    pickle_file_read = open('users.pickle', 'rb')
    dictionary = pickle.load(pickle_file_read)

    dictionary[user_id] = new_state

    pickle_file_write = open('users.pickle', 'wb')
    pickle.dump(dictionary, pickle_file_write)
    pickle_file_write.close()


def check_user_state(user_id):
    # проверить в какой фазе пользователь и существует ли он
    pickle_file_read = open('users.pickle', 'rb')
    dictionary = pickle.load(pickle_file_read)

    if user_id in dictionary:
        current_state = dictionary[user_id]
        return current_state

    return False