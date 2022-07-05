#! /usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json
import datetime
from io import StringIO
import requests

BASE_URL = "https://api-metrika.yandex.ru/stat/v1/data?limit=10000&offset=1&ids={}&oauth_token={}"


class metrica(object):
    def __init__(self, id, token, targets, dir_client):
        self.id = id
        self.token = token
        self.targets = targets
        self.dir_client = dir_client
        self.errors = []

    def get(self, settings, dates):
        req_url = BASE_URL.format(self.id, self.token)

        if self.dir_client is not None and self.dir_client != "-":
            req_url += "&direct_client_logins=" + self.dir_client

        for i in settings.keys():
            req_url += "&{}=".format(i)
            for j in settings[i]:
                req_url += str(j) + ","
            req_url = req_url[:-1]

        for i in dates.keys():
            req_url += "&{}=".format(i)
            for j in dates[i]:
                req_url += str(j) + ","
            req_url = req_url[:-1]

        if self.targets:
            for i in self.targets:
                if 'ym:ad' in req_url:
                    req_url = req_url.replace('&metrics=', '&metrics=ym:ad:goal{}users,'.format(i))
                else:
                    req_url = req_url.replace('&metrics=', '&metrics=ym:s:goal{}users,'.format(i))

        print(req_url)
        r = requests.get(req_url, headers={'Authorization': 'OAuth {}'.format(self.token)}).text
        try:
            pre_data = json.loads(r)['data']
        except:
            if self.get_error(json.loads(r)) not in self.errors:
                self.errors.append(self.get_error(json.loads(r)))
            print(r)

        if json.loads(r)['data'] == []:
            self.errors.append(
                "Данные из Яндекс Директа не получены. Возможно логин от Директа не является главным или указан неверно. Подробнее смотрите тут: http://shendrik.site/bot")

        data = []
        mas_dim = list(settings['dimensions'])
        mas_met = []

        if self.targets:
            for i in self.targets:
                if 'ym:ad' in req_url:
                    mas_met.append('ym:ad:goal{}users'.format(i))
                else:
                    mas_met.append('ym:s:goal{}users'.format(i))

        for i in settings['metrics']:
            mas_met.append(i)

        for i in pre_data:
            new_dict = {}

            k = 0
            dimensions = {}

            for dim in i['dimensions']:
                dimensions[mas_dim[k]] = dim['name']
                try:
                    if 'Banner' in mas_dim[k] or 'Order' in mas_dim[k] and 'id' in dim.keys():
                        if dim['id'] != None:
                            dimensions[mas_dim[k]] += " | " + dim['id']
                except:
                    print(dim)
                k += 1

            k = 0
            metrics = {}
            for met in i['metrics']:
                metrics[mas_met[k]] = met
                k += 1
            new_dict['dimensions'] = dimensions
            new_dict['metrics'] = metrics
            data.append(new_dict)

        return data

    def get_bytime(self, settings, dates):

        req_url = BASE_URL.format(self.id, self.token)

        req_url = req_url.replace('data?', 'data/bytime?')

        if self.dir_client is not None and self.dir_client != "-":
            req_url += "&direct_client_logins=" + self.dir_client

        for i in settings.keys():
            req_url += "&{}=".format(i)
            for j in settings[i]:
                req_url += str(j) + ","
            req_url = req_url[:-1]

        for i in dates.keys():
            req_url += "&{}=".format(i)
            for j in dates[i]:
                req_url += str(j) + ","
            req_url = req_url[:-1]

        if self.targets:
            for i in self.targets:
                if 'ym:ad' in req_url:
                    req_url = req_url.replace('&metrics=', '&metrics=ym:ad:goal{}users,'.format(i))
                else:
                    req_url = req_url.replace('&metrics=', '&metrics=ym:s:goal{}users,'.format(i))

        print(req_url)
        r = requests.get(req_url, headers={'Authorization': 'OAuth {}'.format(self.token)}).text


        js = json.loads(r)
        try:
            pre_data = js['data']
            metrics = js['query']['metrics']
            dimensions = js['query']['dimensions']
        except:
            self.errors = "None"

        list_1 = []

        str_start = ''
        for i in dates['date1']:
            str_start=i


        date1 = datetime.datetime.strptime(str_start, '%Y-%m-%d')


        data = []
        for dim in pre_data:

            for i in range(len(dim['metrics'][0])):
                new_dict = {}

                cur_dim = {}
                for z in range(len(dimensions)):
                    cur_dim[dimensions[z]] = dim['dimensions'][z]['name']


                cur_dim['day'] = (date1 + datetime.timedelta(days=i)).strftime("%w")
                new_dict['dimensions'] = cur_dim
                new_dict['metrics'] = {}

                for j in range(len(dim['metrics'])):
                    new_dict['metrics'][metrics[j]] = dim['metrics'][j][i]
                data.append(new_dict)

        return data

    def get_error(self, dict):
        error = 'Неизвестная ошибка.'
        if dict['message'] == 'Entity not found':
            error = 'ID Метрики указан неверно!'
        if dict['message'] == 'Invalid oauth_token':
            error = 'Токен установлен неверно!'

        if dict['message'] == "Access is denied":
            error = 'Отказано в доступе. Токен и Логин Директа разные.'

        if dict['code'] == 400 and 'goal' in dict['message']:
            error = 'Цели установлены неверно!'

        if dict['code'] == 400 and dict['message'] == "Такой пользователь не существует.":
            error = 'Указан несуществующий логин Яндекс Директа!'

        if dict['code'] == 400 and dict['message'] == "Такой пользователь не существует.":
            error = 'Указан несуществующий логин Яндекс Директа!'

        if dict['code'] == 400 and '4005' in dict['message']:
            error = 'Неверно указана дата начала или дата окончания отчетности!'

        if error == 'Неизвестная ошибка.':
            try:
                f = open("erros.txt", "w+")
                f.write(str(dict))
                f.close()
            except:
                print("Such an irony...")
        return error
