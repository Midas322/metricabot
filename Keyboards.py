#! /usr/bin/env python
# -*- coding: utf-8 -*-

from telebot import types
from CONSTANTS.DIALOG import *

class Keyboards():
    def SET_LOGIN(self):
        markup = types.ReplyKeyboardMarkup()
        markup.row(SET_LOGIN.SET_NAME,SET_LOGIN.SET_TOKEN)
        markup.row(SET_LOGIN.SET_TARGETS,SET_LOGIN.SET_DIR_LOGIN)
        # markup.row(SET_LOGIN.SET_CHANNEL_TO_POST, SET_LOGIN.SET_OK_TO_POST)
        markup.row(SET_LOGIN.SET_DEL_LOGIN)
        markup.row(UCOMANDS.BACK)
        # markup.one_time_keyboard = True
        return markup

    def MAIN_MENU(self):
        markup = types.ReplyKeyboardMarkup()
        markup.row(MAIN_MENU.LOGINS)
        markup.row(MAIN_MENU.QUICK_STAT)
        # markup.row(MAIN_MENU.ABOUT)
        markup.row(MAIN_MENU.PROFILE,MAIN_MENU.ABOUT)

        return markup

    def LOGINS_MENU(self):
        markup = types.ReplyKeyboardMarkup()
        markup.row(LOGINS_MENU.LOGINS_CHOOSE)
        markup.row(LOGINS_MENU.LOGINS_ADD)
        markup.row(UCOMANDS.BACK)
        # markup.one_time_keyboard = True
        return markup

    def LOGINS_KEYBOARD(self, met_ids):
        markup = types.ReplyKeyboardMarkup()
        for i in met_ids:
            markup.row(str(i))
        markup.row(UCOMANDS.BACK)
        # markup.one_time_keyboard = True
        return markup

    def just_BACK(self):
        markup = types.ReplyKeyboardMarkup()
        markup.row(UCOMANDS.BACK)
        # markup.one_time_keyboard = True
        return markup

    def CHOOSE_VAR(self):
        markup = types.ReplyKeyboardMarkup()
        markup.row(CHOOSE_VAR.CHOOSE_STAT)
        markup.row(CHOOSE_VAR.CHOOSE_INFO,CHOOSE_VAR.CHOOSE_SET)
        markup.row(UCOMANDS.BACK)
        # markup.one_time_keyboard = True
        return markup

    def STAT_LOGIN(self):
        markup = types.ReplyKeyboardMarkup()
        markup.row(STAT_LOGIN.GET_STAT, STAT_LOGIN.GET_PLATFORMS)
        markup.row(STAT_LOGIN.GET_QUICK_STAT, STAT_LOGIN.GET_STAT_BY_DAY)
        markup.row(STAT_LOGIN.SET_DATES_MENU)
        # markup.row(STAT_LOGIN.SET_DATE_1,STAT_LOGIN.SET_DATE_2)
        markup.row(UCOMANDS.BACK)
        # markup.one_time_keyboard = True
        return markup

    def PROFILE(self):
        markup = types.ReplyKeyboardMarkup()
        markup.row(PROFILE.ABOUT)
        markup.row(PROFILE.USE_KEY, PROFILE.BUY_KEY)
        markup.row(UCOMANDS.BACK)
        # markup.one_time_keyboard = True
        return markup

    def YES_NO_KEYBOARD(self, current):
        markup = types.ReplyKeyboardMarkup()
        if current:
            markup.row(UCOMANDS.SET_NO)
        else:
            markup.row(UCOMANDS.SET_YES)
        markup.row(UCOMANDS.BACK)
        # markup.one_time_keyboard = True
        return markup


    def DATES_PRESETS_KEYBOARD(self):
        return self.inline_keyboard(DATES_KEYBOARD.List,DATES_KEYBOARD.Len,DATES_KEYBOARD.TAG)

    def HELP_KEYBOARD(self):
        return self.inline_keyboard(HELP_KEYBOARD.List,HELP_KEYBOARD.Len,HELP_KEYBOARD.TAG)

    def inline_keyboard(self, List, len_row, tag):
        markup = types.InlineKeyboardMarkup(row_width=len_row)
        list = [[]]

        for i in List:
            if len(list[-1]) < len_row:
                list[-1].append(types.InlineKeyboardButton(text=i, callback_data=f'{i}###{tag}'))
                if len(list[-1]) >= len_row:
                    list.append([])

        for i in list:
            markup.add(*i)

        return markup


    def BACK(self, pos):
        DICT = {
            MASTER.MAIN_MENU: self.MAIN_MENU,
            MASTER.LOGINS_MENU: self.LOGINS_MENU,
            MASTER.SET_LOGIN: self.SET_LOGIN,
            MASTER.CHOOSE_VAR: self.CHOOSE_VAR,
            MASTER.STAT_LOGIN: self.STAT_LOGIN,
            MASTER.PROFILE: self.PROFILE
        }
        for i in LOGINS_MENU.List:
            DICT[i] = self.LOGINS_MENU

        for i in SET_LOGIN.List:
            DICT[i] = self.SET_LOGIN

        for i in CHOOSE_VAR.List:
            DICT[i] = self.CHOOSE_VAR

        for i in STAT_LOGIN.List:
            DICT[i] = self.STAT_LOGIN

        for i in PROFILE.List:
            DICT[i] = self.STAT_LOGIN

        print(pos)
        try:
            return DICT[pos]()
        except:
            return MASTER.MAIN_MENU