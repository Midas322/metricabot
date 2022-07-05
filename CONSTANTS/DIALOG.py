#! /usr/bin/env python
# -*- coding: utf-8 -*-

class UCOMANDS:
    BACK = 'Назад'
    ACT = 'ACT'
    SET_YES = 'Включить'
    SET_NO = 'Отключить'


class MASTER:
    MAIN_MENU = 'MAIN_MENU'
    LOGINS_MENU = 'LOGINS_MENU'
    SET_LOGIN = 'SET_LOGIN'
    STAT_LOGIN = 'STAT_LOGIN'
    CHOOSE_VAR = 'CHOOSE_VAR'
    PROFILE = 'PROFILE'
    NEW_USER_SEQUENCE= 'NEW_USER_SEQUENCE'

    Dict = {
        MAIN_MENU: {'name':'Главное Меню', 'command':'/menu'},
        LOGINS_MENU: {'name':'Метрики', 'command':'/metrics > /choose'},
        SET_LOGIN: {'name': 'Настройки', 'command':'/settings'},
        STAT_LOGIN: {'name': 'Статистика', 'command':'/stat'},
        CHOOSE_VAR: {'name': 'Меню выбраной Метрики', 'command':'/metmenu'},
        PROFILE: {'name': 'Ваш Профиль', 'command':'/profile'},
    }

class NEW_USER_SEQUENCE:
    STEP_1 = 'STEP_1'
    STEP_2 = 'STEP_2'
    STEP_3 = 'STEP_3'
    STEP_4 = 'STEP_4'

class PROFILE:
    USE_KEY = "Использовать ключ"
    BUY_KEY = "Купить ключ"
    ABOUT = "О аккаунте"
    List = [USE_KEY,ABOUT]

class MAIN_MENU:
    PROFILE = "Ваш профиль"
    LOGINS = "Метрики"
    ABOUT = "HELP!"
    QUICK_STAT = "Статистика Яндекс Директа"
    List = [PROFILE,LOGINS, ABOUT]

class LOGINS_MENU:
    LOGINS_CHOOSE = "Выбрать Метрику"
    LOGINS_ADD = "Добавить Метрику"
    List = [LOGINS_CHOOSE, LOGINS_ADD]
# ad_met(user, chat_id)
class SET_LOGIN:
    SET_TOKEN = "Настроить Token"
    SET_NAME = "Настроить Имя"
    SET_TARGETS = "Настроить Цели"
    SET_DIR_LOGIN = "Настроить Логин Директа"
    SET_DEL_LOGIN = "Удалить Метрику"
    SET_CHANNEL_TO_POST = "Чат Постинга"
    SET_OK_TO_POST = "Факт постинга"
    List = [SET_TOKEN, SET_NAME, SET_TARGETS, SET_DIR_LOGIN, SET_DEL_LOGIN]
    # List = [SET_TOKEN, SET_NAME, SET_TARGETS, SET_DIR_LOGIN, SET_DEL_LOGIN]

class STAT_LOGIN:
    GET_STAT = "Анализ статистики"
    GET_PLATFORMS = "Анализ Площадок"
    GET_QUICK_STAT = "Статистика Я.Д"
    GET_STAT_BY_DAY = "Статистика по дням"
    SET_DATE_1 = "Дата начала"
    SET_DATE_2 = "Дата конца"
    SET_DATES_MENU = "Установить даты"
    List = [GET_STAT,SET_DATE_1,SET_DATE_2]

class CHOOSE_VAR:
    CHOOSE_SET = "Настройки Метрики"
    CHOOSE_STAT = "Статитика"
    CHOOSE_INFO = "О Метрике"
    List = [CHOOSE_SET, CHOOSE_STAT, CHOOSE_INFO]

class DATES_KEYBOARD:
    TODAY = 'Сегодня'
    YESTAERDAY = 'Вчера'
    THIS_WEEK = 'Эта неделя'
    LAST_WEEK = 'Прошлая неделя'
    THIS_MONTH = 'Этот месяц'
    LAST_7_DAYS = 'Прошлые 7 дней'
    LAST_30_DAYS = 'Прошлые 30 дней'
    SET_DATE_1 = "Дата начала"
    SET_DATE_2 = "Дата конца"

    TAG = "DATES_KEYBOARD"
    List = [TODAY, YESTAERDAY, THIS_WEEK, LAST_WEEK, THIS_MONTH, LAST_7_DAYS,SET_DATE_1, SET_DATE_2, LAST_30_DAYS]
    Len = 2


class HELP_KEYBOARD:
    ABOUT = "Что делает бот?"
    HOW_TO_SET = "Как настроить бота?"
    HOW_TO_AD_MET = "Как подключить Метрику?"
    HOW_TO_SET_DATES = "Как устанавливать даты?"
    ABOUT_STATISTICS = "О статитстике"
    COMMANDS = "Команды бота"

    TAG = "DATES_KEYBOARD"
    List = [ABOUT,HOW_TO_AD_MET, HOW_TO_SET_DATES,ABOUT_STATISTICS, COMMANDS]
    Len = 2

class LOCKED:
    List = [STAT_LOGIN.SET_DATE_1, STAT_LOGIN.SET_DATE_2]

