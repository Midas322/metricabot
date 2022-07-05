from oauth2client.service_account import ServiceAccountCredentials
import gspread

CREDENTIALS_FILE = 'phonebot-114ebe93cc30.json'
from datetime import datetime

# account@phonebot-1540291979984.iam.gserviceaccount.com
sheets_list = [['Ваше право', 'site1'], ['Полезный Юрист', 'site2'], ['Банкирро', 'site3']]


class gsheet(object):

    def __init__(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                       ['https://www.googleapis.com/auth/drive'])
        self.client = gspread.authorize(credentials)

    def get_data(self, name):
        data = []
        sheet = self.client.open(name).sheet1
        rows = sheet.get()
        amount_pos = 0
        date_pos = 0
        i = 0
        for cell in rows[0]:
            if cell == "Сумма_вашего_долга":
                amount_pos = i
            if cell == "sended":
                date_pos = i
            i += 1

        for row in rows:
            data.append([row[amount_pos], row[date_pos]])

        data = data[1:]
        return data

    def calc(self, name, sdate1, sdate2):
        data = self.get_data(name)
        date1 = datetime.strptime(sdate1, '%Y-%m-%d')
        date2 = datetime.strptime(sdate2, '%Y-%m-%d')
        all = 0
        less_than_100 = 0
        more_than_500 = 0
        for row in data:
            date_res = datetime.strptime(row[1].split(" ")[0], '%Y-%m-%d')
            if date1 <= date_res and date_res >= date2:
                all += 1
                if row[0] == "до 100 тыс. руб.":
                    less_than_100 += 1

                if row[0] == "500-800 тыс руб" or row[0] == "более 800 тыс руб" or row[0] == "300-500 тыс. руб":
                    more_than_500 += 1

                # if row[0] == "500-800 тыс руб" or row[0] == "более 800 тыс руб":
                #     print(row[0])
                #     more_than_500 += 1

        return [all, all - less_than_100, more_than_500]

    def get_msgs(self, sdate1, sdate2):
        msgs = []
        for i in sheets_list:
            vals = self.calc(i[1], sdate1, sdate2)
            msgs.append(f'{i[0]}\nБольше 100 : {vals[1]}\nБольше 300 : {vals[2]}\nВсего : {vals[0]}')

        return msgs


if __name__ == '__main__':
    a = gsheet()

    date1 = '2021-01-07'
    date2 = '2021-01-20'
    msgs = a.get_msgs(date1, date2)
    for msg in msgs:
        print(msg)
