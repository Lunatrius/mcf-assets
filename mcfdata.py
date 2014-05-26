#!/usr/bin/env python
import os
import re


def threads(base):
    wikurl = 'http://mc.lunatri.us/wiki/'
    downloadurl = 'http://mc.lunatri.us'
    return [
        {
            'file': '1296949-misc.bbcode',
            'f': 51,
            't': 1296949,
            'p': 15841019,
            'title': 'Lunatrius\' mods',
            'tag': '1.7.2',
            'tags': [
                'forge',
                'monster spawn highlighter',
                'stackie',
                'ingame info xml',
                'ingame info',
                'light level'
            ],
            'replacement': {
                'wikurl': wikurl,
                'downloadurl': downloadurl
            }
        },
        {
            'file': '1468779-schematica.bbcode',
            'f': 51,
            't': 1468779,
            'p': 17870619,
            'title': 'Schematica',
            'tag': '1.7.2',
            'tags': [
                'forge',
                'schematica',
                'schematic'
            ],
            'replacement': {
                'wikurl': wikurl,
                'downloadurl': downloadurl
            }
        }
    ]
