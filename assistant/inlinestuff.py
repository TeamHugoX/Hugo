# Hugo - UserBot
# Copyright (C) TeamHugoX
#
# This file is a part of < https://github.com/TeamHugoX/Hugo/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamHugoX/Hugo/blob/main/LICENSE/>.

import base64
from datetime import datetime
from random import choice
from re import compile as re_compile

import requests
from bs4 import BeautifulSoup as bs
from pyHugo.functions.misc import google_search
from pyHugo.functions.tools import async_searcher, dloader, get_ofox
from telethon import Button
from telethon.tl.types import InputWebDocument as wb

from . import *

SUP_BUTTONS = [
    [
        Button.url("• ʀᴇᴘᴏ", url="https://github.com/TeamHugoX/Hugo"),
        Button.url("sᴜᴘᴘᴏʀᴛ •", url="t.me/HugoSupport"),
    ],
]

ofox = "https://telegra.ph/file/231f0049fcd722824f13b.jpg"
gugirl = "https://telegra.ph/file/0df54ae4541abca96aa11.jpg"
hugopic = "https://telegra.ph/file/8a674af5384e452fe8224.jpg"

api1 = base64.b64decode("QUl6YVN5QXlEQnNZM1dSdEI1WVBDNmFCX3c4SkF5NlpkWE5jNkZV").decode(
    "ascii"
)
api2 = base64.b64decode("QUl6YVN5QkYwenhMbFlsUE1wOXh3TVFxVktDUVJxOERnZHJMWHNn").decode(
    "ascii"
)
api3 = base64.b64decode("QUl6YVN5RGRPS253blB3VklRX2xiSDVzWUU0Rm9YakFLSVFWMERR").decode(
    "ascii"
)


@in_pattern("ofox", owner=True)
async def _(e):
    match = None
    try:
        match = e.text.split(" ", maxsplit=1)[1]
    except IndexError:
        kkkk = e.builder.article(
            title="Enter Device Codename",
            thumb=wb(ofox, 0, "image/jpeg", []),
            text="**ᴏғᴏx🦊 ʀᴇᴄᴏᴠᴇʀʏ**\n\nYou didn't search anything",
            buttons=Button.switch_inline("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", query="ofox ", same_peer=True),
        )
        return await e.answer([kkkk])
    device, releases = await get_ofox(match)
    if device.get("detail") is None:
        fox = []
        fullname = device["full_name"]
        codename = device["codename"]
        str(device["supported"])
        maintainer = device["maintainer"]["name"]
        link = f"https://orangefox.download/device/{codename}"
        for data in releases["data"]:
            release = data["type"]
            version = data["version"]
            size = humanbytes(data["size"])
            release_date = datetime.utcfromtimestamp(data["date"]).strftime("%Y-%m-%d")
            text = f"[\xad]({ofox})**ᴏʀᴀɴɢᴇ ғᴏx ʀᴇᴄᴏᴠᴇʀʏ ғᴏʀ**\n\n"
            text += f"`  ғᴜʟʟ ɴᴀᴍᴇ: {fullname}`\n"
            text += f"`  ᴄᴏᴅᴇɴᴀᴍᴇ: {codename}`\n"
            text += f"`  ᴍᴀɪɴᴛᴀɪɴᴇʀ: {maintainer}`\n"
            text += f"`  ʙᴜɪʟᴅ ᴛʏᴘᴇ: {release}`\n"
            text += f"`  ᴠᴇʀsɪᴏɴ: {version}`\n"
            text += f"`  sɪᴢᴇ: {size}`\n"
            text += f"`  ʙᴜɪʟᴅ ᴅᴀᴛᴇ: {release_date}`"
            fox.append(
                await e.builder.article(
                    title=f"{fullname}",
                    description=f"{version}\n{release_date}",
                    text=text,
                    thumb=wb(ofox, 0, "image/jpeg", []),
                    link_preview=True,
                    buttons=[
                        Button.url("ᴅᴏᴡɴʟᴏᴀᴅ", url=f"{link}"),
                        Button.switch_inline(
                            "sᴇᴀʀᴄʜ ᴀɢᴀɪɴ", query="ofox ", same_peer=True
                        ),
                    ],
                )
            )
        await e.answer(
            fox, switch_pm="OrangeFox Recovery Search.", switch_pm_param="start"
        )
    else:
        await e.answer(
            [], switch_pm="OrangeFox Recovery Search.", switch_pm_param="start"
        )


@in_pattern("fl2lnk ?(.*)", owner=True)
async def _(e):
    file_path = e.pattern_match.group(1)
    file_name = file_path.split("/")[-1]
    bitton = [
        [
            Button.inline("anonfiles", data=f"flanonfiles//{file_path}"),
            Button.inline("transfer", data=f"fltransfer//{file_path}"),
        ],
        [
            Button.inline("bayfiles", data=f"flbayfiles//{file_path}"),
            Button.inline("x0", data=f"flx0//{file_path}"),
        ],
        [
            Button.inline("file.io", data=f"flfile.io//{file_path}"),
            Button.inline("siasky", data=f"flsiasky//{file_path}"),
        ],
    ]
    try:
        lnk = e.builder.article(
            title="fl2lnk",
            text=f"**File:**\n{file_name}",
            buttons=bitton,
        )
    except BaseException:
        lnk = e.builder.article(
            title="fl2lnk",
            text="File not found",
        )
    await e.answer([lnk], switch_pm="File to Link.", switch_pm_param="start")


