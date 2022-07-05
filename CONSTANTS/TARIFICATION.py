#! /usr/bin/env python
# -*- coding: utf-8 -*-

class TARIFICATION(object):
    TARIFICATION = True

    tarif_free = "tarif_free"  # бесплатно - 3 метрики - ограничение запроса длинной до 7 дней, максимум до 1 месяца назад по времени - 5 запросов в день (всегда)

    tarif_junior = "tarif_junior"  # 500 р - 3 метрики (30 дней) - запрос до 1 месяца длинной - ограничение до 6 месяцев - 10 запросов в день
    tarif_middle = "tarif_middle"  # 1000 р -  10 метрик (30 дней) - запрос до 1 года длинной - без ограничения - 30 запросов в день
    tarif_pro = "tarif_pro"  # 2000 р -  25 метрик (30 дней)  - запрос до 3 лет длинной - без ограничения - 150 запросов в день
    tarif_gold = "tarif_gold"  # 4000 р -  50 метрик (30 дней)  - запрос до 5 лет длинной - без ограничения - 1 0000 запросов в день

    tarif_vip = "tarif_vip"  # только друзьям - безлимит (навсегда)
    tarif_dungeon_master = "tarif_dungeon_master"  # только себе - админские права (навсегда)

    days_max_range = 'days_max_range'
    days_back = 'days_back'
    amount_of_request = 'amount_of_request'
    amount_of_metrics = 'amount_of_metrics'

    tarif_values = {
        # tarif_free : {days_max_range: 7, days_back: 30, amount_of_request: 10, amount_of_metrics: 3},
        tarif_free : {days_max_range: 30, days_back: 180, amount_of_request: 30, amount_of_metrics: 0},

        tarif_junior : {days_max_range: 30, days_back: 300, amount_of_request: 200, amount_of_metrics: 5, 'name' : 'Начальный'},
        tarif_middle : {days_max_range: 365, days_back: 7300, amount_of_request: 200, amount_of_metrics: 10, 'name' : 'Продвинутый'},
        tarif_pro : {days_max_range: 1095, days_back: 7300, amount_of_request: 500, amount_of_metrics: 25, 'name' : 'Профессиональный'},
        tarif_gold : {days_max_range: 1825, days_back: 7300, amount_of_request: 4000, amount_of_metrics: 50, 'name' : 'Gold'},

        tarif_vip : {days_max_range: 100000, days_back: 100000, amount_of_request: 100000, amount_of_metrics: 100000, 'name' : 'VIP'},
        tarif_dungeon_master : {days_max_range: 100000, days_back: 100000, amount_of_request: 100000, amount_of_metrics: 100000, 'name' : 'Dungeon master'}

    }
