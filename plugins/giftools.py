# Hugo - UserBot
# Copyright (C) TeamHugoX
#
# This file is a part of < https://github.com/TeamHugoX/Hugo/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamHugoX/Hugo/blob/main/LICENSE/>.
"""
**༄** Commands Available

•`{i}invertgif`
  Make Gif Inverted(negative).

•`{i}bwgif`
  Make Gif black and white

•`{i}vtog`
  Reply To Video , It will Create Gif
  Video to Gif

•`{i}gif <query>`
   Send video regarding to query.
"""
import os
import random
import time
from datetime import datetime as dt

from . import HNDLR, LOGS, bash, downloader, eor, get_string, mediainfo, hugo_cmd


@hugo_cmd(pattern="bwgif$")
async def igif(e):
    a = await e.get_reply_message()
    if not (a and a.media):
        return await eor(e, "`Reply To gif only`", time=5)
    wut = mediainfo(a.media)
    if "gif" not in wut:
        return await eor(e, "`Reply To Gif Only`", time=5)
    xx = await eor(e, get_string("com_1"))
    z = await a.download_media()
    try:
        await bash(f'ffmpeg -i "{z}" -vf format=gray hg.gif -y')
        await e.client.send_file(e.chat_id, "ult.gif", support_stream=True)
        os.remove(z)
        os.remove("ult.gif")
        await xx.delete()
    except Exception as er:
        LOGS.info(er)


@hugo_cmd(pattern="invertgif$")
async def igif(e):
    a = await e.get_reply_message()
    if not (a and a.media):
        return await eor(e, "`Reply To gif only`", time=5)
    wut = mediainfo(a.media)
    if "gif" not in wut:
        return await eor(e, "`Reply To Gif Only`", time=5)
    xx = await eor(e, get_string("com_1"))
    z = await a.download_media()
    try:
        await bash(
            f'ffmpeg -i "{z}" -vf lutyuv="y=negval:u=negval:v=negval" hg.gif -y'
        )
        await e.client.send_file(e.chat_id, "ult.gif", support_stream=True)
        os.remove(z)
        os.remove("ult.gif")
        await xx.delete()
    except Exception as er:
        LOGS.info(er)


@hugo_cmd(pattern="gif ?(.*)")
async def gifs(hg):
    get = hg.pattern_match.group(1)
    xx = random.randint(0, 5)
    n = 0
    if ";" in get:
        try:
            n = int(get.split(";")[-1])
        except IndexError:
            pass
    if not get:
        return await eor(hg, f"`{HNDLR}gif <query>`")
    m = await eor(hg, get_string("com_2"))
    gifs = await hg.client.inline_query("gif", get)
    if not n:
        await gifs[xx].click(
            hg.chat_id, reply_to=hg.reply_to_msg_id, silent=True, hide_via=True
        )
    else:
        for x in range(n):
            await gifs[x].click(
                hg.chat_id, reply_to=hg.reply_to_msg_id, silent=True, hide_via=True
            )
    await m.delete()


@hugo_cmd(pattern="vtog$")
async def vtogif(e):
    a = await e.get_reply_message()
    if not (a and a.media):
        return await eor(e, "`Reply To video only`", time=5)
    wut = mediainfo(a.media)
    if "video" not in wut:
        return await eor(e, "`Reply To Video Only`", time=5)
    xx = await eor(e, get_string("com_1"))
    dur = a.media.document.attributes[0].duration
    tt = time.time()
    if int(dur) < 120:
        z = await a.download_media()
        await bash(
            f'ffmpeg -i {z} -vf "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 hg.gif -y'
        )
    else:
        filename = a.file.name
        if not filename:
            filename = "video_" + dt.now().isoformat("_", "seconds") + ".mp4"
        vid = await downloader(filename, a.media.document, xx, tt, get_string("com_5"))
        z = vid.name
        await bash(
            f'ffmpeg -ss 3 -t 100 -i {z} -vf "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 hg.gif'
        )

    await e.client.send_file(e.chat_id, "ult.gif", support_stream=True)
    os.remove(z)
    os.remove("ult.gif")
    await xx.delete()
