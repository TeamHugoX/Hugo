# Hugo - UserBot
# Copyright (C) TeamHugoX
#
# This file is a part of < https://github.com/TeamHugoX/Hugo/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamHugoX/Hugo/blob/main/LICENSE/>.

import asyncio

from pyHugo.dB import stickers
from pyHugo.dB.chatBot_db import chatbot_stats
from pyHugo.dB.clean_db import is_clean_added
from pyHugo.dB.forcesub_db import get_forcesetting
from pyHugo.dB.gban_mute_db import is_gbanned
from pyHugo.dB.greetings_db import get_goodbye, get_welcome, must_thank
from pyHugo.dB.username_db import get_username, update_username
from pyHugo.functions.helper import inline_mention
from pyHugo.functions.tools import create_tl_btn, get_chatbot_reply
from telethon import events
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.utils import get_display_name

from . import LOG_CHANNEL, LOGS, asst, get_string, types, udB, hugo_bot
from ._inline import something


@hugo_bot.on(events.ChatAction())
async def ChatActionsHandler(hg):  # sourcery no-metrics
    # clean chat actions
    if is_clean_added(hg.chat_id):
        try:
            await hg.delete()
        except BaseException:
            pass

    # thank members
    if must_thank(hg.chat_id):
        chat_count = (await hg.client.get_participants(hg.chat_id, limit=0)).total
        if chat_count % 100 == 0:
            stik_id = chat_count / 100 - 1
            sticker = stickers[stik_id]
            await hg.respond(file=sticker)
    # force subscribe
    if (
        udB.get("FORCESUB")
        and ((ult.user_joined or hg.user_added))
        and get_forcesetting(hg.chat_id)
    ):
        user = await hg.get_user()
        if not user.bot:
            joinchat = get_forcesetting(hg.chat_id)
            try:
                await hugo_bot(GetParticipantRequest(int(joinchat), user.id))
            except UserNotParticipantError:
                await hugo_bot.edit_permissions(
                    hg.chat_id, user.id, send_messages=False
                )
                res = await hugo_bot.inline_query(
                    asst.me.username, f"fsub {user.id}_{joinchat}"
                )
                await res[0].click(hg.chat_id, reply_to=hg.action_message.id)

    # gban checks
    if hg.user_joined or hg.added_by:
        user = await hg.get_user()
        chat = await hg.get_chat()
        reason = is_gbanned(user.id)
        if reason and chat.admin_rights:
            try:
                await hg.client.edit_permissions(
                    chat.id,
                    user.id,
                    view_messages=False,
                )
                gban_watch = get_string("can_1").format(inline_mention(user), reason)
                await hg.reply(gban_watch)
            except Exception as er:
                LOGS.exception(er)

        # greetings
        elif get_welcome(hg.chat_id):
            user = await hg.get_user()
            chat = await hg.get_chat()
            title = chat.title or "this chat"
            count = (await hg.client.get_participants(chat, limit=0)).total
            mention = inline_mention(user)
            name = user.first_name
            fullname = get_display_name(user)
            uu = user.username
            username = f"@{uu}" if uu else mention
            wel = get_welcome(hg.chat_id)
            msgg = wel["welcome"]
            med = wel["media"] or None
            userid = user.id
            msg = None
            if msgg:
                msg = msgg.format(
                    mention=mention,
                    group=title,
                    count=count,
                    name=name,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                )
            if wel.get("button"):
                btn = create_tl_btn(wel["button"])
                await something(hg, msg, med, btn)
            elif msg:
                send = await hg.reply(
                    msg,
                    file=med,
                )
                await asyncio.sleep(150)
                await send.delete()
            else:
                await hg.reply(file=med)
    elif (hg.user_left or hg.user_kicked) and get_goodbye(hg.chat_id):
        user = await hg.get_user()
        chat = await hg.get_chat()
        title = chat.title or "this chat"
        count = (await hg.client.get_participants(chat, limit=0)).total
        mention = inline_mention(user)
        name = user.first_name
        fullname = get_display_name(user)
        uu = user.username
        username = f"@{uu}" if uu else mention
        wel = get_goodbye(hg.chat_id)
        msgg = wel["goodbye"]
        med = wel["media"]
        userid = user.id
        msg = None
        if msgg:
            msg = msgg.format(
                mention=mention,
                group=title,
                count=count,
                name=name,
                fullname=fullname,
                username=username,
                userid=userid,
            )
        if wel.get("button"):
            btn = create_tl_btn(wel["button"])
            await something(hg, msg, med, btn)
        elif msg:
            send = await hg.reply(
                msg,
                file=med,
            )
            await asyncio.sleep(150)
            await send.delete()
        else:
            await hg.reply(file=med)


@hugo_bot.on(events.NewMessage(incoming=True))
async def chatBot_replies(e):
    sender = await e.get_sender()
    if not isinstance(sender, types.User):
        return
    if e.text and chatbot_stats(e.chat_id, e.sender_id):
        msg = await get_chatbot_reply(e.message.message)
        if msg:
            await e.reply(msg)
    chat = await e.get_chat()
    if e.is_group and not sender.bot:
        if sender.username:
            await uname_stuff(e.sender_id, sender.username, sender.first_name)
    elif e.is_private and not sender.bot:
        if chat.username:
            await uname_stuff(e.sender_id, chat.username, chat.first_name)


@hugo_bot.on(events.Raw(types.UpdateUserName))
async def uname_change(e):
    await uname_stuff(e.user_id, e.username, e.first_name)


async def uname_stuff(id, uname, name):
    if udB.get("USERNAME_LOG") == "True":
        old = get_username(id)
        # Ignore Name Logs
        if old and old == uname:
            return
        if old and uname:
            await asst.send_message(
                LOG_CHANNEL,
                get_string("can_2").format(old, uname),
            )
        elif old:
            await asst.send_message(
                LOG_CHANNEL,
                get_string("can_3").format(f"[{name}](tg://user?id={id})", old),
            )
        elif uname:
            await asst.send_message(
                LOG_CHANNEL,
                get_string("can_4").format(f"[{name}](tg://user?id={id})", uname),
            )
        update_username(id, uname)
