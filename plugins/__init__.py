# Hugo - UserBot
# Copyright (C) TeamHugoX
#
# This file is a part of < https://github.com/TeamHugoX/Hugo/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamHugoX/Hugo/blob/main/LICENSE/>.

import asyncio
import os
import time
from random import choice

from pyHugo import *
from pyHugo.dB import HUGO_IMAGES
from pyHugo.functions.helper import *
from pyHugo.functions.info import *
from pyHugo.functions.misc import *
from pyHugo.functions.tools import *
from pyHugo.misc._assistant import asst_cmd, callback, in_pattern
from pyHugo.misc._decorators import hugo_cmd
from pyHugo.misc._wrappers import eod, eor
from pyHugo.version import __version__, hugo_version
from telethon import Button, events
from telethon.tl import functions, types

from strings import get_string

Redis = udB.get
client = bot = hugo_bot

OWNER_NAME = hugo_bot.me.first_name
OWNER_ID = hugo_bot.me.id
LOG_CHANNEL = int(udB.get("LOG_CHANNEL"))
INLINE_PIC = udB.get("INLINE_PIC") or choice(HUGO_IMAGES)
if INLINE_PIC == "False":
    INLINE_PIC = None
Telegraph = telegraph_client()

List = []
Dict = {}
N = 0

STUFF = {}

# Chats, which needs to be ignore for some cases
# Considerably, there can be many
# Feel Free to Add Any other...

NOSPAM_CHAT = [
    -1001327032795,  # HugoSupport
    -1001387666944,  # PyrogramChat
    -1001109500936,  # TelethonChat
    -1001050982793,  # Python
    -1001256902287,  # DurovsChat
]

KANGING_STR = [
    "Using Witchery to kang this sticker...",
    "Plagiarising hehe...",
    "Inviting this sticker over to my pack...",
    "Kanging this sticker...",
    "Hey that's a nice sticker!\nMind if I kang?!..",
    "Hehe me stel ur stiker...",
    "Ay look over there (☉｡☉)!→\nWhile I kang this...",
    "Roses are red violets are blue, kanging this sticker so my pack looks cool",
    "Imprisoning this sticker...",
    "Mr.Steal-Your-Sticker is stealing this sticker... ",
]

ATRA_COL = [
    "DarkCyan",
    "DeepSkyBlue",
    "DarkTurquoise",
    "Cyan",
    "LightSkyBlue",
    "Turquoise",
    "MediumVioletRed",
    "Aquamarine",
    "Lightcyan",
    "Azure",
    "Moccasin",
    "PowderBlue",
]
