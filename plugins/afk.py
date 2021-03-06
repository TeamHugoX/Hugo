# Hugo - UserBot
# Copyright (C) TeamHugoX
#
# This file is a part of < https://github.com/TeamHugoX/Hugo/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamHugoX/Hugo/blob/main/LICENSE/>.
"""
**༄** Commands Available -

• `{i}afk <optional reason>`
    AFK means away from keyboard,
    After u active this if Someone tag or msg u then It auto Reply Him/her,

    (Note : By Reply To any media U can set media afk too).

"""

import asyncio

from pyHugo.dB.afk_db import add_afk, del_afk, is_afk
from pyHugo.dB.pmpermit_db import is_approved
from telegraph import upload_file as uf
from telethon import events

from . import (
    LOG_CHANNEL,
    NOSPAM_CHAT,
    Redis,
    asst,
    eor,
    get_string,
    mediainfo,
    hugo_bot,
    hugo_cmd,
)

old_afk_msg = []


@hugo_cmd(pattern="afk ?(.*)", fullsudo=True)
async def set_afk(event):
    if event.client._bot:
        await eor(event, "Master, I am a Bot, I cant go AFK..")
    elif is_afk():
        return
    text, media, media_type = None, None, None
    if event.pattern_match.group(1):
        text = event.text.split(maxsplit=1)[1]
    reply = await event.get_reply_message()
    if reply:
        if reply.text and not text:
            text = reply.text
        if reply.media:
            media_type = mediainfo(reply.media)
            if media_type.startswith(("pic", "gif")):
                file = await event.client.download_media(reply.media)
                iurl = uf(file)
                media = f"https://telegra.ph{iurl[0]}"
            elif "sticker" or "audio" in media_type:
                media = reply.file.id
            else:
                return await eor(event, get_string("com_4"), time=5)
    await eor(event, "`Done`", time=2)
    add_afk(text, media_type, media)
    msg1, msg2 = None, None
    if text and media:
        if "sticker" in media_type:
            msg1 = await hugo_bot.send_file(event.chat_id, file=media)
            msg2 = await hugo_bot.send_message(
                event.chat_id, get_string("afk_5").format(text)
            )
        else:
            msg1 = await hugo_bot.send_message(
                event.chat_id, get_string("afk_5").format(text), file=media
            )
    elif media:
        if "sticker" in media_type:
            msg1 = await hugo_bot.send_file(event.chat_id, file=media)
            msg2 = await hugo_bot.send_message(event.chat_id, get_string("afk_6"))
        else:
            msg1 = await hugo_bot.send_message(
                event.chat_id, get_string("afk_6"), file=media
            )
    elif text:
        msg1 = await event.respond(get_string("afk_5").format(text))
    else:
        msg1 = await event.respond(get_string("afk_6"))
    old_afk_msg.append(msg1)
    if msg2:
        old_afk_msg.append(msg2)
        return await asst.send_message(LOG_CHANNEL, msg2.text)
    await asst.send_message(LOG_CHANNEL, msg1.text)


@hugo_bot.on(events.NewMessage(outgoing=True))
async def remove_afk(event):
    if (
        event.is_private
        and Redis("PMSETTING") == "True"
        and not is_approved(event.chat_id)
    ):
        return
    elif "afk" in event.text.lower():
        return
    if is_afk():
        _, _, _, afk_time = is_afk()
        del_afk()
        off = await event.reply(get_string("afk_1").format(afk_time))
        await asst.send_message(LOG_CHANNEL, get_string("afk_2").format(afk_time))
        for x in old_afk_msg:
            try:
                await x.delete()
            except BaseException:
                pass
        await asyncio.sleep(10)
        await off.delete()


@hugo_bot.on(
    events.NewMessage(incoming=True, func=lambda e: bool(e.mentioned or e.is_private)),
)
async def on_afk(event):
    if (
        event.is_private
        and Redis("PMSETTING") == "True"
        and not is_approved(event.chat_id)
    ):
        return
    elif "afk" in event.text.lower():
        return
    elif not is_afk():
        return
    if event.chat_id in NOSPAM_CHAT:
        return
    sender = await event.get_sender()
    if sender.bot or sender.verified:
        return
    text, media_type, media, afk_time = is_afk()
    msg1, msg2 = None, None
    if text and media:
        if "sticker" in media_type:
            msg1 = await event.reply(file=media)
            msg2 = await event.reply(get_string("afk_3").format(afk_time, text))
        else:
            msg1 = await event.reply(
                get_string("afk_3").format(afk_time, text), file=media
            )
    elif media:
        if "sticker" in media_type:
            msg1 = await event.reply(file=media)
            msg2 = await event.reply(get_string("afk_4").format(afk_time))
        else:
            msg1 = await event.reply(get_string("afk_4").format(afk_time), file=media)
    elif text:
        msg1 = await event.reply(get_string("afk_3").format(afk_time, text))
    else:
        msg1 = await event.reply(get_string("afk_4").format(afk_time))
    for x in old_afk_msg:
        try:
            await x.delete()
        except BaseException:
            pass
    old_afk_msg.append(msg1)
    if msg2:
        old_afk_msg.append(msg2)
