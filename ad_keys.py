#! /usr/bin/env python
# -*- coding: utf-8 -*-

import csv

from DataClasses.BotDataBase import BotDataBase
from DataClasses.BotDataBaseClasses import *
from datetime import datetime, timedelta
from CONSTANTS.TARIFICATION import *

bdb = BotDataBase()

class ad_keys(object):
    def __init__(self):
        with open('keys.csv') as f:
            keys = list(csv.reader(f))

        for key in keys:
            print(key)
            print(key[0])
            print(key[1])
            print(key[2])
            bdb.add_key(key[0],key[1],int(key[2]))


if __name__ == '__main__':
    run = ad_keys()