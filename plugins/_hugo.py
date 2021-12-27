# Hugo - UserBot
# Copyright (C) TeamHugoX
#
# This file is a part of < https://github.com/TeamHugoX/Hugo/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamHugoX/Hugo/blob/main/LICENSE/>.

from telethon.errors import (
    BotMethodInvalidError,
    ChatSendInlineForbiddenError,
    ChatSendMediaForbiddenError,
)

from . import LOG_CHANNEL, LOGS, Button, asst, eor, get_string, hugo_cmd

REPOMSG = """
• **HUGO USERBOT** •\n
• Repo - [Click Here](https://github.com/TeamHugoX/Hugo)
• Addons - [Click Here](https://github.com/TeamHugoX/HugoAddons)
• Support - @HugoSupport
"""

RP_BUTTONS = [
    [
        Button.url(get_string("bot_3"), "https://github.com/TeamHugoX/Hugo"),
        Button.url("Addons", "https://github.com/TeamHugoX/HugoAddons"),
    ],
    [Button.url("Support Group", "t.me/HugoSupport")],
]

HGSTRING = """🌠 **Thanks for Deploying Hugo Userbot!**

• Here, are the Some Basic stuff from, where you can Know, about its Usage."""


@hugo_cmd(
    pattern="repo$",
    type=["official", "manager"],
)
async def repify(e):
    try:
        q = await e.client.inline_query(asst.me.username, "")
        await q[0].click(e.chat_id)
        return await e.delete()
    except (
        ChatSendInlineForbiddenError,
        ChatSendMediaForbiddenError,
        BotMethodInvalidError,
    ):
        pass
    except Exception as er:
        LOGS.info("Error while repo command : " + str(er))
    await eor(e, REPOMSG)


@hugo_cmd(pattern="hugo$")
async def useHugo(rs):
    button = Button.inline("Start >>", "initft_2")
    msg = await asst.send_message(
        LOG_CHANNEL,
        HGSTRING,
        file="https://telegra.ph/file/4482256188c61636dd43e.jpg",
        buttons=button,
    )
    await eor(rs, f"**[Click Here]({msg.message_link})**")
