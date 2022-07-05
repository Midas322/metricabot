#! /usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import *

db = SqliteDatabase('data.db', pragmas={'journal_mode': 'wal'})


class MyModel(Model):
    class Meta:
        database = db


class User(MyModel):
    id = PrimaryKeyField(primary_key=True)
    # chat_id пользователя
    chat_id = IntegerField(null=False)
    choosed_element = CharField(null=True)

    request_today = IntegerField(default=0)
    request_month = IntegerField(default=0)
    tariff = CharField(default='tarif_free')
    end_tariff = DateField(null=True)
    date1 = CharField(null=True, max_length=15)
    date2 = CharField(null=True, max_length=15)

    # Позиция в диалоге
    dialog_position = CharField(default='MAIN_MENU')
    # Позиция в меню
    menu_position = CharField(null=True)


class Login(MyModel):
    id = PrimaryKeyField(primary_key=True)
    user = ForeignKeyField(User, related_name='modificator', null=False, on_delete='CASCADE')
    met_id = IntegerField(null=False)
    token = CharField(max_length=30, null=True)
    name = CharField(max_length=30, null=True)
    dir_client = CharField(max_length=30, null=True)
    channel_to_post = CharField(max_length=30, null=True)
    ok_to_post = BooleanField(null=True)


class Tagrget(MyModel):
    id = PrimaryKeyField(primary_key=True)
    target = IntegerField(null=False)
    login = ForeignKeyField(Login, related_name='modificator', null=False, on_delete='CASCADE')


class Tariff(MyModel):
    id = PrimaryKeyField(primary_key=True)

    name = CharField(null=False, max_length=20)
    tariff = CharField(null=False, max_length=20)
    duration = IntegerField(null=False)
    infinite = BooleanField(null=False)
    used = BooleanField(null=False)

class Log(MyModel):
    id = PrimaryKeyField(primary_key=True)
    user = ForeignKeyField(User, related_name='modificator', null=False, on_delete='CASCADE')
    date_time = CharField()
    text = CharField()

# class User_Key_Pair(MyModel):
#     user = ForeignKeyField(User, related_name='modificator', null=False)
#     key = ForeignKeyField(Key, related_name='modificator', null=False)