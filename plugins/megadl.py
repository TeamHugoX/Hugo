# Hugo - UserBot
# Copyright (C) TeamHugoX
#
# This file is a part of < https://github.com/TeamHugoX/Hugo/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamHugoX/Hugo/blob/main/LICENSE/>.
"""
**༄** Commands Available -

•`{i}megadl <link>`
  It Downloads and Upload Files from mega.nz links.
"""
import time
from datetime import datetime

from . import (
    HNDLR,
    LOGS,
    bash,
    eor,
    get_all_files,
    get_string,
    humanbytes,
    os,
    time_formatter,
    hugo_cmd,
    uploader,
)


@hugo_cmd(pattern="megadl ?(.*)")
async def _(e):
    link = e.pattern_match.group(1)
    if os.path.isdir("mega"):
        await bash("rm -rf mega")
    os.mkdir("mega")
    xx = await eor(e, f"{get_string('com_1')}\nTo Check Progress : `{HNDLR}ls mega`")
    s = datetime.now()
    x, y = await bash(f"megadl {link} --path mega")
    ok = get_all_files("mega")
    tt = time.time()
    c = 0
    for kk in ok:
        try:
            res = await uploader(kk, kk, tt, xx, get_string("com_6"))
            await e.client.send_file(
                e.chat_id,
                res,
                caption="`" + kk.split("/")[-1] + "`",
                force_document=True,
                thumb="resources/extras/hugo.png",
            )
            c += 1
        except Exception as er:
            LOGS.info(er)
    ee = datetime.now()
    t = time_formatter(((ee - s).seconds) * 1000)
    size = 0
    for path, dirs, files in os.walk("mega"):
        for f in files:
            fp = os.path.join(path, f)
            size += os.path.getsize(fp)
    await xx.delete()
    await e.client.send_message(
        e.chat_id,
        f"Downloaded And Uploaded Total - `{c}` files of `{humanbytes(size)}` in `{t}`",
    )
    await bash("rm -rf mega")
