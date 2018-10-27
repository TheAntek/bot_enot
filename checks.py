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


def id_check(number):
    # проверка на коректность номера в списке
    try:
        int(number)
        if int(number) > 30 or int(number) < 1:
            return False
    except ValueError:
        return False
    return True


def name_check(text):
    # проверка коректности фамилии. должно быть ---> Фамилия И. О.
    from re import match

    if not match('\w+ \w\. \w\.', text):
        return False

    if not match('\D+ \D\. \D\.', text):
        return False

    return True
