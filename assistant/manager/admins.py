# Hugo - UserBot
# Copyright (C) TeamHugoX
#
# This file is a part of < https://github.com/TeamHugoX/Hugo/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamHugoX/Hugo/blob/main/LICENSE/>.

from . import *


@hugo_cmd(pattern="dkick", type=["manager", "official"])
async def dowj(e):
    replied = await e.get_reply_message()
    if replied:
        user = replied.sender_id
    else:
        return await eor(e, "Reply to a message...")
    try:
        await replied.delete()
        await e.client.kick_participant(e.chat_id, user)
        await eor(e, "Kicked Successfully!")
    except Exception as E:
        await eor(e, str(E))


@hugo_cmd(pattern="dban", type=["manager", "official"])
async def dowj(e):
    replied = await e.get_reply_message()
    if replied:
        user = replied.sender_id
    else:
        return await eor(e, "Reply to a message...")
    try:
        await replied.delete()
        await e.client.edit_permissions(e.chat_id, user, view_messages=False)
        await eor(e, "Banned Successfully!")
    except Exception as E:
        await eor(e, str(E))
