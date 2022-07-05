#! /usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import time
from pathlib import Path
from datetime import datetime, timedelta
import os
import threading

from telebot import types

from CONSTANTS.DIALOG import *
from CONSTANTS.TARIFICATION import *
from Keyboards import Keyboards
from DataClasses.BotDataBase import BotDataBase
from DataClasses.BotDataBaseClasses import *
import telebot
from metuser import metuser
from once_a_day import once_a_day
from gsheet import gsheet
# TOKEN = "1263781356:AAH3SJ88CsqwTcys9J77Xop1NlyeyF9gesw"  # Основной Бот
# TOKEN = "1296656249:AAHo1t5ebTRwaVGCgwPjBiqlcZ6ouVto2iA"  # Тестовый Бот
TOKEN = "1310243112:AAF6m0gjflNKyxfqAuVKeFkMvz0QmUNvtm0"  # Проще Бот


bot = telebot.TeleBot(TOKEN)
once = once_a_day()

my_file = Path("data.db")
to_create = not my_file.is_file()
bdb = BotDataBase()

if to_create:
    print("was created")
    bdb.create_keys_table("key", "key")
    bdb.add_key("key", "def")

keyboards = Keyboards()


def dates_keyboadr_handler(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    code = callback_query.data.split("###")[0]
    print(code)
    user: User = bdb.get_User(chat_id)
    bdb.ad_log(user, callback_query.data)

    if code == DATES_KEYBOARD.SET_DATE_1:
        if is_locked(user.dialog_position):
            bot.send_message(chat_id=chat_id, text='Операция пока невозможна. Чтовы выти на главное меню нажмите /menu')
            return
        bot.send_message(chat_id=chat_id, text='Введите дату начала в формате 2020-06-07 (Год-Месяц-День).',
                         reply_markup=keyboards.just_BACK())
        user.dialog_position = append_dp(user.dialog_position, STAT_LOGIN.SET_DATE_1)
        user.save()
        return

    if code == DATES_KEYBOARD.SET_DATE_2:
        if is_locked(user.dialog_position):
            bot.send_message(chat_id=chat_id, text='Операция пока невозможна. Чтовы выти на главное меню нажмите /menu')
            return
        bot.send_message(chat_id=chat_id, text='Введите дату конца в формате 2020-06-07 (Год-Месяц-День).',
                         reply_markup=keyboards.just_BACK())
        user.dialog_position = append_dp(user.dialog_position, STAT_LOGIN.SET_DATE_2)
        user.save()
        return

    if code == DATES_KEYBOARD.TODAY:
        day = datetime.today().strftime("%Y-%m-%d")
        user.date1 = day
        user.date2 = day
        user.save()
        bot.send_message(chat_id=chat_id, text=f'Дата отчета установлены на {user.date1}.')
        return

    if code == DATES_KEYBOARD.YESTAERDAY:
        day = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        user.date1 = day
        user.date2 = day
        user.save()
        bot.send_message(chat_id=chat_id, text=f'Дата отчета установлены на {user.date1}.')
        return

    if code == DATES_KEYBOARD.THIS_WEEK:
        today = datetime.today()
        wd_back = 0
        if today.weekday() == 0:
            wd_back = 6
        else:
            wd_back = today.weekday() - 1
        user.date1 = (today - timedelta(days=wd_back + 1)).strftime("%Y-%m-%d")
        user.date2 = today.strftime("%Y-%m-%d")
        user.save()
        bot.send_message(chat_id=chat_id,
                         text=f'Дата отчета установлены на:\nДата начала : {user.date1}\nДата конца : {user.date2}')
        return

    if code == DATES_KEYBOARD.LAST_WEEK:
        today = datetime.today()
        wd_back = 0
        wd_back = today.weekday() - 1

        user.date1 = (today - timedelta(days=wd_back + 8)).strftime("%Y-%m-%d")
        user.date2 = (today - timedelta(days=wd_back + 2)).strftime("%Y-%m-%d")
        user.save()
        bot.send_message(chat_id=chat_id,
                         text=f'Дата отчета установлены на:\nДата начала : {user.date1}\nДата конца : {user.date2}')

    if code == DATES_KEYBOARD.LAST_7_DAYS:
        user.date1 = (datetime.today() - timedelta(days=8)).strftime("%Y-%m-%d")
        user.date2 = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        user.save()
        bot.send_message(chat_id=chat_id,
                         text=f'Дата отчета установлены на:\nДата начала : {user.date1}\nДата конца : {user.date2}')
        return

    if code == DATES_KEYBOARD.LAST_30_DAYS:
        user.date1 = (datetime.today() - timedelta(days=31)).strftime("%Y-%m-%d")
        user.date2 = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        user.save()
        bot.send_message(chat_id=chat_id,
                         text=f'Дата отчета установлены на:\nДата начала : {user.date1}\nДата конца : {user.date2}')
        return

    if code == DATES_KEYBOARD.THIS_MONTH:
        user.date1 = (datetime.today() - timedelta(days=datetime.today().day - 1)).strftime("%Y-%m-%d")
        user.date2 = datetime.today().strftime("%Y-%m-%d")
        user.save()
        bot.send_message(chat_id=chat_id,
                         text=f'Дата отчета установлены на:\nДата начала : {user.date1}\nДата конца : {user.date2}')
        return


def HOW_TO_AD_MET(chat_id):
    bot.send_message(chat_id=chat_id,
                     text='Чтобы подключить метрику, нужно нажать в главном меню кнопку Метрики или /metmenu.')
    time.sleep(2)
    bot.send_message(chat_id=chat_id, text='Далее нажмите Добавить Метрику')
    time.sleep(2)
    bot.send_message(chat_id=chat_id,
                     text='После чего вам нудно будет ввести ID Метрики. А затем добавить Токен к данной метрике.')
    time.sleep(2)
    bot.send_message(chat_id=chat_id,
                     text='Полную инструкцию по добавлению Метрики вы можете посмотреть тут: http://proshebot.ru/instructions')
    time.sleep(2)
    bot.send_message(chat_id=chat_id, text='Так же она показана вот в этом видео:')
    bot.send_message(chat_id=chat_id, text='https://www.youtube.com/watch?v=PxBRXF221ns')
    time.sleep(2)
    bot.send_message(chat_id=chat_id,
                     text='Так же есть команда /admet (можете нажать) которая позволяет быстро перейти к Добавлению метрики.')


def HOW_TO_SET_DATES(chat_id):
    bot.send_message(chat_id=chat_id,
                     text=f'Меню Дат можно вызвать нажав кнопку *{STAT_LOGIN.SET_DATES_MENU}* в меню *{MASTER.Dict[MASTER.STAT_LOGIN]["name"]}* или введя команду /dates.',
                     parse_mode="Markdown")
    time.sleep(1)
    bot.send_message(chat_id=chat_id,
                     text=f'Все кнопки, кроме *{DATES_KEYBOARD.SET_DATE_1}* и *{DATES_KEYBOARD.SET_DATE_2}*, устанавливают даты по одному нажатию.',
                     parse_mode="Markdown")
    time.sleep(2)
    bot.send_message(chat_id=chat_id,
                     text=f'При нажатии на *{DATES_KEYBOARD.SET_DATE_1}* и *{DATES_KEYBOARD.SET_DATE_2}* вам нужно будет установить даты вручную. Вписав дату в формате 2020-06-01 (Год-Месяц-Ден).',
                     parse_mode="Markdown")
    time.sleep(1)
    bot.send_message(chat_id=chat_id,
                     text=f'Разадение между Годом, Месяцем и Днём должно обязательно быть через знак "-".',
                     parse_mode="Markdown")


def help_keyboadr_handler(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    code = callback_query.data.split("###")[0]
    user: User = bdb.get_User(chat_id)
    bdb.ad_log(user, callback_query.data)

    if code == HELP_KEYBOARD.ABOUT:
        bot.send_message(chat_id=chat_id, text='Я упрощаю оптимизацию рекламы через анализ трафика.')
        time.sleep(1)
        bot.send_message(chat_id=chat_id, text='Так же позволяю следить за подлюченными рекламными аккаунтами.')
        time.sleep(1)
        bot.send_message(chat_id=chat_id,
                         text='Чтобы управялть мной, нужно нажимать кнопки на клавиатуре. Словестные команды я не поддерживаю.')
        time.sleep(2)
        bot.send_message(chat_id=chat_id, text='Перед тем как получать статитику с метрики, необходимо её подключить.')
        time.sleep(1)
        bot.send_message(chat_id=chat_id, text='Нажмите /howtoad чтобы я рассказал как подключить метрику.')
        return

    if code == HELP_KEYBOARD.HOW_TO_SET:
        bot.send_message(chat_id=chat_id, text='Операция пока невозможна. Чтовы выти на главное меню нажмите /menu')
        return

    if code == HELP_KEYBOARD.HOW_TO_AD_MET:
        HOW_TO_AD_MET(chat_id)
        return

    if code == HELP_KEYBOARD.HOW_TO_SET_DATES:
        HOW_TO_SET_DATES(chat_id)
        return

    if code == HELP_KEYBOARD.COMMANDS:
        bot.send_message(chat_id=chat_id, text='Список всех команд:')
        bot.send_message(chat_id=chat_id,
                         text='/help - Удобная инструкция к боту\n/menu - В главное меню\n/back - Назад\n/dates - Настроит даты отчета\n/admet - Добавляет счетчик Метрики\n/choose - Выбрать метрику')
        return

    if code == HELP_KEYBOARD.ABOUT_STATISTICS:
        bot.send_message(chat_id=chat_id,
                         text=f'Чтобы анализировать статистику рекламны, вам нужно выбрать метрику. Для этого нужно в главном меню (/menu) нажать *{MAIN_MENU.LOGINS}*',
                         parse_mode='Markdown')
        time.sleep(1)
        bot.send_message(chat_id=chat_id,
                         text=f'Затем *{LOGINS_MENU.LOGINS_CHOOSE}*, или *{LOGINS_MENU.LOGINS_ADD}* если у вас нет добавленных Метрик.',
                         parse_mode='Markdown')
        time.sleep(1)
        bot.send_message(chat_id=chat_id,
                         text=f'После чего выберите необходимую метрику. Потом нажмите *{CHOOSE_VAR.CHOOSE_STAT}* ',
                         parse_mode='Markdown')
        time.sleep(1)
        bot.send_message(chat_id=chat_id, text=f'Установите даты. Об этом я тоже рассказываю в /help.',
                         parse_mode='Markdown')
        time.sleep(1)
        bot.send_message(chat_id=chat_id,
                         text=f'После чего вы можете запросить любой анализ статистики. Подробнее о каждом виде анализа вы можете посмотреть тут /helpstat',
                         parse_mode='Markdown')
        time.sleep(1)
        bot.send_message(chat_id=chat_id,
                         text=f'Кнопка *{MAIN_MENU.QUICK_STAT}* в главном меню отправляет статитику Яндекс Директа по всем аккаунтам за указанный период.',
                         parse_mode='Markdown')
        time.sleep(2)
        bot.send_message(chat_id=chat_id,
                         text='Анализ статитики отправляется в виде Эксель файла, полноное описание его можно посмотрет тут:')
        bot.send_message(chat_id=chat_id, text='https://www.youtube.com/watch?v=T3rVMut_0fg&feature=emb_logo')
        return


@bot.callback_query_handler(func=lambda call: True)
def query_handler(callback_query: types.CallbackQuery):
    tag = ''
    if '###' in callback_query.data:
        tag = callback_query.data.split("###")[1]

    if tag == DATES_KEYBOARD.TAG:
        threading.Thread(target=dates_keyboadr_handler, args=(callback_query,)).start()

    if tag == HELP_KEYBOARD.TAG:
        threading.Thread(target=help_keyboadr_handler, args=(callback_query,)).start()


# Хендлер
@bot.message_handler(content_types=["text"])
def handle_text(message):
    threading.Thread(target=handler, args=(message,)).start()


# Обычный режим
def handler(message):
    # Получаем пользователя
    chat_id = message.from_user.id
    text = message.text
    user: User = bdb.get_User(chat_id)

    # Создание пользователя и отправка его в начальный диалог
    if user is None:
        user = bdb.add_User(chat_id)
        user.dialog_position = dp([MASTER.MAIN_MENU])
        user.save()
        bot.send_message(chat_id=chat_id, text="Привет!", reply_markup=keyboards.MAIN_MENU())
        time.sleep(1)
        bot.send_message(chat_id=chat_id, text="Я Проще!Бот, помогающий в работе с Яндекс Директом и Яндекс Метрикой.")
        time.sleep(2)
        bot.send_message(chat_id=chat_id,
                         text="Я автоматизирую анализ трафика и позволяю следить за большим количеством аккаунтов Яндекс Директа.")
        time.sleep(1)
        bot.send_message(chat_id=chat_id, text="Если у тебя возникнут вопросы, то пиши /help и я на них отвечу",
                         reply_markup=keyboards.HELP_KEYBOARD())
        return

    bdb.ad_log(user, text)

    if text == '/back' or text == UCOMANDS.BACK:
        Back(user, chat_id)
        return

    if text == "/key" and user.tariff == TARIFICATION.tarif_free:
        bot.send_message(chat_id=chat_id, text="Введите ключ:", reply_markup=keyboards.just_BACK())
        user.dialog_position = dp([MASTER.MAIN_MENU, PROFILE.USE_KEY])
        user.save()
        return

    # Ввод ключа
    if PROFILE.USE_KEY in user.dialog_position:
        key = bdb.get_key(text)
        print(key)

        if key != None:
            if key.used:
                if user.tariff != TARIFICATION.tarif_free:
                    Back(user, chat_id, "Вы ввели уже использованный ключ!")
                else:
                    bot.send_message(chat_id=chat_id,
                                     text="Вы ввели уже использованный ключ!")
            else:
                bdb.assing_key(key, user)
                TV = TARIFICATION.tarif_values[user.tariff]
                msg = 'Тариф {} подключен до {}.'.format(TV['name'], user.end_tariff.strftime("%Y-%m-%d"))
                Back(user, chat_id, msg)
        else:
            if user.tariff != TARIFICATION.tarif_free:
                Back(user, chat_id, "Вы ввели неправильный ключ!")
            else:
                bot.send_message(chat_id=chat_id,
                                 text="Вы ввели неправильный ключ!")
        return

    # if user.tariff == TARIFICATION.tarif_free:
    #     bot.send_message(chat_id=chat_id,
    #                      text="Привет! Бот пока находится в разработке!")
    #     return



    if text == '/menu':
        user.dialog_position = dp([MASTER.MAIN_MENU])
        user.save()
        bot.send_message(chat_id=chat_id, text=bread_crumbs(user.dialog_position), reply_markup=keyboards.MAIN_MENU())
        return

    if text == '/admet':
        ad_met(user, chat_id)
        return


    if text == '/howtoad':
        HOW_TO_AD_MET(chat_id)
        return

    if text == '/helpdates':
        HOW_TO_AD_MET(chat_id)
        return

    if text == '/tt' and user.tariff == TARIFICATION.tarif_dungeon_master:
        gs = gsheet()
        msgs = gs.get_msgs(user.date1,user.date1)
        for msg in msgs:
            bot.send_message(chat_id=chat_id, text=msg)
        return


    if text == '/master' and user.tariff == TARIFICATION.tarif_dungeon_master:
        msg = ''
        msg += '/users\n'
        msg += '/usersandlogins\n'
        msg += '/logs\n'
        msg += '/tt\n'
        bot.send_message(chat_id=chat_id, text=msg)
        return

    if '/toall' in text and user.tariff == TARIFICATION.tarif_dungeon_master:
        msg = text.replace('/toall', '')
        users = bdb.get_all_Users()
        for us in users:
            try:
                bot.send_message(chat_id=us.chat_id, text=msg)
            except:
                pass
        return

    if text == '/users' and user.tariff == TARIFICATION.tarif_dungeon_master:
        users_amount = len(bdb.get_all_Users())
        msg = f'Пользователей : {users_amount}'
        bot.send_message(chat_id=chat_id, text=msg)
        return

    if text == '/usersandlogins' and user.tariff == TARIFICATION.tarif_dungeon_master:
        msg = ''
        users = bdb.get_all_Users()
        for user in users:
            logins = bdb.get_all_Logins(user)
            if logins != None:
                log_am = len(logins)
            else:
                log_am = 0

            msg += f'{user.chat_id} : {log_am}\n'
        bot.send_message(chat_id=chat_id, text=msg)
        return

    if '/logs' in text and user.tariff == TARIFICATION.tarif_dungeon_master:
        logs = bdb.get_logs()
        file = 'documents/logs.csv'
        with open(file, 'w') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            for row in logs:
                wr.writerow(row)
        bot.send_document(chat_id, open(file, 'rb'))

    if text == '/dates' or text == STAT_LOGIN.SET_DATES_MENU:
        bot.send_message(chat_id=chat_id,
                         text="Установите даты отчета. Сейчас они установлены на:\nДата начала : {}\nДата конца : {}".format(
                             user.date1, user.date2), reply_markup=keyboards.DATES_PRESETS_KEYBOARD())
        return

    if text == '/help' or text == STAT_LOGIN.SET_DATES_MENU:
        bot.send_message(chat_id=chat_id, text="Отвечу на ваши вопросы.", reply_markup=keyboards.HELP_KEYBOARD())
        return

    if text == '/helpsettings':
        bot.send_message(chat_id=chat_id, text="Сейчас расскажу что делает каждая кнопка:")
        time.sleep(1)
        bot.send_message(chat_id=chat_id,
                         text=f"*{SET_LOGIN.SET_NAME}* : Меняет название метрики в списке выбора Метрики. Это очень удобно",
                         parse_mode='Markdown')
        time.sleep(2)
        bot.send_message(chat_id=chat_id,
                         text=f'*{SET_LOGIN.SET_TOKEN}* : Настраивает Токен для цели. Токен - это ключ, который позволяет получать данные из Яндекс Метрики. Токен можно плучить по ссылке:',
                         parse_mode='Markdown')
        bot.send_message(chat_id=chat_id,
                         text='https://oauth.yandex.ru/authorize?response_type=token&client_id=2ca9c7117f3d4797b6cf9a67db7db0c2')
        bot.send_message(chat_id=chat_id,
                         text='Получать токен нужно под тем логином Яндекса, который имеет доступ к нужному счетчику Метркии.')
        time.sleep(3)
        bot.send_message(chat_id=chat_id,
                         text=f'*{SET_LOGIN.SET_TARGETS}* : Настраивает отслеживаемые цели Яндекс Метрики. Нужно ввести номер необходимых целей через запятую. ',
                         parse_mode='Markdown')
        time.sleep(1)
        bot.send_message(chat_id=chat_id,
                         text='Чтобы узнать номер целей, зайдите в Метрику. Нажмите в левом меню Настройки, далее нажмите Цели. Напротив названия каждой цели есть её номер.')
        time.sleep(2)
        bot.send_message(chat_id=chat_id,
                         text=f'*{SET_LOGIN.SET_DIR_LOGIN}* : Настраивает логин Директа для получения расходов РК. В него нужно ввести почту Директа без @yandex.ru в конце. Вы должны ввести ту же почту, через которую подключали счетчик.',
                         parse_mode='Markdown')
        time.sleep(1)
        bot.send_message(chat_id=chat_id,
                         text=f'*{SET_LOGIN.SET_DEL_LOGIN}* : Удаляет метрику. Для этого нужно ввести ID Метрики после запроса.',
                         parse_mode='Markdown')
        time.sleep(1)
        bot.send_message(chat_id=chat_id,
                         text='Полную инструкцию по настройке метрики можно посмотреть вот тут: https://www.youtube.com/watch?v=PxBRXF221ns&feature=emb_logo')
        return

    if text == '/helpstat':
        bot.send_message(chat_id=chat_id, text="Сейчас расскажу что делает каждая кнопка:")
        time.sleep(1)
        bot.send_message(chat_id=chat_id,
                         text=f"*{STAT_LOGIN.GET_STAT}* : Анализ рекламы по большому количеству параметров.",
                         parse_mode='Markdown')
        time.sleep(1)
        bot.send_message(chat_id=chat_id, text=f"*{STAT_LOGIN.GET_PLATFORMS}* : Удобна для минусации площадок в РСЯ.",
                         parse_mode='Markdown')
        time.sleep(1)
        bot.send_message(chat_id=chat_id, text=f"*{STAT_LOGIN.GET_QUICK_STAT}* : Быстрая статитикая Яндекс Директа.",
                         parse_mode='Markdown')
        time.sleep(1)
        bot.send_message(chat_id=chat_id, text=f"*{STAT_LOGIN.GET_STAT_BY_DAY}* : Анализирует рекламу по дням недели.",
                         parse_mode='Markdown')
        time.sleep(1)
        bot.send_message(chat_id=chat_id,
                         text=f"*{STAT_LOGIN.SET_DATES_MENU}* : Вызывает меню настройки дат. Подробнее о нём : /helpdates",
                         parse_mode='Markdown')
        time.sleep(1)
        bot.send_message(chat_id=chat_id,
                         text=f"Подробнее о статитике можно посмотреть тут : https://www.youtube.com/watch?v=T3rVMut_0fg&feature=emb_logo")

        return

    # Начальный диалог
    if dp([MASTER.MAIN_MENU, MASTER.NEW_USER_SEQUENCE]) in user.dialog_position:
        if NEW_USER_SEQUENCE.STEP_1 in user.dialog_position:
            try:
                id = int(text.replace(" ", ""))
                login = bdb.set_Login(user, id)
                user.dialog_position = dp([MASTER.MAIN_MENU, MASTER.NEW_USER_SEQUENCE, NEW_USER_SEQUENCE.STEP_2])
                user.choosed_element = str(login.met_id)
                user.save()

                bot.send_message(chat_id=chat_id, text="Метрика {} добавлена".format(id))
                time.sleep(1)
                bot.send_message(chat_id=chat_id, text="Теперь нужно добавить Токен от метрики.")
                time.sleep(1)
                bot.send_message(chat_id=chat_id,
                                 text="Для этого перейдите по ссылке под припреленным к метрике аккаунтом Яндекса:")
                bot.send_message(chat_id=chat_id,
                                 text="https://oauth.yandex.ru/authorize?response_type=token&client_id=849a60b03ba84617bf45bb53d2a90b7c")
                bot.send_message(chat_id=chat_id, text="И скопируйте и вставьте сюда Токен:")
            except:
                bot.send_message(chat_id=chat_id, text='Вы ввели неправильный ID. Повторите попытку.')
            return

        if NEW_USER_SEQUENCE.STEP_2 in user.dialog_position:
            login = bdb.get_Login(user, int(user.choosed_element))
            login.token = text.replace(" ", "")
            user.dialog_position = dp([MASTER.MAIN_MENU, MASTER.NEW_USER_SEQUENCE, NEW_USER_SEQUENCE.STEP_3])
            user.save()
            login.save()
            bot.send_message(chat_id=chat_id, text="Токен установлен.")
            time.sleep(1)
            bot.send_message(chat_id=chat_id, text="Тепер вы можете получать статитику с аккаунта Метрики.")
            time.sleep(1)
            bot.send_message(chat_id=chat_id, text="Для этого нужно выбрать даты отчета.")
            time.sleep(1)
            bot.send_message(chat_id=chat_id, text="Укажите дату начала в формате 2020-09-01")
            return

        if NEW_USER_SEQUENCE.STEP_3 in user.dialog_position:
            if is_date_valid(text):
                user.date1 = text
                user.save()
                bot.send_message(chat_id=chat_id, text="Дата начала установлена.")
                bot.send_message(chat_id=chat_id, text="Теперь укажите дату конца в формате 2020-09-30")
                user.dialog_position = dp([MASTER.MAIN_MENU, MASTER.NEW_USER_SEQUENCE, NEW_USER_SEQUENCE.STEP_4])
                user.save()
            else:
                Back(user, chat_id, text="Неверно введена дата. Укажите дату начала в формате 2020-09-01")
            return

        if NEW_USER_SEQUENCE.STEP_4 in user.dialog_position:
            if is_date_valid(text):
                user.date2 = text
                user.dialog_position = dp([MASTER.MAIN_MENU, MASTER.LOGINS_MENU, MASTER.CHOOSE_VAR])
                user.save()
                bot.send_message(chat_id=chat_id,
                                 text="Дата конца установлена. Теперь вы можете запрашивать анализ статитики.")
                time.sleep(1)
                bot.send_message(chat_id=chat_id,
                                 text="Чтобы настраивать цели метрики и узнавать расход Яндекс Директа посмотрите инструкцию: http://proshebot.ru/instructions")
                time.sleep(1)
                login = bdb.get_Login(user, int(user.choosed_element))
                bot.send_message(chat_id=chat_id, text="Выбрана метрика {}".format(login.met_id),
                                 reply_markup=keyboards.CHOOSE_VAR())
            else:
                Back(user, chat_id, text="Неверно введена дата. Укажите дату конца в формате 2020-09-30")
            return

    if user.dialog_position == MASTER.MAIN_MENU:
        bot.send_message(chat_id=chat_id, text="Меню", reply_markup=keyboards.MAIN_MENU())
        user.dialog_position = dp(MASTER.MAIN_MENU)
        user.save()

    if user.tariff == TARIFICATION.tarif_free:
        bot.send_message(chat_id=chat_id,
                         text=f"У вас не установлен тариф! Чтобы пользоваться ботом введите ключ от тарифа /key. Подробнее о тарифах на сайте http://proshebot.ru/tariffs", parse_mode="Markdown")
        return

    # Добавление метрики
    if user.dialog_position == dp([MASTER.MAIN_MENU, MASTER.LOGINS_MENU, LOGINS_MENU.LOGINS_ADD]):
        try:
            id = int(text)
            login = bdb.set_Login(user, id)
            user.choosed_element = str(id)
            user.dialog_position = dp([MASTER.MAIN_MENU, MASTER.LOGINS_MENU, MASTER.CHOOSE_VAR, MASTER.SET_LOGIN])
            user.save()
            bot.send_message(chat_id=chat_id,
                             text=f"Добавлена метрика {id}. Теперь нужно настроить Токен.\nНажмите *{SET_LOGIN.SET_TOKEN}*.",
                             reply_markup=keyboards.SET_LOGIN(), parse_mode="Markdown")
        except:
            bot.send_message(chat_id=chat_id, text='Вы ввели неправильный ID')

    # Изменение имени метрики
    if user.dialog_position == dp(
            [MASTER.MAIN_MENU, MASTER.LOGINS_MENU, MASTER.CHOOSE_VAR, MASTER.SET_LOGIN, SET_LOGIN.SET_NAME]):
        login = bdb.get_Login(user, int(user.choosed_element))
        login.name = text
        login.save()
        Back(user, chat_id, "Метрика теперь назыается {}:{}".format(text, int(user.choosed_element)))

    # Изменение Токена
    if user.dialog_position == dp(
            [MASTER.MAIN_MENU, MASTER.LOGINS_MENU, MASTER.CHOOSE_VAR, MASTER.SET_LOGIN, SET_LOGIN.SET_TOKEN]):
        login = bdb.get_Login(user, int(user.choosed_element))
        login.token = text
        login.save()
        Back(user, chat_id, "Токен установлен")

    # Изменение Чата постинга
    if user.dialog_position == dp(
            [MASTER.MAIN_MENU, MASTER.LOGINS_MENU, MASTER.CHOOSE_VAR, MASTER.SET_LOGIN, SET_LOGIN.SET_CHANNEL_TO_POST]):
        login = bdb.get_Login(user, int(user.choosed_element))
        login.channel_to_post = text.replace("https://t.me/", "")
        login.save()
        Back(user, chat_id, "Чат установлен")

    # Изменение Факта постинга
    if user.dialog_position == dp(
            [MASTER.MAIN_MENU, MASTER.LOGINS_MENU, MASTER.CHOOSE_VAR, MASTER.SET_LOGIN,
             SET_LOGIN.SET_OK_TO_POST]):
        login = bdb.get_Login(user, int(user.choosed_element))

        msg = 'Настройка не изменена'

        if text == UCOMANDS.SET_YES:
            login.ok_to_post = True
            msg = 'Теперь отправка идёт в чат'
            login.save()

        if text == UCOMANDS.SET_NO:
            login.ok_to_post = False
            msg = 'Теперь отправка не идёт в чат'
            login.save()
        Back(user, chat_id, msg)

    # Изменение Логина Директа
    if user.dialog_position == dp(
            [MASTER.MAIN_MENU, MASTER.LOGINS_MENU, MASTER.CHOOSE_VAR, MASTER.SET_LOGIN, SET_LOGIN.SET_DIR_LOGIN]):
        login = bdb.get_Login(user, int(user.choosed_element))
        login.dir_client = text
        login.save()
        Back(user, chat_id, "Логин Директа установлен")

    # Изменение целей
    if user.dialog_position == dp(
            [MASTER.MAIN_MENU, MASTER.LOGINS_MENU, MASTER.CHOOSE_VAR, MASTER.SET_LOGIN, SET_LOGIN.SET_TARGETS]):
        login = bdb.get_Login(user, int(user.choosed_element))
        old_targets = bdb.get_all_Targets(login)
        if old_targets is not None:
            for i in old_targets:
                i.delete_instance()

        if text != "-":
            for i in text.replace(" ", "").split(","):
                bdb.set_Target(target=int(i), login=login)
            Back(user, chat_id, "Цели установлены")
        else:
            Back(user, chat_id, "Цели удалены")

    # Удаление метрики
    if user.dialog_position == dp(
            [MASTER.MAIN_MENU, MASTER.LOGINS_MENU, MASTER.CHOOSE_VAR, MASTER.SET_LOGIN, SET_LOGIN.SET_DEL_LOGIN]):
        clogin = int(user.choosed_element)
        if clogin == int(text):
            login = bdb.get_Login(user, clogin)
            login.delete_instance()
            user.dialog_position = dp([MASTER.MAIN_MENU, MASTER.LOGINS_MENU])
            user.save()
            bot.send_message(chat_id=chat_id, text="Метрика {} удалена".format(text),
                             reply_markup=keyboards.LOGINS_MENU())

    if STAT_LOGIN.SET_DATE_1 in user.dialog_position:
        if is_date_valid(text):
            if TARIFICATION.TARIFICATION:
                try:
                    date_set = datetime.strptime(text, '%Y-%m-%d')
                    days_back = TARIFICATION.tarif_values[user.tariff][TARIFICATION.days_back]
                    date_max = datetime.now() - timedelta(days=days_back)
                    if date_set >= date_max:
                        user.date1 = text
                        user.save()
                        Back(user, chat_id, text="Дата 1 установлена")
                    else:
                        user.date1 = date_max.strftime('%Y-%m-%d')
                        user.save()
                        Back(user, chat_id,
                             text="Дата 1 установлена на {} число.\nВаш тариф не позволяет делать запросы на более чем {} дней от текущей даты.\nПодробнее о тарифах вы можете узнать тут: http://proshebot.ru/tariffs".format(
                                 user.date1, days_back))
                    return
                except:
                    Back(user, chat_id, text="Неверно введена дата")
                    return
            else:
                user.date1 = text
                user.save()
                Back(user, chat_id, text="Дата 1 установлена")

        else:
            Back(user, chat_id, text="Неверно введена дата")
            return

    if STAT_LOGIN.SET_DATE_2 in user.dialog_position:
        if is_date_valid(text):
            if TARIFICATION.TARIFICATION:
                try:
                    date_set = datetime.strptime(text, '%Y-%m-%d')
                    days_back = TARIFICATION.tarif_values[user.tariff][TARIFICATION.days_back]
                    date_max = datetime.now() - timedelta(days=days_back)
                    if date_set >= date_max:
                        user.date2 = text
                        user.save()
                        Back(user, chat_id, text="Дата 2 установлена")
                    else:
                        user.date2 = date_max.strftime('%Y-%m-%d')
                        user.save()
                        Back(user, chat_id,
                             text="Дата 2 установлена на {} число.\nВаш тариф не позволяет делать запросы на более чем {} дней от текущей даты.\nПодробнее о тарифах вы можете узнать тут: http://proshebot.ru/tariffs".format(
                                 user.date1, days_back))
                    return
                except:
                    Back(user, chat_id, text="Неверно введена дата")
                    return
            else:
                user.date2 = text
                user.save()
                Back(user, chat_id, text="Дата 2 установлена")

        else:
            Back(user, chat_id, text="Неверно введена дата")
            return

    # Выбор Метрики
    if user.dialog_position == dp([MASTER.MAIN_MENU, MASTER.LOGINS_MENU, UCOMANDS.ACT]):
        try:
            id = int(text.split(":")[-1])
            login = bdb.get_Login(user, id)
            user.choosed_element = str(id)
            user.dialog_position = dp([MASTER.MAIN_MENU, MASTER.LOGINS_MENU, MASTER.CHOOSE_VAR])
            user.save()
            bread_crumbs(user.dialog_position, chat_id)
            bot.send_message(chat_id=chat_id, text="Выбрана метрика {}".format(bdb.get_full_name(login)),
                             reply_markup=keyboards.CHOOSE_VAR())
            return
        except:
            Back(user, chat_id, text='Вы ввели неправильный ID')

    if text == '/metmenu':
        try:
            login = bdb.get_Login(user, int(user.choosed_element))
            user.dialog_position = dp([MASTER.MAIN_MENU, MASTER.LOGINS_MENU, MASTER.CHOOSE_VAR])
            user.save()
            bread_crumbs(user.dialog_position, chat_id)
            bot.send_message(chat_id=chat_id, text="Выбрана метрика {}".format(bdb.get_full_name(login)),
                             reply_markup=keyboards.CHOOSE_VAR())
            return
        except:
            Back(user, chat_id, text='Вы ввели неправильный ID')

    # Метрики
    if text == MAIN_MENU.LOGINS or text == '/metrics':
        user.dialog_position = dp([MASTER.MAIN_MENU, MASTER.LOGINS_MENU])
        user.save()
        bot.send_message(chat_id=chat_id, text=bread_crumbs(user.dialog_position), reply_markup=keyboards.LOGINS_MENU())
        return

    # Быстрая статистика по всем аккаунтам
    if text == MAIN_MENU.QUICK_STAT or text == '/dir':
        logins = bdb.get_all_Logins(user)
        requests = 0
        for login in logins:
            if login.token != None and user.date1 != None and user.date2 != None and login.dir_client != None:
                if not dates_is_ok(user, chat_id):
                    return

                if not dates_is_ok(user, chat_id):
                    return

                try:
                    targets_list = bdb.get_all_Targets(login)
                    targets = []
                    for i in targets_list:
                        targets.append(int(i.target))

                    met = metuser(met_id=login.met_id, targets=targets,
                                  token=login.token, dir_client=login.dir_client)
                    msg = "Метрика : {}\n".format(login.name)
                    msg += met.quick_stat([user.date1, user.date2])
                    bot.send_message(chat_id=chat_id, text=msg)
                    requests += 1

                    if login.channel_to_post is not None and login.ok_to_post and login.channel_to_post != "-":
                        try:
                            bot.send_message(chat_id='@{}'.format(login.channel_to_post), text=msg)
                        except:
                            name = str(login.met_id)
                            if login.name != None:
                                name += f":{login.name}"
                            bot.send_message(chat_id=chat_id,
                                             text="Ошибка при сборе отправки статистики счетчика {}\nСпособы решения проблемы можно посмотреть тут http://proshebot.ru/instructions#errors".format(
                                                 name))
                except:
                    name = str(login.met_id)
                    if login.name != None:
                        name += f":{login.name}"
                    bot.send_message(chat_id=chat_id,
                                     text="Ошибка при сборе отправки статистики счетчика {}\nСпособы решения проблемы можно посмотреть тут http://proshebot.ru/instructions#errors".format(
                                         name))
                time.sleep(0.3)

        user.request_today += requests
        user.save()

        return

    # Быстрая статистика по аккаунту
    if text == STAT_LOGIN.GET_QUICK_STAT:
        login = bdb.get_Login(user, int(user.choosed_element))
        if login.token != None and user.date1 != None and user.date2 != None and login.dir_client != None:
            if not dates_is_ok(user, chat_id):
                return

            if not is_over_request(user, chat_id):
                return

            try:
                targets_list = bdb.get_all_Targets(login)
                targets = []
                for i in targets_list:
                    targets.append(int(i.target))
                print(targets)
                met = metuser(met_id=login.met_id, targets=targets,
                              token=login.token, dir_client=login.dir_client)
                msg = "Метрика : {}\n".format(login.name)
                msg += met.quick_stat([user.date1, user.date2])
                bot.send_message(chat_id=chat_id, text=msg)
                user.request_today += 1
                user.save()

                if login.channel_to_post is not None and login.ok_to_post and login.channel_to_post != "-":
                    try:
                        bot.send_message(chat_id='@{}'.format(login.channel_to_post), text=msg)
                    except:
                        bot.send_message(chat_id=chat_id,
                                         text="Ошибка при сборе отправки статистики метрики {} в прикреплёный чат. Способы решения проблемы можно посмотреть тут http://proshebot.ru/instructions#errors".format(
                                             login.met_id))
            except:
                bot.send_message(chat_id=chat_id,
                                 text="Ошибка при сборе статистики метрики {}. Способы решения проблемы можно посмотреть тут http://proshebot.ru/instructions#errors".format(
                                     login.met_id))
        elif login.token == None:
            bot.send_message(chat_id=chat_id, text="Токен не указан.".format(login.met_id))
        elif login.dir_client is None:
            bot.send_message(chat_id=chat_id,
                             text="Не указан логин Яндекс Дриректа. Посмотрите инструкцию как это сделать : http://proshebot.ru/instructions".format(
                                 login.met_id))
        else:
            bot.send_message(chat_id=chat_id,
                             text="Ошибка при сборе статистики метрики {}. Способы решения проблемы можно посмотреть тут http://proshebot.ru/instructions#errors".format(
                                 login.met_id))
        return

    # Выбрать настройки
    if text == CHOOSE_VAR.CHOOSE_SET or text == '/settings':
        user.dialog_position = dp([MASTER.MAIN_MENU, MASTER.LOGINS_MENU, MASTER.CHOOSE_VAR, MASTER.SET_LOGIN])
        user.save()
        bread_crumbs(user.dialog_position, chat_id)
        bot.send_message(chat_id=chat_id,
                         text='Настройки Метрики. Подробнее о настройках можно узнать тут /helpsettings',
                         reply_markup=keyboards.SET_LOGIN())
        return

    # Открыть профиль
    if text == MAIN_MENU.PROFILE or text == '/profile':
        user.dialog_position = dp([MASTER.MAIN_MENU, MASTER.PROFILE])
        user.save()
        bot.send_message(chat_id=chat_id, text=bread_crumbs(user.dialog_position), reply_markup=keyboards.PROFILE())
        return

    # Ввести ключ
    if text == PROFILE.USE_KEY:
        bot.send_message(chat_id=chat_id, text='Введите ваш ключ:', reply_markup=keyboards.just_BACK())
        user.dialog_position = dp([MASTER.MAIN_MENU, MASTER.PROFILE, PROFILE.USE_KEY])
        user.save()
        return

    # О профиле
    if text == PROFILE.ABOUT:
        msg = ''
        TV = TARIFICATION.tarif_values[user.tariff]
        msg += 'Ваш тариф : {}\n'.format(TV["name"])
        logins = bdb.get_all_Logins(user)
        if user.tariff != TARIFICATION.tarif_free and user.tariff != TARIFICATION.tarif_vip and user.tariff != TARIFICATION.tarif_dungeon_master:
            msg += 'Оплачен до : {}\n'.format(user.end_tariff.strftime("%Y-%m-%d"))
        msg += "Количество подключенных метрик : {} из {}\n".format(len(logins), TV[TARIFICATION.amount_of_metrics])
        msg += "Запросов в день : {} из {}\n".format(user.request_today, TV[TARIFICATION.amount_of_request])
        msg += "Максимальная длинна запроса : {} дней\n".format(TV[TARIFICATION.days_max_range])
        msg += "Подробнее о тарифах вы можете узнать тут: http://proshebot.ru/tariffs"

        bot.send_message(chat_id=chat_id, text=msg)
        bread_crumbs(user.dialog_position, chat_id)
        return

    # О профиле
    if text == PROFILE.BUY_KEY:
        msg = "Купить ключ можно написав мне напрямую @TheSuperD20\nПодробнее о тарифах и ценах вы можете узнать тут: http://proshebot.ru/tariffs"
        bot.send_message(chat_id=chat_id, text=msg)
        return

    # О боте
    if text == MAIN_MENU.ABOUT:
        bot.send_message(chat_id=chat_id,
                         text='Инструкция по работе с ботом : http://proshebot.ru/instructions\nПо возникшим вопросам пишите @TheSuperD20')
        bot.send_message(chat_id=chat_id, text="Отвечу на ваши вопросы.", reply_markup=keyboards.HELP_KEYBOARD())
        return

    # Выбрать статистику
    if text == CHOOSE_VAR.CHOOSE_STAT or text == "/stat":
        clogin = int(user.choosed_element)
        login = bdb.get_Login(user, clogin)

        out_str = str(bdb.get_full_name(login)) + "\n"
        if user.date1 != None:
            out_str += "Дата начала : {}\n".format(user.date1)
        else:
            out_str += "Дата начала не указана\n"

        if user.date2 != None:
            out_str += "Дата конца : {}\n".format(user.date2)
        else:
            out_str += "Дата конца не указана\n"

        out_str += "Помощь по статитике: /helpstat"

        if login.token == None:
            out_str += "\nТокен не указан!"

        user.dialog_position = dp([MASTER.MAIN_MENU, MASTER.LOGINS_MENU, MASTER.CHOOSE_VAR, MASTER.STAT_LOGIN])
        user.save()
        bread_crumbs(user.dialog_position, chat_id)
        bot.send_message(chat_id=chat_id, text=out_str, reply_markup=keyboards.STAT_LOGIN())

        return

    # Информация о метрике
    if text == CHOOSE_VAR.CHOOSE_INFO:
        login = bdb.get_Login(user, int(user.choosed_element))
        met_id = login.met_id
        token = login.token
        name = login.name
        dir_client = login.dir_client
        tl = bdb.get_all_Targets(login)
        if tl is not None:
            targets = ""
            for i in tl:
                targets += str(i.target) + ","
            targets = targets[:-1]
        else:
            targets = "Цели не заданы"
        out = "ID Метрики : {}\nИмя : {}\nТокен : {}\nЦели : {}\nЛогин Директа : {}".format(met_id, name, token,
                                                                                            targets,
                                                                                            dir_client)
        bot.send_message(chat_id=chat_id, text=out)
        return

    # Выбрать Метрики
    if text == LOGINS_MENU.LOGINS_CHOOSE or text == '/choose':
        logins = bdb.get_all_Logins(user)
        if logins:
            met_ids = []
            for i in logins:
                if i.name:
                    met_ids.append(i.name + ":" + str(i.met_id))
                else:
                    met_ids.append(i.met_id)
            cur_amount = TARIFICATION.tarif_values[user.tariff][TARIFICATION.amount_of_metrics]
            if len(met_ids) > cur_amount:
                met_ids = met_ids[cur_amount:]
                bot.send_message(chat_id=chat_id,
                                 text='Ваша тариф закончился, поэтому вам отобаржается только {} метрик из {}. Продлите тариф!\nПодробнее о тарифах вы можете узнать тут: http://proshebot.ru/tariffs'.format(
                                     cur_amount, len(met_ids)))

            user.dialog_position = dp([MASTER.MAIN_MENU, MASTER.LOGINS_MENU, UCOMANDS.ACT])
            user.save()
            bot.send_message(chat_id=chat_id, text='Выберите метрику', reply_markup=keyboards.LOGINS_KEYBOARD(met_ids))
            return
        else:
            bot.send_message(chat_id=chat_id,
                             text="У вас нет прикреплённых метрик. Добавьте метрику. Для этого нажмите /admet",
                             reply_markup=keyboards.LOGINS_MENU())

    # Получить статитику
    if text == STAT_LOGIN.GET_STAT:
        clogin = int(user.choosed_element)
        login = bdb.get_Login(user, clogin)
        if login.token != None and user.date1 != None and user.date2 != None:

            if not dates_is_ok(user, chat_id):
                return

            if not is_over_request(user, chat_id):
                return

            try:
                bot.send_message(chat_id=chat_id,
                                 text='Собираем статистику...')
                targets_list = bdb.get_all_Targets(login)
                targets = []
                if targets_list is not None:
                    for i in targets_list:
                        targets.append(int(i.target))

                met = metuser(met_id=login.met_id, targets=targets,
                              token=login.token, dir_client=login.dir_client)
                file = met.make_file([user.date1, user.date2])
                bot.send_document(message.from_user.id, open(file, 'rb'))
                user.request_today += 1
                user.save()
                os.remove(file)
                if len(met.errors) > 1:
                    bot.send_message(chat_id=chat_id,
                                     text='При сборе статитики произошли следующие ошибки!')
                    for i in met.errors:
                        bot.send_message(chat_id=chat_id,
                                         text='{}'.format(i))
                    return
            except:
                bot.send_message(chat_id=chat_id,
                                 text='Произошла ошибка при сборе статистики. Настройки метрики указаны не верно. Способы решения проблемы можно посмотреть тут http://proshebot.ru/instructions#errors')
                print("Ошибки : {}".format(met.errors))
                if len(met.errors) > 0:
                    bot.send_message(chat_id=chat_id,
                                     text='При сборе статитики произошли следующие ошибки:')
                    for i in met.errors:
                        bot.send_message(chat_id=chat_id,
                                         text='{}'.format(i))
        else:
            if login.token == None:
                bot.send_message(chat_id=chat_id,
                                 text='Вы не указали Токен для метрики! Мы не можем получить статитику!')
            if user.date1 == None or user.date2 == None:
                bot.send_message(chat_id=chat_id,
                                 text='Вы не указали даты статистики!')

    # Получить Платформы
    if text == STAT_LOGIN.GET_PLATFORMS:
        clogin = int(user.choosed_element)
        login = bdb.get_Login(user, clogin)
        if login.token != None and user.date1 != None and user.date2 != None:

            if not is_over_request(user, chat_id):
                return

            if not dates_is_ok(user, chat_id):
                return

            try:
                bot.send_message(chat_id=chat_id,
                                 text='Собираем статистику...')
                targets_list = bdb.get_all_Targets(login)
                targets = []
                if targets_list is not None:
                    for i in targets_list:
                        targets.append(int(i.target))

                met = metuser(met_id=login.met_id, targets=targets,
                              token=login.token, dir_client=login.dir_client)
                file = met.make_file_platforms([user.date1, user.date2])
                bot.send_document(message.from_user.id, open(file, 'rb'))
                user.request_today += 1
                user.save()
                os.remove(file)
                if len(met.errors) > 1:
                    bot.send_message(chat_id=chat_id,
                                     text='При сборе статитики произошли следующие ошибки!')
                    for i in met.errors:
                        bot.send_message(chat_id=chat_id,
                                         text='{}'.format(i))
                    return
            except:
                bot.send_message(chat_id=chat_id,
                                 text='Произошла ошибка при сборе статистики. Настройки метрики указаны не верно. Способы решения проблемы можно посмотреть тут http://proshebot.ru/instructions#errors')
                print("Ошибки : {}".format(met.errors))
                if len(met.errors) > 0:
                    bot.send_message(chat_id=chat_id,
                                     text='При сборе статитики произошли следующие ошибки:')
                    for i in met.errors:
                        bot.send_message(chat_id=chat_id,
                                         text='{}'.format(i))
        else:
            if login.token == None:
                bot.send_message(chat_id=chat_id,
                                 text='Вы не указали Токен для метрики! Мы не можем получить статитику!')
            if user.date1 == None or user.date2 == None:
                bot.send_message(chat_id=chat_id,
                                 text='Вы не указали даты статистики!')

    # Получить статитику по дням
    if text == STAT_LOGIN.GET_STAT_BY_DAY:
        clogin = int(user.choosed_element)
        login = bdb.get_Login(user, clogin)
        if login.token != None and user.date1 != None and user.date2 != None:

            if not dates_is_ok(user, chat_id):
                return

            if not is_over_request(user, chat_id):
                return

            try:
                bot.send_message(chat_id=chat_id,
                                 text='Собираем статистику...')
                targets_list = bdb.get_all_Targets(login)
                targets = []
                if targets_list is not None:
                    for i in targets_list:
                        targets.append(int(i.target))

                met = metuser(met_id=login.met_id, targets=targets,
                              token=login.token, dir_client=login.dir_client)
                file = met.make_file_by_time([user.date1, user.date2])
                bot.send_document(message.from_user.id, open(file, 'rb'))
                user.request_today += 1
                user.save()
                os.remove(file)
                if len(met.errors) > 1:
                    bot.send_message(chat_id=chat_id,
                                     text='При сборе статитики произошли следующие ошибки!')
                    for i in met.errors:
                        bot.send_message(chat_id=chat_id,
                                         text='{}'.format(i))
                return
            except:
                bot.send_message(chat_id=chat_id,
                                 text='Произошла ошибка при сборе статистики. Настройки метрики указаны не верно. Способы решения проблемы можно посмотреть тут http://proshebot.ru/instructions#errors')
                print("Ошибки : {}".format(met.errors))
                if len(met.errors) > 0:
                    bot.send_message(chat_id=chat_id,
                                     text='При сборе статитики произошли следующие ошибки:')
                    for i in met.errors:
                        bot.send_message(chat_id=chat_id,
                                         text='{}'.format(i))
        else:
            if login.token == None:
                bot.send_message(chat_id=chat_id,
                                 text='Вы не указали Токен для метрики! Мы не можем получить статитику!')
            if user.date1 == None or user.date2 == None:
                bot.send_message(chat_id=chat_id,
                                 text='Вы не указали даты статистики!')

    # Изменить Дату 1
    if text == STAT_LOGIN.SET_DATE_1:
        bot.send_message(chat_id=chat_id, text='Введите дату начала в формате 2020-06-07 (Год-Месяц-День).',
                         reply_markup=keyboards.just_BACK())
        user.dialog_position = dp(
            [MASTER.MAIN_MENU, MASTER.LOGINS_MENU, MASTER.CHOOSE_VAR, MASTER.STAT_LOGIN, STAT_LOGIN.SET_DATE_1])
        user.save()
        return

    # Изменить Дату 2
    if text == STAT_LOGIN.SET_DATE_2:
        bot.send_message(chat_id=chat_id, text='Введите дату конца в формате 2020-06-07 (Год-Месяц-День).',
                         reply_markup=keyboards.just_BACK())
        user.dialog_position = dp(
            [MASTER.MAIN_MENU, MASTER.LOGINS_MENU, MASTER.CHOOSE_VAR, MASTER.STAT_LOGIN, STAT_LOGIN.SET_DATE_2])
        user.save()
        return

    '''
    Настройки Метрики
    '''
    # Изменить Токен
    if text == SET_LOGIN.SET_TOKEN:
        bot.send_message(chat_id=chat_id,
                         text='Токен можно получить тут: https://oauth.yandex.ru/authorize?response_type=token&client_id=2ca9c7117f3d4797b6cf9a67db7db0c2\nВведите Токен',
                         reply_markup=keyboards.just_BACK())
        user.dialog_position = dp(
            [MASTER.MAIN_MENU, MASTER.LOGINS_MENU, MASTER.CHOOSE_VAR, MASTER.SET_LOGIN, SET_LOGIN.SET_TOKEN])
        user.save()
        return

    # Изменить Чат постинга
    if text == SET_LOGIN.SET_CHANNEL_TO_POST:
        bot.send_message(chat_id=chat_id,
                         text='Введите ID чата',
                         reply_markup=keyboards.just_BACK())
        user.dialog_position = dp(
            [MASTER.MAIN_MENU, MASTER.LOGINS_MENU, MASTER.CHOOSE_VAR, MASTER.SET_LOGIN, SET_LOGIN.SET_CHANNEL_TO_POST])
        user.save()
        return

    # Изменить Факт постинга
    if text == SET_LOGIN.SET_OK_TO_POST:
        login = bdb.get_Login(user, int(user.choosed_element))

        if login.ok_to_post:
            msg = 'Сейчас постинг идёт в чат.\nОтключить?'
        else:
            msg = 'Сейчас постинг не идёт в чат.\nВключить?'

        bot.send_message(chat_id=chat_id,
                         text=msg,
                         reply_markup=keyboards.YES_NO_KEYBOARD(login.ok_to_post))
        user.dialog_position = dp(
            [MASTER.MAIN_MENU, MASTER.LOGINS_MENU, MASTER.CHOOSE_VAR, MASTER.SET_LOGIN,
             SET_LOGIN.SET_OK_TO_POST])
        user.save()
        return

    # Изменить цели
    if text == SET_LOGIN.SET_TARGETS:
        bot.send_message(chat_id=chat_id, text='Введите ID целей через запятую без пробелов',
                         reply_markup=keyboards.just_BACK())
        user.dialog_position = dp(
            [MASTER.MAIN_MENU, MASTER.LOGINS_MENU, MASTER.CHOOSE_VAR, MASTER.SET_LOGIN, SET_LOGIN.SET_TARGETS])
        user.save()
        return

    # Изменить Логин Директа
    if text == SET_LOGIN.SET_DIR_LOGIN:
        bot.send_message(chat_id=chat_id, text='Введите управляющий логин от Яндекс Директа без @yandex.ru в конце.',
                         reply_markup=keyboards.just_BACK())
        user.dialog_position = dp(
            [MASTER.MAIN_MENU, MASTER.LOGINS_MENU, MASTER.CHOOSE_VAR, MASTER.SET_LOGIN, SET_LOGIN.SET_DIR_LOGIN])
        user.save()
        return

    # Добавить Метрику
    if text == LOGINS_MENU.LOGINS_ADD:
        ad_met(user, chat_id)

    # Удалить Метрику
    if text == SET_LOGIN.SET_DEL_LOGIN:
        login = user.choosed_element
        bot.send_message(chat_id=chat_id,
                         text='Если вы хотите удалить метрику "{}" то отправьте её ID.'.format(login),
                         reply_markup=keyboards.just_BACK())
        user.dialog_position = dp(
            [MASTER.MAIN_MENU, MASTER.LOGINS_MENU, MASTER.CHOOSE_VAR, MASTER.SET_LOGIN, SET_LOGIN.SET_DEL_LOGIN])
        user.save()
        return

    # Изменить имя метрики
    if text == SET_LOGIN.SET_NAME:
        bot.send_message(chat_id=chat_id, text='Введите имя для метрики', reply_markup=keyboards.just_BACK())
        user.dialog_position = dp(
            [MASTER.MAIN_MENU, MASTER.LOGINS_MENU, MASTER.CHOOSE_VAR, MASTER.SET_LOGIN, SET_LOGIN.SET_NAME])
        user.save()
        return


def is_date_valid(date):
    list = date.split('-')
    try:
        a = int(list[0]) + int(list[1]) + int(list[2])
        return True
    except:
        return False


def Back(user, chat_id, text=None):
    if len(user.dialog_position.split(".")) > 1:
        cur_dia_pos = user.dialog_position.split(".")[:-1]
        try:
            user.dialog_position = dp(cur_dia_pos[:-1])
            user.save()
            if text is not None:
                bot.send_message(chat_id=chat_id, text=text,
                                 reply_markup=keyboards.BACK(cur_dia_pos[-2]))
            else:
                bot.send_message(chat_id=chat_id, text=bread_crumbs(user.dialog_position),
                                 reply_markup=keyboards.BACK(cur_dia_pos[-2]))
        except:
            bot.send_message(chat_id=chat_id, text="Произошла ошибка", reply_markup=keyboards.MAIN_MENU())
            user.dialog_position = dp(MAIN_MENU)
            user.save()
    else:
        bot.send_message(chat_id=chat_id, text="Меню", reply_markup=keyboards.MAIN_MENU())
        user.dialog_position = dp([MASTER.MAIN_MENU])
        user.save()

def ad_met(user, chat_id):
    if is_locked(user.dialog_position):
        bot.send_message(chat_id=chat_id, text='Операция пока невозможна. Чтовы выти на главное меню нажмите /menu')
        return
    logins = bdb.get_all_Logins(user)
    cur_amount = TARIFICATION.tarif_values[user.tariff][TARIFICATION.amount_of_metrics]

    if logins != None:
        if len(logins) > cur_amount:
            bot.send_message(chat_id=chat_id,
                             text='У вас добавлено максимальное количество Метрик для вашего тарифа ({} штук)!\nПодробнее о тарифах вы можете узнать тут: http://proshebot.ru/tariffs'.format(
                                 cur_amount))
            return
    else:
        if cur_amount == 0:
            bot.send_message(chat_id=chat_id,
                             text='У вас добавлено максимальное количество Метрик для вашего тарифа ({} штук)!\nПодробнее о тарифах вы можете узнать тут: http://proshebot.ru/tariffs'.format(
                                 cur_amount))
            return

    bot.send_message(chat_id=chat_id, text='Введите ID Метрики', reply_markup=keyboards.just_BACK())
    user.dialog_position = dp([MASTER.MAIN_MENU, MASTER.LOGINS_MENU, LOGINS_MENU.LOGINS_ADD])
    user.save()
    return


def dates_is_ok(user, chat_id):
    if not TARIFICATION.TARIFICATION:
        return True

    date1 = datetime.strptime(user.date1, '%Y-%m-%d')
    date2 = datetime.strptime(user.date2, '%Y-%m-%d')

    if date2 >= date1:
        date_range = (date2 - date1).days
        days_max_range = TARIFICATION.tarif_values[user.tariff][TARIFICATION.days_max_range]
        if date_range > days_max_range:
            bot.send_message(chat_id=chat_id,
                             text='Вы выбрали слишком большой по времени запрос.\nВаш тариф позволяет делать запросы максимум по {} дней.\nПодробнее о тарифах вы можете узнать тут: http://proshebot.ru/tariffs'.format(
                                 days_max_range))
            return False
    else:
        bot.send_message(chat_id=chat_id,
                         text='Даты указааны не верно, начало запроса идёт после конца!\nДата 1 : {}\nДата 2 : {}'.format(
                             user.date1, user.date2))
        return False
    return True


def is_over_request(user: User, chat_id):
    if not TARIFICATION.TARIFICATION:
        return True
    if user.request_today > TARIFICATION.tarif_values[user.tariff][TARIFICATION.amount_of_request]:
        bot.send_message(chat_id=chat_id,
                         text='Вы привысили количество запросов в день!\nВаш тариф позволяет делать максимум по {} запросов в днень.\nПодробнее о тарифах вы можете узнать тут: http://proshebot.ru/tariffs'.format(
                             TARIFICATION.tarif_values[user.tariff][TARIFICATION.amount_of_request]))
        return False
    # user.request_today += 1
    # user.save()
    return True


def dp(array):
    pos = ''
    for i in array:
        pos += i + '.'
    i = i[:-1]
    return pos


def is_locked(dp):
    for i in LOCKED.List:
        if i in dp:
            return True
    return False


def append_dp(dp, statment):
    return dp + "." + statment


def bread_crumbs(dp, chat_id=None):
    bc = ''
    print(dp)
    list = dp.split('.')
    for i in list:
        if i in MASTER.Dict.keys():
            dict = MASTER.Dict[i]
            bc += f'{dict["name"]} ({dict["command"]}) > '
    bc += 'Вы тут'
    if chat_id != None:
        bot.send_message(chat_id=chat_id, text=bc)
    return bc


def run_pernding():
    while 1:
        try:
            once.run_pending()
        except:
            date = datetime.today()
            print("BD Error : {}".format(date.strptime("%Y-%m-%d %H-%M-%S")))


def infinit_polling():
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except:
            print('Error in infinit_polling')
            # try:
            #     bot.send_message(chat_id=65868829, text='OMG! Я упал в infinit_polling, сделай что - нибудь!')
            # except:
            #     pass
            time.sleep(15)


if __name__ == '__main__':
    threading.Thread(target=run_pernding).start()
    threading.Thread(target=infinit_polling).start()
    # bot.polling(none_stop=True, interval=0)
