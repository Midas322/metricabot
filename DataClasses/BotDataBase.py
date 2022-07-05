#! /usr/bin/env python
# -*- coding: utf-8 -*-

from DataClasses.BotDataBaseClasses import *

from datetime import datetime, timezone, timedelta


class BotDataBase(object):
    def __init__(self):
        User.create_table()
        Login.create_table()
        Tagrget.create_table()
        Log.create_table()
        Tariff.create_table()

    def add_User(self, chat_id):
        new_user = User.create(chat_id=chat_id)
        return new_user

    def get_User(self, chat_id):
        query = User.select().where(User.chat_id == chat_id)
        if query.exists():
            return query[0]
        return None

    def get_all_Users(self):
        query = User.select()
        if query.exists():
            return query
        return None

    def get_Login(self, user, met_id):
        query = Login.select().where(Login.user == user and Login.met_id == met_id)
        if query.exists():
            return query[0]
        return None

    def set_Login(self, user, met_id):
        new_Login = Login.create(user=user, met_id=met_id)
        return new_Login

    def get_all_Logins(self, user):
        query = Login.select().where(Login.user == user)
        if query.exists():
            return query
        return None

    def set_Target(self, target, login):
        new_target = Tagrget.create(target=target, login=login)
        return new_target

    def get_all_Targets(self, login):
        query = Tagrget.select().where(Tagrget.login == login)
        if query.exists():
            return query
        return None

    def create_keys_table(self, name, tariff, duration=30, infinite=False):
        new_key = Tariff(name=name, tariff=tariff, duration=duration, infinite=infinite, used=False)
        db.create_tables([new_key], safe=True)
        return new_key

    def add_key(self, name, tariff, duration=30, infinite=False):
        new_key = Tariff.create(name=name, tariff=tariff, duration=duration, infinite=infinite, used=False)
        return new_key

    def get_key(self, name):
        query = Tariff.select().where(Tariff.name == name)
        if query.exists():
            return query[0]
        return None

    def get_full_name(self, login: Login):
        name = ""

        if login.name is not None:
            name += f"{login.name} : "
        name += str(login.met_id)
        return name

    def assing_key(self, key, user):
        if not key.infinite:
            key.user = user
            key.used = True

        user.end_tariff = datetime.today() + timedelta(days=key.duration)
        user.tariff = key.tariff
        user.save()
        key.save()

    def ad_log(self, user: User, text: str):
        today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        new_log = Log.create(user=user, text=text, date_time=today)
        return new_log

    def get_logs(self):
        logs = [['chat_di', 'text', 'date_time']]
        for user in User.select():
            for log in Log.select().where(Log.user == user):
                logs.append([user.chat_id, log.text, log.date_time])

        return logs
