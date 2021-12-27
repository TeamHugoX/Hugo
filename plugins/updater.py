# Hugo - UserBot
# Copyright (C) TeamHugoX
#
# This file is a part of < https://github.com/TeamHugoX/Hugo/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamHugoX/Hugo/blob/main/LICENSE/>.
"""
**༄** Commands Available -

• `{i}update`
    See changelogs if any update is available.
"""

from random import choice

from git import Repo
from pyHugo.dB import HUGO_IMAGES

from . import (
    INLINE_PIC,
    Button,
    asst,
    bash,
    call_back,
    callback,
    eor,
    get_string,
    os,
    sys,
    udB,
    hugo_cmd,
    updater,
)

HGPIC = INLINE_PIC or choice(HUGO_IMAGES)


@hugo_cmd(pattern="update ?(.*)")
async def _(e):
    xx = await eor(e, get_string("upd_1"))
    m = updater()
    branch = (Repo.init()).active_branch
    if m:
        if e.pattern_match.group(1) and (
            "fast" in e.pattern_match.group(1) or "soft" in e.pattern_match.group(1)
        ):
            await bash("git pull -f && pip3 install -r requirements.txt")
            call_back()
            await xx.edit(get_string("upd_7"))
            os.execl(sys.executable, "python3", "-m", "pyHugo")
            return
        x = await asst.send_file(
            int(udB.get("LOG_CHANNEL")),
            HGPIC,
            caption="• **Update Available** •",
            force_document=False,
            buttons=Button.inline("Changelogs", data="changes"),
        )
        Link = x.message_link
        await xx.edit(
            f'<strong><a href="{Link}">[ChangeLogs]</a></strong>',
            parse_mode="html",
            link_preview=False,
        )
    else:
        await xx.edit(
            f'<code>Your BOT is </code><strong>up-to-date</strong><code> with </code><strong><a href="https://github.com/TeamHugoX/Hugo/tree/{branch}">[{branch}]</a></strong>',
            parse_mode="html",
            link_preview=False,
        )


@callback("updtavail", owner=True)
async def updava(event):
    await event.delete()
    await asst.send_file(
        int(udB.get("LOG_CHANNEL")),
        HGPIC,
        caption="• **Update Available** •",
        force_document=False,
        buttons=Button.inline("Changelogs", data="changes"),
    )
