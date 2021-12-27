# Hugo - UserBot
# Copyright (C) TeamHugoX
#
# This file is a part of < https://github.com/TeamHugoX/Hugo/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamHugoX/Hugo/blob/main/LICENSE/>.
"""
**༄** Commands Available -

• `{i}border <reply to photo/sticker>`
    To create border around that media..
    Ex - `{i}border 12,22,23`
       - `{i}border 12,22,23 ; width (in number)`

• `{i}grey <reply to any media>`
    To make it black nd white.

• `{i}color <reply to any Black nd White media>`
    To make it Colorfull.

• `{i}toon <reply to any media>`
    To make it toon.

• `{i}danger <reply to any media>`
    To make it look Danger.

• `{i}negative <reply to any media>`
    To make negative image.

• `{i}blur <reply to any media>`
    To make it blurry.

• `{i}quad <reply to any media>`
    create a Vortex.

• `{i}mirror <reply to any media>`
    To create mirror pic.

• `{i}flip <reply to any media>`
    To make it flip.

• `{i}sketch <reply to any media>`
    To draw its sketch.

• `{i}blue <reply to any media>`
    just cool.

• `{i}csample <color name /color code>`
   example : `{i}csample red`
             `{i}csample #ffffff`

• `{i}pixelator <reply image>`
    Create a Pixelated Image..
"""
import asyncio
import os

import aiohttp
import cv2
import numpy as np
from PIL import Image
from telegraph import upload_file as upf
from telethon.errors.rpcerrorlist import (
    ChatSendMediaForbiddenError,
    MessageDeleteForbiddenError,
)

from . import Redis, download_file, eor, get_string, requests, udB, hugo_cmd


@hugo_cmd(
    pattern="sketch$",
)
async def sketch(e):
    ureply = await e.get_reply_message()
    xx = await eor(e, "`...`")
    if not (ureply and (ureply.media)):
        await xx.edit(get_string("cvt_3"))
        return
    ultt = await ureply.download_media()
    if ultt.endswith(".tgs"):
        await xx.edit(get_string("sts_9"))
        cmd = ["lottie_convert.py", ultt, "hg.png"]
        file = "hg.png"
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    else:
        await xx.edit(get_string("com_1"))
        img = cv2.VideoCapture(ultt)
        heh, lol = img.read()
        cv2.imwrite("hg.png", lol)
        file = "hg.png"
    img = cv2.imread(file)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted_gray_image = 255 - gray_image
    blurred_img = cv2.GaussianBlur(inverted_gray_image, (21, 21), 0)
    inverted_blurred_img = 255 - blurred_img
    pencil_sketch_IMG = cv2.divide(gray_image, inverted_blurred_img, scale=256.0)
    cv2.imwrite("hugo.png", pencil_sketch_IMG)
    await e.reply(file="hugo.png")
    await xx.delete()
    os.remove(file)
    os.remove("hugo.png")


@hugo_cmd(pattern="color$")
async def _(event):
    reply = await event.get_reply_message()
    if not reply.media:
        return await eor(event, "`Reply To a Black nd White Image`")
    xx = await eor(event, "`Coloring image 🎨🖌️...`")
    image = await reply.download_media()
    img = cv2.VideoCapture(image)
    ret, frame = img.read()
    cv2.imwrite("hg.jpg", frame)
    if udB.get("DEEP_API"):
        key = Redis("DEEP_API")
    else:
        key = "quickstart-QUdJIGlzIGNvbWluZy4uLi4K"
    r = requests.post(
        "https://api.deepai.org/api/colorizer",
        files={"image": open("hg.jpg", "rb")},
        headers={"api-key": key},
    )
    os.remove("hg.jpg")
    os.remove(image)
    if "status" in r.json():
        return await event.edit(
            r.json()["status"] + "\nGet api nd set `{i}setredis DEEP_API key`"
        )
    r_json = r.json()["output_url"]
    await event.client.send_file(event.chat_id, r_json, reply_to=reply)
    await xx.delete()


