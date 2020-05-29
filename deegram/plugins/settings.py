from asyncio import sleep

from telethon import Button, events

from .. import bot, users

search_buttons = [
    [
        Button.switch_inline("Search track 🎧", same_peer=True),
        Button.switch_inline("Search album 💽", query=".a: ", same_peer=True),
    ],
    [Button.inline("❌")],
]


@bot.on(events.NewMessage(pattern="/settings"))
async def settings(event):
    if hasattr(event, "query"):
        answer = event.edit
    else:
        answer = event.respond
    await answer(
        "Settings:",
        buttons=[[Button.inline("Quality 🎧", data="q")], [Button.inline("❌")]],
    )
    raise events.StopPropagation


@bot.on(events.CallbackQuery(pattern="q"))
async def settings_quality(event):
    q = users[event.query.user_id]["quality"]
    a = "Lossless"
    b = "High"
    c = "Medium"
    d = "Low"
    s = " ✅"

    if q == "FLAC":
        a += s
    elif q == "MP3_320":
        b += s
    elif q == "MP3_256":
        c += s
    elif q == "MP3_128":
        d += s

    await event.edit(
        "Select song quality: ",
        buttons=[
            [Button.inline(a, data="FLAC"), Button.inline(b, data="MP3_320")],
            [Button.inline(c, data="MP3_256"), Button.inline(d, data="MP3_128")],
            [Button.inline("◀️"), Button.inline("❌")],
        ],
    )


@bot.on(events.CallbackQuery(pattern=r"(FLAC|MP3_\d{3})"))
async def callback(event):
    q = event.data.decode("utf-8")
    if users[event.query.user_id]["quality"] != q:
        users[event.query.user_id]["quality"] = q
        await event.answer("Done!")
        await settings_quality(event)
    else:
        await event.answer("Already selected!")


@bot.on(events.CallbackQuery(pattern="❌"))
async def cancel(event):
    await event.edit("Canceled.")
    await sleep(1.5)
    await event.delete()


@bot.on(events.CallbackQuery(pattern="◀️"))
async def back_to_settings(event):
    await settings(event)
