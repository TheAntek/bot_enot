import gspread
from oauth2client.service_account import ServiceAccountCredentials


def add_to_database(group, number, values):
    # принимаем 2 параметра: string group and list of values ['name', 'mark1', 'mark2'...]
    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open('Students').get_worksheet(int(group[-1])-1)

    for i in range(len(values)):
        sheet.update_cell(int(number)+10, i+1, values[i])


def student_exist(group, name):
    # проверить существует ли студент в таблице
    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open('Students').get_worksheet(int(group[-1]) - 1)
    student_names = sheet.col_values(1)

    if name in student_names:
        return True

    return False


def id_exist(group, number):
    # проверить существует ли кто-то в таблице под таким же номером в списке
    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open('Students').get_worksheet(int(group[-1]) - 1)
    val = sheet.cell(int(number)+10, 1).value

    if val != '':
        return True

    return False


def get_marks(group, name):
    # узнаем оценки студента
    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open('Students').get_worksheet(int(group[-1]) - 1)
    cell = sheet.find(name)

    marks_in_list = sheet.row_values(cell.row)
    marks_in_string = ' '.join(marks_in_list[1:-1])
    # функция возвращает все оценки след образом: ('m1 m2 m3 m4 m5 m6', 'AVERAGE')
    return marks_in_string, marks_in_list[-1]


def average_marks(group):
    # узнаем средний балл каждого в группе
    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open('Students').get_worksheet(int(group[-1]) - 1)
    avg_values = sheet.col_values(8)[1:]  # весь столбец без названия столбца

    return sorted(avg_values, reverse=True)
