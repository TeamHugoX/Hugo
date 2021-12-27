# Hugo - UserBot
# Copyright (C) TeamHugoX
#
# This file is a part of < https://github.com/TeamHugoX/Hugo/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamHugoX/Hugo/blob/main/LICENSE/>.
"""
**༄** Commands Available -

• `{i}lock <msgs/media/sticker/gif/games/inline/polls/invites/pin/changeinfo>`
    Lock the Used Setting in Used Group.

• `{i}unlock <msgs/media/sticker/gif/games/inline/polls/invites/pin/changeinfo>`
    UNLOCK the Used Setting in Used Group.

"""
from pyHugo.functions.admins import lock_unlock
from telethon.tl.functions.messages import EditChatDefaultBannedRightsRequest

from . import eor, hugo_cmd


@hugo_cmd(
    pattern="lock ?(.*)",
    groups_only=True,
    admins_only=True,
    type=["official", "manager"],
)
async def lockho(e):
    mat = e.pattern_match.group(1)
    if not mat:
        return await eor(e, "`Give some Proper Input..`", time=5)
    ml = lock_unlock(mat)
    if not ml:
        return await eor(e, "`Incorrect Input`", time=5)
    await e.client(EditChatDefaultBannedRightsRequest(e.chat_id, ml))
    await eor(e, f"Locked - `{mat}` ! ")


@hugo_cmd(
    pattern="unlock ?(.*)",
    groups_only=True,
    admins_only=True,
    type=["official", "manager"],
)
async def unlckho(e):
    mat = e.pattern_match.group(1)
    if not mat:
        return await eor(e, "`Give some Proper Input..`", time=5)
    ml = lock_unlock(mat, lock=False)
    if not ml:
        return await eor(e, "`Incorrect Input`", time=5)
    await e.client(EditChatDefaultBannedRightsRequest(e.chat_id, ml))
    await eor(e, f"Unlocked - `{mat}` ! ")