@callback(
    re_compile(
        "fl(.*)",
    ),
    owner=True,
)
async def _(e):
    t = (e.data).decode("UTF-8")
    data = t[2:]
    host = data.split("//")[0]
    file = data.split("//")[1]
    file_name = file.split("/")[-1]
    await e.edit(f"Uploading `{file_name}` on {host}")
    await dloader(e, host, file)


@in_pattern("repo", owner=True)
async def repo(e):
    res = [
        await e.builder.article(
            title="Hugo Userbot",
            description="Userbot | Telethon",
            thumb=wb(hugopic, 0, "image/jpeg", []),
            text="• **HUGO USERBOT** •",
            buttons=SUP_BUTTONS,
        ),
    ]
    await e.answer(res, switch_pm="Hugo Repo.", switch_pm_param="start")


@in_pattern("go", owner=True)
async def gsearch(q_event):
    try:
        match = q_event.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await q_event.answer(
            [], switch_pm="Google Search. Enter a query!", switch_pm_param="start"
        )
    searcher = []
    gresults = await google_search(match)
    for i in gresults:
        try:
            title = i["title"]
            link = i["link"]
            desc = i["description"]
            searcher.append(
                await q_event.builder.article(
                    title=title,
                    description=desc,
                    thumb=wb(gugirl, 0, "image/jpeg", []),
                    text=f"**ɢᴏᴏɢʟᴇ sᴇᴀʀᴄʜ**\n\n**••Tɪᴛʟᴇ••**\n`{title}`\n\n**••Dᴇsᴄʀɪᴘᴛɪᴏɴ••**\n`{desc}`",
                    link_preview=False,
                    buttons=[
                        [Button.url("ʟɪɴᴋ", url=f"{link}")],
                        [
                            Button.switch_inline(
                                "sᴇᴀʀᴄʜ ᴀɢᴀɪɴ",
                                query="go ",
                                same_peer=True,
                            ),
                            Button.switch_inline(
                                "sʜᴀʀᴇ",
                                query=f"go {match}",
                                same_peer=False,
                            ),
                        ],
                    ],
                ),
            )
        except IndexError:
            break
    await q_event.answer(searcher, switch_pm="Google Search.", switch_pm_param="start")


@in_pattern("mods", owner=True)
async def _(e):
    try:
        quer = e.text.split(" ", maxsplit=1)[1]
    except IndexError:
        await e.answer(
            [], switch_pm="Mod Apps Search. Enter app name!", switch_pm_param="start"
        )
    page = 1
    start = (page - 1) * 3 + 1
    da = choice([api1, api2, api3])
    url = f"https://www.googleapis.com/customsearch/v1?key={da}&cx=25b3b50edb928435b&q={quer}&start={start}"
    data = requests.get(url).json()
    search_items = data.get("items")
    search(quer)
    modss = []
    for a in search_items:
        title = a.get("title")
        desc = a.get("snippet")
        link = a.get("link")
        text = f"**• ᴛɪᴛʟᴇ •** `{title}`\n\n"
        text += f"**ᴅᴇsᴄʀɪᴘᴛɪᴏɴ** `{desc}`"
        modss.append(
            await e.builder.article(
                title=title,
                description=desc,
                text=text,
                link_preview=True,
                buttons=[
                    [Button.url("ᴅᴏᴡɴʟᴏᴀᴅ", url=f"{link}")],
                    [
                        Button.switch_inline(
                            "ᴍᴏʀᴇ ᴍᴏᴅs",
                            query="mods ",
                            same_peer=True,
                        ),
                        Button.switch_inline(
                            "sʜᴀʀᴇ",
                            query=f"mods {quer}",
                            same_peer=False,
                        ),
                    ],
                ],
            ),
        )
    await e.answer(modss, switch_pm="Search Mod Applications.", switch_pm_param="start")


@in_pattern("xda", owner=True)
async def xda_dev(event):
    QUERY = event.text.split(" ", maxsplit=1)
    try:
        query = QUERY[1]
    except IndexError:
        return await event.answer(
            [], switch_pm=get_string("instu_3"), switch_pm_param="start"
        )
    le = "https://www.xda-developers.com/search/" + query.replace(" ", "+")
    ct = await async_searcher(le, re_content=True)
    ml = bs(ct, "html.parser", from_encoding="utf-8")
    ml = ml.find_all("div", re_compile("layout_post_"), id=re_compile("post-"))
    out = []
    for on in ml:
        data = on.find_all("img", "xda_image")[0]
        title = data["alt"]
        thumb = data["src"]
        hre = on.find_all("div", "item_content")[0].find("h4").find("a")["href"]
        desc = on.find_all("div", "item_meta clearfix")[0].text
        thumb = wb(thumb, 0, "image/jpeg", [])
        text = f"[{title}]({hre})"
        out.append(
            await event.builder.article(
                title=title, description=desc, url=hre, thumb=thumb, text=text
            )
        )
    uppar = "No Results Found :(" if not out else "|| XDA Search Results ||"
    await event.answer(out, switch_pm=uppar, switch_pm_param="start")


