# Hugo - UserBot
# Copyright (C) TeamHugoX
#
# This file is a part of < https://github.com/TeamHugoX/Hugo/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamHugoX/Hugo/blob/main/LICENSE/>.
"""
**༄** Commands Available -

• `{i}ftyping <time/in secs>`
    `Show Fake Typing in current chat.`

• `{i}faudio <time/in secs>`
    `Show Fake Recording Action in current chat.`

• `{i}fvideo <time/in secs>`
    `Show Fake video action in current chat.`

• `{i}fgame <time/in secs>`
    `Show Fake Game Playing Action in current chat.`

• `{i}flocation <time/in secs>`
    `Show Fake location Action in current chat.`

• `{i}fcontact <time/in secs>`
    `Show Fake contact choosing Action in current chat.`

• `{i}fround <time/in secs>`
    `Show Fake video message action in current chat.`

• `{i}fphoto <time/in secs>`
    `Show Fake sending photo in current chat.`

• `{i}fdocument <time/in secs>`
    `Show Fake sending document in current chat.`
"""
import math
import time

from pyHugo.functions.admins import ban_time

from . import asyncio, eor, get_string, hugo_cmd


@hugo_cmd(
    pattern="f(typing|audio|contact|document|game|location|photo|round|video) ?(.*)"
)
async def _(e):
    act = e.pattern_match.group(1)
    t = e.pattern_match.group(2)
    if act in ["audio", "round", "video"]:
        act = "record-" + act
    if t.isdigit():
        t = int(t)
    elif t.endswith(("s", "h", "d", "m")):
        t = math.ceil((await ban_time(e, t)) - time.time())
    else:
        t = 60
    await eor(e, get_string("fka_1").format(str(t)), time=5)
    async with e.client.action(e.chat_id, act):
        await asyncio.sleep(t)