@hugo_cmd(
    pattern="grey$",
)
async def hgd(event):
    ureply = await event.get_reply_message()
    if not (ureply and (ureply.media)):
        await eor(event, get_string("cvt_3"))
        return
    ultt = await ureply.download_media()
    if ultt.endswith(".tgs"):
        xx = await eor(event, get_string("sts_9"))
        cmd = ["lottie_convert.py", ultt, "hg.png"]
        file = "hg.png"
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    else:
        xx = await eor(event, get_string("com_1"))
        img = cv2.VideoCapture(ultt)
        heh, lol = img.read()
        cv2.imwrite("hg.png", lol)
        file = "hg.png"
    hg = cv2.imread(file)
    hugo = cv2.cvtColor(hg, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("hg.jpg", hugo)
    await event.client.send_file(
        event.chat_id,
        "hg.jpg",
        force_document=False,
        reply_to=event.reply_to_msg_id,
    )
    await xx.delete()
    os.remove("hg.png")
    os.remove("hg.jpg")
    os.remove(ultt)


@hugo_cmd(
    pattern="blur$",
)
async def hgd(event):
    ureply = await event.get_reply_message()
    if not (ureply and (ureply.media)):
        await eor(event, get_string("cvt_3"))
        return
    ultt = await ureply.download_media()
    if ultt.endswith(".tgs"):
        xx = await eor(event, get_string("sts_9"))
        cmd = ["lottie_convert.py", ultt, "hg.png"]
        file = "hg.png"
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    else:
        xx = await eor(event, get_string("com_1"))
        img = cv2.VideoCapture(ultt)
        heh, lol = img.read()
        cv2.imwrite("hg.png", lol)
        file = "hg.png"
    hg = cv2.imread(file)
    hugo = cv2.GaussianBlur(hg, (35, 35), 0)
    cv2.imwrite("hg.jpg", hugo)
    await event.client.send_file(
        event.chat_id,
        "hg.jpg",
        force_document=False,
        reply_to=event.reply_to_msg_id,
    )
    await xx.delete()
    for i in ["hg.png", "hg.jpg", ultt]:
        if os.path.exists(i):
            os.remove(i)


@hugo_cmd(
    pattern="negative$",
)
async def hgd(event):
    ureply = await event.get_reply_message()
    xx = await eor(event, "`...`")
    if not (ureply and (ureply.media)):
        await xx.edit(get_string("cvt_3"))
        return
    ultt = await ureply.download_media()
    if ultt.endswith(".tgs"):
        await xx.edit(get_string("sts_9"))
        cmd = ["lottie_convert.py", ultt, "hg.png"]
        file = "hg.png"
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    else:
        await xx.edit(get_string("com_1"))
        img = cv2.VideoCapture(ultt)
        heh, lol = img.read()
        cv2.imwrite("hg.png", lol)
        file = "hg.png"
    hg = cv2.imread(file)
    hugo = cv2.bitwise_not(hg)
    cv2.imwrite("hg.jpg", hugo)
    await event.client.send_file(
        event.chat_id,
        "hg.jpg",
        force_document=False,
        reply_to=event.reply_to_msg_id,
    )
    await xx.delete()
    os.remove("hg.png")
    os.remove("hg.jpg")
    os.remove(ultt)


@hugo_cmd(
    pattern="mirror$",
)
async def hgd(event):
    ureply = await event.get_reply_message()
    xx = await eor(event, "`...`")
    if not (ureply and (ureply.media)):
        await xx.edit(get_string("cvt_3"))
        return
    ultt = await ureply.download_media()
    if ultt.endswith(".tgs"):
        await xx.edit(get_string("sts_9"))
        cmd = ["lottie_convert.py", ultt, "hg.png"]
        file = "hg.png"
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    else:
        await xx.edit(get_string("com_1"))
        img = cv2.VideoCapture(ultt)
        heh, lol = img.read()
        cv2.imwrite("hg.png", lol)
        file = "hg.png"
    hg = cv2.imread(file)
    ish = cv2.flip(hg, 1)
    hugo = cv2.hconcat([hg, ish])
    cv2.imwrite("hg.jpg", hugo)
    await event.client.send_file(
        event.chat_id,
        "hg.jpg",
        force_document=False,
        reply_to=event.reply_to_msg_id,
    )
    await xx.delete()
    os.remove("hg.png")
    os.remove("hg.jpg")
    os.remove(ultt)


@hugo_cmd(
    pattern="flip$",
)
async def hgd(event):
    ureply = await event.get_reply_message()
    xx = await eor(event, "`...`")
    if not (ureply and (ureply.media)):
        await xx.edit(get_string("cvt_3"))
        return
    ultt = await ureply.download_media()
    if ultt.endswith(".tgs"):
        await xx.edit(get_string("sts_9"))
        cmd = ["lottie_convert.py", ultt, "hg.png"]
        file = "hg.png"
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    else:
        await xx.edit(get_string("com_1"))
        img = cv2.VideoCapture(ultt)
        heh, lol = img.read()
        cv2.imwrite("hg.png", lol)
        file = "hg.png"
    hg = cv2.imread(file)
    trn = cv2.flip(hg, 1)
    ish = cv2.rotate(trn, cv2.ROTATE_180)
    hugo = cv2.vconcat([hg, ish])
    cv2.imwrite("hg.jpg", hugo)
    await event.client.send_file(
        event.chat_id,
        "hg.jpg",
        force_document=False,
        reply_to=event.reply_to_msg_id,
    )
    await xx.delete()
    os.remove("hg.png")
    os.remove("hg.jpg")
    os.remove(ultt)


@hugo_cmd(
    pattern="quad$",
)
async def hgd(event):
    ureply = await event.get_reply_message()
    xx = await eor(event, "`...`")
    if not (ureply and (ureply.media)):
        await xx.edit(get_string("cvt_3"))
        return
    ultt = await ureply.download_media()
    if ultt.endswith(".tgs"):
        await xx.edit(get_string("sts_9"))
        cmd = ["lottie_convert.py", ultt, "hg.png"]
        file = "hg.png"
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    else:
        await xx.edit(get_string("com_1"))
        img = cv2.VideoCapture(ultt)
        heh, lol = img.read()
        cv2.imwrite("hg.png", lol)
        file = "hg.png"
    hg = cv2.imread(file)
    roid = cv2.flip(hg, 1)
    mici = cv2.hconcat([hg, roid])
    fr = cv2.flip(mici, 1)
    trn = cv2.rotate(fr, cv2.ROTATE_180)
    hugo = cv2.vconcat([mici, trn])
    cv2.imwrite("hg.jpg", hugo)
    await event.client.send_file(
        event.chat_id,
        "hg.jpg",
        force_document=False,
        reply_to=event.reply_to_msg_id,
    )
    await xx.delete()
    os.remove("hg.png")
    os.remove("hg.jpg")
    os.remove(ultt)


@hugo_cmd(
    pattern="toon$",
)
async def hgd(event):
    ureply = await event.get_reply_message()
    xx = await eor(event, "`...`")
    if not (ureply and (ureply.media)):
        await xx.edit(get_string("cvt_3"))
        return
    ultt = await ureply.download_media()
    if ultt.endswith(".tgs"):
        await xx.edit(get_string("sts_9"))
        cmd = ["lottie_convert.py", ultt, "hg.png"]
        file = "hg.png"
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    else:
        await xx.edit(get_string("com_1"))
        img = cv2.VideoCapture(ultt)
        heh, lol = img.read()
        cv2.imwrite("hg.png", lol)
        file = "hg.png"
    hg = cv2.imread(file)
    height, width, channels = hg.shape
    samples = np.zeros([height * width, 3], dtype=np.float32)
    count = 0
    for x in range(height):
        for y in range(width):
            samples[count] = ult[x][y]
            count += 1
    compactness, labels, centers = cv2.kmeans(
        samples,
        12,
        None,
        (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001),
        5,
        cv2.KMEANS_PP_CENTERS,
    )
    centers = np.uint8(centers)
    ish = centers[labels.flatten()]
    hugo = ish.reshape(ult.shape)
    cv2.imwrite("hg.jpg", hugo)
    await event.client.send_file(
        event.chat_id,
        "hg.jpg",
        force_document=False,
        reply_to=event.reply_to_msg_id,
    )
    await xx.delete()
    os.remove("hg.png")
    os.remove("hg.jpg")
    os.remove(ultt)


@hugo_cmd(
    pattern="danger$",
)
async def hgd(event):
    ureply = await event.get_reply_message()
    xx = await eor(event, "`...`")
    if not (ureply and (ureply.media)):
        await xx.edit(get_string("cvt_3"))
        return
    ultt = await ureply.download_media()
    if ultt.endswith(".tgs"):
        await xx.edit(get_string("sts_9"))
        cmd = ["lottie_convert.py", ultt, "hg.png"]
        file = "hg.png"
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    else:
        await xx.edit(get_string("com_1"))
        img = cv2.VideoCapture(ultt)
        heh, lol = img.read()
        cv2.imwrite("hg.png", lol)
        file = "hg.png"
    hg = cv2.imread(file)
    dan = cv2.cvtColor(hg, cv2.COLOR_BGR2RGB)
    hugo = cv2.cvtColor(dan, cv2.COLOR_HSV2BGR)
    cv2.imwrite("hg.jpg", hugo)
    await event.client.send_file(
        event.chat_id,
        "hg.jpg",
        force_document=False,
        reply_to=event.reply_to_msg_id,
    )
    await xx.delete()
    os.remove("hg.png")
    os.remove("hg.jpg")
    os.remove(ultt)


@hugo_cmd(pattern="csample (.*)")
async def sampl(hg):
    color = hg.pattern_match.group(1)
    if color:
        img = Image.new("RGB", (200, 100), f"{color}")
        img.save("csample.png")
        try:
            try:
                await hg.delete()
                await hg.client.send_message(
                    hg.chat_id, f"Colour Sample for `{color}` !", file="csample.png"
                )
            except MessageDeleteForbiddenError:
                await hg.reply(f"Colour Sample for `{color}` !", file="csample.png")
        except ChatSendMediaForbiddenError:
            await eor(hg, "Umm! Sending Media is disabled here!")

    else:
        await eor(hg, "Wrong Color Name/Hex Code specified!")


@hugo_cmd(
    pattern="blue$",
)
async def hgd(event):
    ureply = await event.get_reply_message()
    xx = await eor(event, "`...`")
    if not (ureply and (ureply.media)):
        await xx.edit(get_string("cvt_3"))
        return
    ultt = await ureply.download_media()
    if ultt.endswith(".tgs"):
        await xx.edit(get_string("sts_9"))
        cmd = ["lottie_convert.py", ultt, "hg.png"]
        file = "hg.png"
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    else:
        await xx.edit(get_string("com_1"))
        img = cv2.VideoCapture(ultt)
        heh, lol = img.read()
        cv2.imwrite("hg.png", lol)
        file = "hg.png"
    got = upf(file)
    lnk = f"https://telegra.ph{got[0]}"
    async with aiohttp.ClientSession() as ses:
        async with ses.get(
            f"https://nekobot.xyz/api/imagegen?type=blurpify&image={lnk}"
        ) as out:
            r = await out.json()
    ms = r.get("message")
    if not r["success"]:
        return await xx.edit(ms)
    await download_file(ms["message"], "hg.png")
    img = Image.open("hg.png").convert("RGB")
    img.save("ult.webp", "webp")
    await event.client.send_file(
        event.chat_id,
        "ult.webp",
        force_document=False,
        reply_to=event.reply_to_msg_id,
    )
    await xx.delete()
    os.remove("hg.png")
    os.remove("ult.webp")
    os.remove(ultt)


@hugo_cmd(pattern="border ?(.*)")
async def ok(event):
    hm = await event.get_reply_message()
    if not (hm and (hm.photo or hm.sticker)):
        return await eor(event, "`Reply to Sticker or Photo..`")
    col = event.pattern_match.group(1)
    wh = 20
    if not col:
        col = [255, 255, 255]
    else:
        try:
            if ";" in col:
                col_ = col.split(";", maxsplit=1)
                wh = int(col_[1])
                col = col_[0]
            col = [int(col) for col in col.split(",")[:2]]
        except ValueError:
            return await eor(event, "`Not a Valid Input...`")
    okla = await hm.download_media()
    img1 = cv2.imread(okla)
    constant = cv2.copyMakeBorder(img1, wh, wh, wh, wh, cv2.BORDER_CONSTANT, value=col)
    cv2.imwrite("output.png", constant)
    await event.client.send_file(event.chat.id, "output.png")
    os.remove("output.png")
    os.remove(okla)
    await event.delete()


@hugo_cmd(pattern="pixelator ?(.*)")
async def pixelator(event):
    reply_message = await event.get_reply_message()
    if not (reply_message and reply_message.photo):
        return await eor(event, "`Reply to a photo`")
    hw = 50
    try:
        hw = int(event.pattern_match.group(1))
    except (ValueError, TypeError):
        pass
    msg = await eor(event, get_string("com_1"))
    image = await reply_message.download_media()
    input_ = cv2.imread(image)
    height, width = input_.shape[:2]
    w, h = (hw, hw)
    temp = cv2.resize(input_, (w, h), interpolation=cv2.INTER_LINEAR)
    output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
    cv2.imwrite("output.jpg", output)
    await msg.respond("• Pixelated by Hugo", file="output.jpg")
    await msg.delete()
    os.remove("output.jpg")
    os.remove(image)