APP_CACHE = {}


@in_pattern("app", owner=True)
async def _(e):
    try:
        f = e.text.split(" ", maxsplit=1)[1]
    except IndexError:
        swa = get_string("instu_1")
        res = []
        if APP_CACHE:
            [res.append(APP_CACHE[a][0]) for a in APP_CACHE.keys()]
            swa = get_string("instu_2")
        return await e.answer(res, switch_pm=swa, switch_pm_param="start")
    try:
        return await e.answer(
            APP_CACHE[f], switch_pm="Application Searcher.", switch_pm_param="start"
        )
    except KeyError:
        pass
    foles = []
    base_uri = "https://play.google.com"
    url = f"{base_uri}/store/search?q={f.replace(' ', '%20')}&c=apps"
    aap = await async_searcher(url, re_content=True)
    b_ = bs(aap, "html.parser", from_encoding="utf-8")
    aap = b_.find_all("div", "Vpfmgd")
    for z in aap[:10]:
        url = base_uri + z.find("a")["href"]
        scra = await async_searcher(url, re_content=True)
        bp = bs(scra, "html.parser", from_encoding="utf-8")
        name = z.find("div", "WsMG1c nnK0zc")["title"]
        desc = (
            str(bp.find("div", jsname="sngebd"))
            .replace('<div jsname="sngebd">', "")
            .replace("<br/>", "\n")
            .replace("</div>", "")[:300]
            + "..."
        )
        dev = z.find("div", "KoLSrc").text
        icon = z.find("img", "T75of QNCnCf")["data-src"]
        text = f"**• ᴀᴘᴘ ɴᴀᴍᴇ •** [{name}]({icon})\n"
        text += f"**• ᴅᴇᴠᴇʟᴏᴘᴇʀ •** `{dev}`\n"
        text += f"**• ᴅᴇsᴄʀɪᴘᴛɪᴏɴ •**\n`{desc}`"
        foles.append(
            await e.builder.article(
                title=name,
                description=dev,
                thumb=wb(icon, 0, "image/jpeg", []),
                text=text,
                link_preview=True,
                buttons=[
                    [Button.url("ʟɪɴᴋ", url=url)],
                    [
                        Button.switch_inline(
                            "ᴍᴏʀᴇ ᴀᴘᴘs",
                            query="app ",
                            same_peer=True,
                        ),
                        Button.switch_inline(
                            "sʜᴀʀᴇ",
                            query=f"app {f}",
                            same_peer=False,
                        ),
                    ],
                ],
            ),
        )
    APP_CACHE.update({f: foles})
    await e.answer(foles, switch_pm="Application Searcher.", switch_pm_param="start")


PISTON_URI = "https://emkc.org/api/v2/piston/"
PISTON_LANGS = {}


@in_pattern("run", owner=True)
async def piston_run(event):
    try:
        lang = event.text.split()[1]
        code = event.text.split(maxsplit=2)[2]
    except IndexError:
        result = await event.builder.article(
            title="Bad Query",
            description="Usage: [Language] [code]",
            text=f'**Inline Usage**\n\n`@{asst.me.username} run python print("hello world")`\n\n[Language List](https://telegra.ph/Hugo-09-01-6)',
        )
        return await event.answer([result])
    if not PISTON_LANGS:
        se = await async_searcher(PISTON_URI + "runtimes", re_json=True)
        PISTON_LANGS.update({lang.pop("language"): lang for lang in se})
    if lang in PISTON_LANGS.keys():
        version = PISTON_LANGS[lang]["version"]
    else:
        result = await event.builder.article(
            title="Unsupported Language",
            description="Usage: [Language] [code]",
            text=f'**Inline Usage**\n\n`@{asst.me.username} run python print("hello world")`\n\n[Language List](https://telegra.ph/Hugo-09-01-6)',
        )
        return await event.answer([result])
    output = (
        await async_searcher(
            PISTON_URI + "execute",
            post=True,
            json={"language": lang, "version": version, "files": [{"content": code}]},
            re_json=True,
        )
    )["run"]["output"] or get_string("instu_4")
    if len(output) > 3000:
        output = output[:3000] + "..."
    result = await event.builder.article(
        title="Result",
        description=output,
        text=f"• **Language:**\n`{lang}`\n\n• **Code:**\n`{code}`\n\n• **Result:**\n`{output}`",
        buttons=Button.switch_inline("Fork", query=event.text, same_peer=True),
    )
    await event.answer([result], switch_pm="• Piston •", switch_pm_param="start")
