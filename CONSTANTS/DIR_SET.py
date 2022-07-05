#! /usr/bin/env python
# -*- coding: utf-8 -*-

class DIR_SET():
    settings = {
        'dimensions': [
            'ym:s:<attribution>DirectClickOrder',
            'ym:s:<attribution>DirectBannerGroup',
            'ym:s:<attribution>DirectPhraseOrCond',
        ],
        'metrics': [
            'ym:s:visits',
            'ym:s:pageviews',
            'ym:s:users',
            'ym:s:bounceRate'
        ]
    }
    dems_def = [{
        'name': '',
        'dimensions': []
    }, {
        'name': '1',
        'dimensions': [0]
    }, {
        'name': '1/2 ',
        'dimensions': [0, 1]
    },
    ]

    dems_def_short = [{
        'name': '',
        'dimensions': []
    }, {
        'name': '1',
        'dimensions': [0]
    }
    ]

    dems_def_one = [{
        'name': '',
        'dimensions': []
    }]

    presets = [
        {
            'settings': {'dimensions': ['ym:s:<attribution>DirectClickOrder'],
                         'metrics': ['ym:s:visits', 'ym:s:pageviews', 'ym:s:users', 'ym:s:bounceRate']},
            'name': 'Директ Сводка',
            'dir_client': False,
            'dimensions': dems_def_one
        },
        {
            'settings': {'dimensions': ['ym:s:<attribution>DirectClickOrder', 'ym:s:<attribution>DirectBannerGroup'],
                         'metrics': ['ym:s:visits', 'ym:s:pageviews', 'ym:s:users', 'ym:s:bounceRate']},
            'name': 'Директ Группы',
            'dir_client': False,
            'dimensions': dems_def_one
        },
        {
            'settings': {'dimensions': ['ym:s:<attribution>DirectClickOrder', 'ym:s:<attribution>DirectBannerGroup',
                                        'ym:s:<attribution>DirectClickBanner', ],
                         'metrics': ['ym:s:visits', 'ym:s:pageviews', 'ym:s:users', 'ym:s:bounceRate']},
            'name': 'Директ Объявления',
            'dir_client': False,
            'dimensions': dems_def
        },
        {
            'settings': {'dimensions': ['ym:s:<attribution>DirectClickOrder', 'ym:s:<attribution>DirectBannerGroup',
                                        'ym:s:<attribution>DirectPhraseOrCond', ],
                         'metrics': ['ym:s:visits', 'ym:s:pageviews', 'ym:s:users', 'ym:s:bounceRate']},
            'name': 'Директ Ключи',
            'dir_client': False,
            'dimensions': dems_def
        },
        {
            'settings': {'dimensions': ['ym:ad:<attribution>DirectOrder'],
                         'metrics': ['ym:ad:visits', ' ym:ad:<currency>AdCost', 'ym:ad:bounceRate']},
            'name': 'Директ Сводка Расходы',
            'dir_client': True,
            'dimensions': dems_def_one
        },
        {
            'settings': {'dimensions': ['ym:ad:<attribution>DirectOrder', 'ym:ad:<attribution>DirectBannerGroup'],
                         'metrics': ['ym:ad:visits', 'ym:ad:<currency>AdCost', 'ym:ad:bounceRate']},
            'name': 'Директ Группы Расходы',
            'dir_client': True,
            'dimensions': dems_def
        },
        {
            'settings': {'dimensions': ['ym:ad:<attribution>DirectOrder', 'ym:ad:<attribution>DirectBannerGroup',
                                        'ym:ad:<attribution>DirectBanner'],
                         'metrics': ['ym:ad:visits', 'ym:ad:<currency>AdCost', 'ym:ad:bounceRate']},
            'name': 'Директ Объявления Расходы',
            'dir_client': True,
            'dimensions': dems_def
        },
        {
            'settings': {'dimensions': ['ym:ad:<attribution>DirectOrder', 'ym:ad:<attribution>DirectBannerGroup',
                                        'ym:ad:<attribution>DirectPhraseOrCond'],
                         'metrics': ['ym:ad:visits', ' ym:ad:<currency>AdCost', 'ym:ad:bounceRate']},
            'name': 'Директ Ключи Расходы',
            'dir_client': True,
            'dimensions': dems_def
        },
        {
            'settings': {'dimensions': ['ym:s:<attribution>DirectClickOrder', 'ym:s:gender', 'ym:s:ageInterval'],
                         'metrics': ['ym:s:visits', 'ym:s:pageviews', 'ym:s:users', 'ym:s:bounceRate']},
            'name': 'Директ Пол и Возраст',
            'dir_client': False,
            'dimensions': dems_def
        }, {
            'settings': {
                'dimensions': ['ym:s:<attribution>DirectClickOrder', 'ym:s:hour'],
                'metrics': ['ym:s:visits', 'ym:s:pageviews', 'ym:s:users', 'ym:s:bounceRate']
            },
            'name': 'По времени суток',
            'dir_client': False,
            'dimensions': dems_def
        }, {
            'settings': {'dimensions': ['ym:s:<attribution>TrafficSource', 'ym:s:<attribution>SourceEngine'],
                         'metrics': ['ym:s:visits', 'ym:s:pageviews', 'ym:s:users', 'ym:s:bounceRate']},
            'dir_client': False,
            'name': 'Источники Сводка',
            'dimensions': dems_def
        }, {
            'settings': {'dimensions': ['ym:s:<attribution>DirectClickOrder', 'ym:s:deviceCategory'],
                         'metrics': ['ym:s:visits', 'ym:s:pageviews', 'ym:s:users', 'ym:s:bounceRate']},
            'name': 'Директ Устройства',
            'dir_client': False,
            'dimensions': dems_def_short
        }
    ]

    presets_by_time = [
        {
            'settings': {'dimensions': ['ym:s:<attribution>DirectClickOrder'],
                         'metrics': ['ym:s:visits', 'ym:s:pageviews', 'ym:s:users', 'ym:s:bounceRate'],
                         'group': ['day']},
            'name': 'Директ Сводка',
            'dir_client': False,
            'dimensions': [{'name': 'Директ Компании ', 'dimensions': []}]
        },
        {
            'settings': {'dimensions': ['ym:ad:<attribution>DirectOrder'],
                         'metrics': ['ym:ad:visits', ' ym:ad:<currency>AdCost', 'ym:ad:bounceRate'],
                         'group': ['day']},
            'name': 'Директ Сводка Расходы',
            'dir_client': True,
            'dimensions': [{'name': 'Директ Компании ', 'dimensions': []}]
        }
    ]

    presets_platforms = [
        {
            'settings': {'dimensions': ['ym:s:<attribution>DirectPlatformType', 'ym:s:<attribution>DirectPlatform'],
                         'metrics': ['ym:s:visits', 'ym:s:pageviews', 'ym:s:users', 'ym:s:bounceRate']},
            'dir_client': False,
            'name': 'Директ Площадки',
            'dimensions': dems_def
        }, {
            'settings': {'dimensions': ['ym:ad:<attribution>DirectPlatformType', 'ym:ad:<attribution>DirectPlatform'],
                         'metrics': ['ym:ad:visits', 'ym:ad:<currency>AdCost', 'ym:ad:bounceRate']},
            'dir_client': True,
            'name': 'Директ Площадки Расходы',
            'dimensions': dems_def
        }
    ]

    quick_stat = {
        'dimensions': [''],
        'metrics': ['ym:ad:visits', ' ym:ad:<currency>AdCost', 'ym:ad:bounceRate'],
    }
