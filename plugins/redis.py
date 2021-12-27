# Hugo - UserBot
# Copyright (C) TeamHugoX
#
# This file is a part of < https://github.com/TeamHugoX/Hugo/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamHugoX/Hugo/blob/main/LICENSE/>.
"""
**༄** Commands Available -

• **DataBase Commands, do not use if you don't know what it is.**

• `{i}setredis key | value`
    Redis Set Value.
    e.g :
    `{i}setredis hi there`
    `{i}setredis hi there | hugo here`

• `{i}delredis key`
    Delete Key from Redis DB

• `{i}renredis old keyname | new keyname`
    Update Key Name
"""

import re

from . import Redis, eor, udB, hugo_cmd


@hugo_cmd(pattern="setredis ?(.*)", fullsudo=True)
async def _(hg):
    try:
        delim = " " if re.search("[|]", hg.pattern_match.group(1)) is None else " | "
        data = hg.pattern_match.group(1).split(delim, maxsplit=1)
        udB.set(data[0], data[1])
        redisdata = Redis(data[0])
        await eor(
            hg,
            "Redis Key Value Pair Updated\nKey : `{}`\nValue : `{}`".format(
                data[0],
                redisdata,
            ),
        )
    except BaseException:
        await eor(hg, "`Something Went Wrong`")


@hugo_cmd(pattern="delredis ?(.*)", fullsudo=True)
async def _(hg):
    try:
        key = hg.pattern_match.group(1)
        k = udB.delete(key)
        if k == 0:
            return await eor(hg, "`No Such Key.`")
        await eor(hg, f"`Successfully deleted key {key}`")
    except BaseException:
        await eor(hg, "`Something Went Wrong`")


@hugo_cmd(pattern="renredis ?(.*)", fullsudo=True)
async def _(hg):
    delim = " " if re.search("[|]", hg.pattern_match.group(1)) is None else " | "
    data = hg.pattern_match.group(1).split(delim)
    if Redis(data[0]):
        try:
            udB.rename(data[0], data[1])
            await eor(
                hg,
                "Redis Key Rename Successful\nOld Key : `{}`\nNew Key : `{}`".format(
                    data[0],
                    data[1],
                ),
            )
        except BaseException:
            await eor(hg, "Something went wrong ...")
    else:
        await eor(hg, "Key not found")
