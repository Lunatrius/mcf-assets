#!/usr/bin/env python
import os
import re


def threads(base):
    wikurl = 'http://mc.lunatri.us/wiki/'
    downloadurl = 'http://mc.lunatri.us/f'
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
                'downloadurl': downloadurl,
                'changelogcore': clean_changelog(base, 'LunatriusCore'),
                'changelogigi': clean_changelog(base, 'InGameInfoXML'),
                'changelogmsh': clean_changelog(base, 'MonsterSpawnHighlighter'),
                'changelogstackie': clean_changelog(base, 'Stackie'),
                'changeloglaserlevel': clean_changelog(base, 'LaserLevel')
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
                'downloadurl': downloadurl,
                'changelog': clean_changelog(base, 'schematica')
            }
        }
    ]


def clean_changelog(base, modid):
    with open(os.path.join(base, modid, 'changelog.txt')) as fh:
        changelog = ''.join(fh.readlines())
    changelog = re.sub('jenkins-[a-zA-Z0-9]+-(?=\d)', '#', changelog)
    changelog = changelog[:2048]
    changelog = changelog[:changelog.rfind('\n\n')]
    return changelog.strip()
