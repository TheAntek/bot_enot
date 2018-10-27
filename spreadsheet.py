def add_to_database(group, number, values):
    # принимаем 2 параметра: string group and list of values ['name', 'mark1', 'mark2'...]
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials

    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open('Students').get_worksheet(int(group[-1])-1)

    sheet.insert_row(values, number+1)


if __name__ == '__main__':
    pass
