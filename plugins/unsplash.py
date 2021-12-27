# Hugo - UserBot
# Copyright (C) TeamHugoX
#
# This file is a part of < https://github.com/TeamHugoX/Hugo/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamHugoX/Hugo/blob/main/LICENSE/>.
"""
**༄** Commands Available -

• {i}unsplash <search query> ; <no of pics>
    Unsplash Image Search.
"""

from pyHugo.functions.misc import unsplashsearch

from . import download_file, eor, get_string, os, hugo_cmd


@hugo_cmd(pattern="unsplash ?(.*)")
async def searchunsl(hg):
    match = hg.pattern_match.group(1)
    if not match:
        return await eor(hg, "Give me Something to Search")
    if ";" in match:
        num = int(match.split(";")[1])
        query = match.split(";")[0]
    else:
        num = 5
        query = match
    tep = await eor(hg, get_string("com_1"))
    res = await unsplashsearch(query, limit=num)
    if not res:
        return await eor(hg, get_string("unspl_1"), time=5)
    dir = "resources/downloads/"
    CL, nl = [], 0
    for rp in res:
        Hp = await download_file(rp, f"{dir}img-{nl}.png")
        CL.append(Hp)
        nl += 1
    await hg.client.send_file(hg.chat_id, CL, caption=f"Uploaded {len(res)} Images!")
    await tep.delete()
    [os.remove(img) for img in CL]
