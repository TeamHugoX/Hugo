# Hugo - UserBot
# Copyright (C) TeamHugoX
#
# This file is a part of < https://github.com/TeamHugoX/Hugo/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamHugoX/Hugo/blob/main/LICENSE/>.

from pyHugo import *
from pyHugo.functions.helper import *
from pyHugo.misc import owner_and_sudos
from pyHugo.misc._assistant import asst_cmd, callback, in_pattern
from telethon import Button, custom

from plugins import ATRA_COL
from strings import get_languages, get_string, language

OWNER_NAME = hugo_bot.me.first_name
OWNER_ID = hugo_bot.me.id

AST_PLUGINS = {}


async def setit(event, name, value):
    try:
        udB.set(name, value)
    except BaseException:
        return await event.edit("`Something Went Wrong`")


def get_back_button(name):
    return [Button.inline("« ʙᴀᴄᴋ", data=f"{name}")]
