#!/usr/bin/env python
import os
import re


def threads(base):
    downloadurl = 'http://mc.lunatri.us/f'
    return [
        {
            'file': '1296949-misc.bbcode',
            'f': 51,
            't': 1296949,
            'p': 15841019,
            'title': 'Lunatrius\' mods',
            'tag': '1.6.4',
            'tags': [
                'forge',
                'monster spawn highlighter',
                'stackie',
                'ingame info xml',
                'ingame info',
                'light level'
            ],
            'replacement': {
                'downloadurl': downloadurl,
                'changelogigi': clean_changelog(base, 'ingameinfo'),
                'changelogmsg': clean_changelog(base, 'monsterspawnhighlighter'),
                'changelogstackie': clean_changelog(base, 'stackie')
            }
        },
        {
            'file': '1468779-schematica.bbcode',
            'f': 51,
            't': 1468779,
            'p': 17870619,
            'title': 'Schematica',
            'tag': '1.6.4',
            'tags': [
                'forge',
                'schematica',
                'schematic'
            ],
            'replacement': {
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
