# Hugo - UserBot
# Copyright (C) TeamHugoX
#
# This file is a part of < https://github.com/TeamHugoX/Hugo/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamHugoX/Hugo/blob/main/LICENSE/>.
"""
**༄** Commands Available -

•`{i}addprofanity`
   If someone sends bad word in a chat, Then bot will delete that message.

•`{i}remprofanity`
   From chat from Profanity list.

"""

from ProfanityDetector import detector
from pyHugo.dB.nsfw_db import is_profan, profan_chat, rem_profan

from . import eor, events, get_string, hugo_bot, hugo_cmd


@hugo_cmd(pattern="addprofanity$", admins_only=True)
async def addp(e):
    profan_chat(e.chat_id, "mute")
    await eor(e, get_string("prof_1"), time=10)


@hugo_cmd(pattern="remprofanity", admins_only=True)
async def remp(e):
    rem_profan(e.chat_id)
    await eor(e, get_string("prof_2"), time=10)


@hugo_bot.on(events.NewMessage(incoming=True))
async def checkprofan(e):
    chat = e.chat_id
    if is_profan(chat) and e.text:
        x, y = detector(e.text)
        if y:
            await e.delete()
