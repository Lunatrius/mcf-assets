#!/usr/bin/env python2.7
import os
import re


def threads(base):
    wikurl = 'http://mc.lunatri.us/wiki/'
    downloadurl = 'http://mc.lunatri.us'
    return [
        {
            'file': '1296949-misc.bbcode',
            't': 1284041,
            'p': 24991373,
            'title': 'Lunatrius\' mods',
            'tag': '1.7.10',
            'tags': [
                'forge',
                'monster spawn highlighter',
                'stackie',
                'ingame info xml',
                'ingame info',
                'light level'
            ],
            'replacement': {
                'sizeh1': '24px',
                'sizeh2': '18px',
                'wikurl': wikurl,
                'downloadurl': downloadurl
            }
        },
        {
            'file': '1468779-schematica.bbcode',
            't': 1285818,
            'p': 25104841,
            'title': 'Schematica',
            'tag': '1.7.10',
            'tags': [
                'forge',
                'schematica',
                'schematic'
            ],
            'replacement': {
                'sizeh1': '18px',
                'sizeh2': '16px',
                'wikurl': wikurl,
                'downloadurl': downloadurl
            }
        }
    ]
