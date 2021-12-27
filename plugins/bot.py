# Hugo - UserBot
# Copyright (C) TeamHugoX
#
# This file is a part of < https://github.com/TeamHugoX/Hugo/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamHugoX/Hugo/blob/main/LICENSE/>.
"""
**༄** Commands Available

• `{i}alive` | `{i}ialive`
    Check if your bot is working.

• `{i}ping`
    Check Hugo's response time.

• `{i}cmds`
    View all plugin names.

• `{i}restart`
    To restart your bot.

• `{i}logs (sys)`
    Get the full terminal logs.

• `{i}logs carbon`
    Get the carbonized sys logs.

• `{i}logs heroku`
   Get the latest 100 lines of heroku logs.

• `{i}shutdown`
    Turn off your bot.
"""
import os
import sys
import time
from platform import python_version as pyver
from random import choice

from git import Repo
from pyHugo.version import __version__ as HugoVer
from telethon import __version__
from telethon.errors.rpcerrorlist import ChatSendMediaForbiddenError
from telethon.utils import resolve_bot_file_id

try:
    from carbonnow import Carbon
except ImportError:
    Carbon = None

from . import (
    ATRA_COL,
    LOGS,
    OWNER_NAME,
    Button,
    Telegraph,
    Var,
    allcmds,
    asst,
    bash,
    call_back,
    callback,
    def_logs,
    eor,
    get_string,
    heroku_logs,
    in_pattern,
    restart,
    shutdown,
    start_time,
    time_formatter,
    udB,
    hugo_cmd,
    hugo_version,
)

# Will move to strings
alive_txt = """
The Hugo Userbot

  ◍ Version - {}
  ◍ Py-Hugo - {}
  ◍ Telethon - {}
"""


@callback("alive")
async def alive(event):
    text = alive_txt.format(hugo_version, HugoVer, __version__)
    await event.answer(text, alert=True)


@hugo_cmd(
    pattern="alive$",
)
async def lol(hg):
    pic = udB.get("ALIVE_PIC")
    uptime = time_formatter((time.time() - start_time) * 1000)
    header = udB.get("ALIVE_TEXT") or get_string("bot_1")
    y = Repo().active_branch
    xx = Repo().remotes[0].config_reader.get("url")
    rep = xx.replace(".git", f"/tree/{y}")
    kk = f" `[{y}]({rep})` "
    als = (get_string("alive_1")).format(
        header,
        OWNER_NAME,
        hugo_version,
        HugoVer,
        uptime,
        pyver(),
        __version__,
        kk,
    )
    if pic is None:
        await eor(hg, als)
    elif "telegra" in pic:
        try:
            await hg.reply(als, file=pic, link_preview=False)
            await hg.delete()
        except ChatSendMediaForbiddenError:
            await eor(hg, als, link_preview=False)
    else:
        try:
            await hg.reply(file=pic)
            await hg.reply(als, link_preview=False)
            await hg.delete()
        except ChatSendMediaForbiddenError:
            await eor(hg, als, link_preview=False)


@hugo_cmd(
    pattern="ialive$",
)
async def is_on(hg):
    if not hg.client._bot:
        await hg.delete()
        try:
            res = await hg.client.inline_query(asst.me.username, "alive")
            await res[0].click(hg.chat_id)
        except Exception as er:
            LOGS.info(er)
        return
    pic = udB.get("ALIVE_PIC")
    uptime = time_formatter((time.time() - start_time) * 1000)
    header = udB.get("ALIVE_TEXT") or get_string("bot_1")
    y = Repo().active_branch
    xx = Repo().remotes[0].config_reader.get("url")
    rep = xx.replace(".git", f"/tree/{y}")
    kk = f" `[{y}]({rep})` "
    als = (get_string("alive_1")).format(
        header,
        OWNER_NAME,
        hugo_version,
        HugoVer,
        uptime,
        pyver(),
        __version__,
        kk,
    )
    buttons = [
        [Button.inline(get_string("bot_2"), "alive")],
        [
            Button.url(get_string("bot_3"), "https://github.com/TeamHugoX/Hugo"),
            Button.url(get_string("bot_4"), "t.me/HugoSupport"),
        ],
    ]
    await hg.client.send_message(
        hg.chat_id, als, file=pic, buttons=buttons, link_preview=False
    )


@hugo_cmd(pattern="ping$", chats=[], type=["official", "assistant"])
async def _(event):
    if event.out:
        await event.delete()
    start = time.time()
    x = await event.respond("Pong !")
    end = round((time.time() - start) * 1000)
    uptime = time_formatter((time.time() - start_time) * 1000)
    await x.edit(get_string("ping").format(end, uptime))


@hugo_cmd(
    pattern="cmds$",
)
async def cmds(event):
    await allcmds(event, Telegraph)


heroku_api = Var.HEROKU_API


@hugo_cmd(
    pattern="restart$",
    fullsudo=True,
)
async def restartbt(hg):
    ok = await eor(hg, get_string("bot_5"))
    call_back()
    if heroku_api:
        return await restart(ok)
    await bash("git pull && pip3 install -r requirements.txt")
    os.execl(sys.executable, sys.executable, "-m", "pyHugo")


@hugo_cmd(
    pattern="shutdown$",
    fullsudo=True,
)
async def shutdownbot(hg):
    await shutdown(hg)


@hugo_cmd(
    pattern="logs ?(.*)",
    chats=[],
)
async def _(event):
    opt = event.pattern_match.group(1)
    if opt == "heroku":
        await heroku_logs(event)
    elif opt == "carbon" and Carbon:
        event = await eor(event, get_string("com_1"))
        code = open("hugo.log", "r").read()[-2500:]
        file = await Carbon(
            base_url="https://carbonara.vercel.app/api/cook",
            code=code,
            background=choice(ATRA_COL),
        ).memorize("hugo-logs")
        await event.reply("**Hugo Logs.**", file=file)
    else:
        await def_logs(event)
    await event.delete()


@in_pattern("alive", owner=True)
async def inline_alive(hg):
    pic = udB.get("ALIVE_PIC")
    uptime = time_formatter((time.time() - start_time) * 1000)
    header = udB.get("ALIVE_TEXT") or get_string("bot_1")
    y = Repo().active_branch
    xx = Repo().remotes[0].config_reader.get("url")
    rep = xx.replace(".git", f"/tree/{y}")
    kk = f" `[{y}]({rep})` "
    als = (get_string("alive_1")).format(
        header,
        OWNER_NAME,
        hugo_version,
        HugoVer,
        uptime,
        pyver(),
        __version__,
        kk,
    )
    buttons = [
        [
            Button.url(get_string("bot_3"), "https://github.com/TeamHugoX/Hugo"),
            Button.url(get_string("bot_4"), "t.me/HugoSupport"),
        ]
    ]
    builder = hg.builder
    if pic:
        try:
            if ".jpg" in pic:
                results = [await builder.photo(pic, text=als, buttons=buttons)]
            else:
                _pic = resolve_bot_file_id(pic)
                if _pic:
                    pic = _pic
                    buttons.insert(
                        0, [Button.inline(get_string("bot_2"), data="alive")]
                    )
                results = [
                    await builder.document(
                        pic,
                        title="Inline Alive",
                        description="@TheHugo",
                        buttons=buttons,
                    )
                ]
            return await hg.answer(results)
        except BaseException as er:
            LOGS.info(er)
    result = [
        await builder.article("Alive", text=als, link_preview=False, buttons=buttons)
    ]
    await hg.answer(result)
