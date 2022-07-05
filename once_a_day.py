#! /usr/bin/env python
# -*- coding: utf-8 -*-

from DataClasses.BotDataBase import BotDataBase
from DataClasses.BotDataBaseClasses import *
from datetime import datetime, timedelta
from CONSTANTS.TARIFICATION import *

import schedule
import time

bdb = BotDataBase()


class once_a_day(object):
    def __init__(self):
        print("set")
        schedule.every().day.at("00:00").do(self.job)
        # schedule.every().minutes.do(self.job)

        # while 1:
        #     self.run_pending()

    def run_pending(self):
        schedule.run_pending()
        time.sleep(1)

    def job(self):
        users: [User] = bdb.get_all_Users()
        today = datetime.today().date()

        for user in users:
            user.request_today = 0

            if user.end_tariff == None:
                continue

            if user.end_tariff >= today:
                if user.tariff != TARIFICATION.tarif_dungeon_master and user.tariff != TARIFICATION.tarif_vip:
                    user.tariff = TARIFICATION.tarif_free
            user.save()

        print("done")


if __name__ == '__main__':
    run = once_a_day()
