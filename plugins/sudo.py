# Hugo - UserBot
# Copyright (C) TeamHugoX
#
# This file is a part of < https://github.com/TeamHugoX/Hugo/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamHugoX/Hugo/blob/main/LICENSE/>.
"""
**༄** Commands Available -

• `{i}addsudo`
    Add Sudo Users by replying to user or using <space> separated userid(s)

• `{i}delsudo`
    Remove Sudo Users by replying to user or using <space> separated userid(s)

• `{i}listsudo`
    List all sudo users.
"""
from pyHugo.dB.sudos import add_sudo, del_sudo, is_sudo

from . import Redis, eor, get_string, get_display_name, get_user_id, udB, hugo_bot, hugo_cmd


@hugo_cmd(pattern="addsudo ?(.*)", fullsudo=True)
async def _(hg):
    inputs = hg.pattern_match.group(1)
    if hg.reply_to_msg_id:
        replied_to = await hg.get_reply_message()
        sender = await replied_to.get_sender()
        id = replied_to.sender_id
        name = get_display_name(sender)
    elif inputs:
        id = await get_user_id(inputs)
        try:
            name = (await hg.client.get_entity(int(id))).first_name
        except BaseException:
            name = ""
    elif hg.is_private:
        id = hg.chat_id
        name = get_display_name(ult.chat)
    else:
        return await eor(hg, get_string("sudo_1"), time=5)

    if id == hugo_bot.me.id:
        mmm = get_string("sudo_2")
    elif is_sudo(id):
        if name != "":
            mmm = f"[{name}](tg://user?id={id}) `is already a SUDO User ...`"
        else:
            mmm = f"`{id} is already a SUDO User...`"
    elif add_sudo(id):
        udB.set("SUDO", "True")
        if name != "":
            mmm = f"**Added [{name}](tg://user?id={id}) as SUDO User**"
        else:
            mmm = f"**Added **`{id}`** as SUDO User**"
    else:
        mmm = "`SEEMS LIKE THIS FUNCTION CHOOSE TO BREAK ITSELF`"
    await eor(hg, mmm, time=5)


@hugo_cmd(pattern="delsudo ?(.*)", fullsudo=True)
async def _(hg):
    inputs = hg.pattern_match.group(1)
    if hg.reply_to_msg_id:
        replied_to = await hg.get_reply_message()
        id = replied_to.sender_id
        name = get_display_name(replied_to.sender)
    elif inputs:
        id = await get_user_id(inputs)
        try:
            name = (await hg.client.get_entity(int(id))).first_name
        except BaseException:
            name = ""
    elif hg.is_private:
        id = hg.chat_id
        name = get_display_name(ult.chat)
    else:
        return await eor(hg, get_string("sudo_1"), time=5)
    if not is_sudo(id):
        if name != "":
            mmm = f"[{name}](tg://user?id={id}) `wasn't a SUDO User ...`"
        else:
            mmm = f"`{id} wasn't a SUDO User...`"
    elif del_sudo(id):
        if name != "":
            mmm = f"**Removed [{name}](tg://user?id={id}) from SUDO User(s)**"
        else:
            mmm = f"**Removed **`{id}`** from SUDO User(s)**"
    else:
        mmm = "`SEEMS LIKE THIS FUNCTION CHOOSE TO BREAK ITSELF`"
    await eor(hg, mmm, time=5)


@hugo_cmd(
    pattern="listsudo$",
)
async def _(hg):
    sudos = Redis("SUDOS")
    if sudos == "" or sudos is None:
        return await eor(hg, get_string("sudo_3"), time=5)
    sumos = sudos.split(" ")
    msg = ""
    for i in sumos:
        try:
            name = (await hg.client.get_entity(int(i))).first_name
        except BaseException:
            name = ""
        if name != "":
            msg += f"• [{name}](tg://user?id={i}) ( `{i}` )\n"
        else:
            msg += f"• `{i}` -> Invalid User\n"
    m = udB.get("SUDO") or "False"
    if m == "False":
        m = "[False](https://telegra.ph/Hugo-04-06)"
    return await eor(
        hg, f"**SUDO MODE : {m}\n\nList of SUDO Users :**\n{msg}", link_preview=False
    )
