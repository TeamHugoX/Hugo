# Hugo - UserBot
# Copyright (C) TeamHugoX
#
# This file is a part of < https://github.com/TeamHugoX/Hugo/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamHugoX/Hugo/blob/main/LICENSE/>.

import re

from . import Button, callback, get_back_button, get_languages, language, udB


@callback("lang", owner=True)
async def setlang(event):
    languages = get_languages()
    thgd = [
        Button.inline(
            f"{languages[hg]['natively']} [{hg.lower()}]",
            data=f"set_{hg}",
        )
        for hg in languages
    ]
    buttons = list(zip(thgd[::2], thgd[1::2]))
    if len(thgd) % 2 == 1:
        buttons.append((thgd[-1],))
    buttons.append([Button.inline("« ʙᴀᴄᴋ", data="mainmenu")])
    await event.edit("List Of Available Languages.", buttons=buttons)


@callback(re.compile(b"set_(.*)"), owner=True)
async def settt(event):
    lang = event.data_match.group(1).decode("UTF-8")
    languages = get_languages()
    language[0] = lang
    udB.delete("language") if lang == "en" else udB.set("language", lang)
    await event.edit(
        f"Your language has been set to {languages[lang]['natively']} ({lang}).",
        buttons=get_back_button("lang"),
    )
