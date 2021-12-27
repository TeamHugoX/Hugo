# Hugo - UserBot
# Copyright (C) TeamHugoX
#
# This file is a part of < https://github.com/TeamHugoX/Hugo/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamHugoX/Hugo/blob/main/LICENSE/>.
"""
**༄** Commands Available -

• `{i}fsub <chat username><id>`
    Enable ForceSub in Used Chat !

• `{i}checkfsub`
    Check/Get Active ForceSub Setting of Used Chat.

• `{i}remfsub`
    Remove ForceSub from Used Chat !

    Note - You Need to be Admin in Both Channel/Chats
        in order to Use ForceSubscribe.
"""

import re

from pyHugo.dB.forcesub_db import add_forcesub, get_forcesetting, rem_forcesub
from telethon.errors.rpcerrorlist import ChatAdminRequiredError, UserNotParticipantError
from telethon.tl.custom import Button
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.functions.messages import ExportChatInviteRequest

from . import (
    LOGS,
    asst,
    callback,
    eor,
    events,
    get_string,
    in_pattern,
    udB,
    hugo_bot,
    hugo_cmd,
)

CACHE = {}


@hugo_cmd(pattern="fsub ?(.*)", admins_only=True, groups_only=True)
async def addfor(e):
    match = e.pattern_match.group(1)
    if not match:
        return await eor(e, get_string("fsub_1"), time=5)
    if match.startswith("@"):
        ch = match
    else:
        try:
            ch = int(match)
        except BaseException:
            return await eor(e, get_string("fsub_2"), time=5)
    try:
        match = (await e.client.get_entity(ch)).id
    except BaseException:
        return await eor(e, get_string("fsub_2"), time=5)
    if not str(match).startswith("-100"):
        match = int("-100" + str(match))
    add_forcesub(e.chat_id, match)
    await eor(e, "Added ForceSub in This Chat !")


@hugo_cmd(pattern="remfsub$")
async def remor(e):
    res = rem_forcesub(e.chat_id)
    if not res:
        return await eor(e, get_string("fsub_3"), time=5)
    await eor(e, "Removed ForceSub...")


@hugo_cmd(pattern="checkfsub$")
async def getfsr(e):
    res = get_forcesetting(e.chat_id)
    if not res:
        return await eor(e, "ForceSub is Not Active In This Chat !", time=5)
    cha = await e.client.get_entity(int(res))
    await eor(e, f"**ForceSub Status** : `Active`\n- **{cha.title}** `({res})`")


@in_pattern("fsub ?(.*)", owner=True)
async def fcall(e):
    match = e.pattern_match.group(1)
    spli = match.split("_")
    user = await hugo_bot.get_entity(int(spli[0]))
    cl = await hugo_bot.get_entity(int(spli[1]))
    text = f"Hi [{user.first_name}](tg://user?id={user.id}), You Need to Join"
    text += f" {cl.title} in order to Chat in this Group."
    if not cl.username:
        el = (await hugo_bot(ExportChatInviteRequest(cl))).link
    else:
        el = "https://t.me/" + cl.username
    res = [
        await e.builder.article(
            title="forcesub",
            text=text,
            buttons=[
                [Button.url(text=get_string("fsub_4"), url=el)],
                [Button.inline(get_string("fsub_5"), data=f"unm_{match}")],
            ],
        )
    ]
    await e.answer(res)


@callback(re.compile("unm_(.*)"))
async def diesoon(e):
    match = (e.data_match.group(1)).decode("UTF-8")
    spli = match.split("_")
    if e.sender_id != int(spli[0]):
        return await e.answer(get_string("fsub_7"), alert=True)
    try:
        await hugo_bot(GetParticipantRequest(int(spli[1]), int(spli[0])))
    except UserNotParticipantError:
        return await e.answer(
            "Please Join That Channel !\nThen Click This Button !", alert=True
        )
    await hugo_bot.edit_permissions(
        e.chat_id, int(spli[0]), send_messages=True, until_date=None
    )
    await e.edit(get_string("fsub_8"))


@hugo_bot.on(events.NewMessage(incoming=True))
async def cacheahs(hg):
    if not udB.get("FORCESUB"):
        return

    user = await hg.get_sender()
    joinchat = get_forcesetting(hg.chat_id)
    if not joinchat or user.bot:
        return
    if CACHE.get(hg.chat_id):
        if CACHE[hg.chat_id].get(user.id):
            CACHE[hg.chat_id].update({user.id: CACHE[hg.chat_id][user.id] + 1})
        else:
            CACHE[hg.chat_id].update({user.id: 1})
    else:
        CACHE.update({hg.chat_id: {user.id: 1}})
    count = CACHE[hg.chat_id][user.id]
    if count == 11:
        CACHE[hg.chat_id][user.id].update(1)
        return
    if count in range(2, 11):
        return
    try:
        await hugo_bot.get_permissions(int(joinchat), user.id)
        return
    except UserNotParticipantError:
        pass
    try:
        await hugo_bot.edit_permissions(hg.chat_id, user.id, send_messages=False)
    except ChatAdminRequiredError:
        return
    except Exception as e:
        LOGS.info(e)
    res = await hugo_bot.inline_query(asst.me.username, f"fsub {user.id}_{joinchat}")
    await res[0].click(hg.chat_id, reply_to=hg.id)
