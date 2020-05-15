"""
حذف اکانت های دیلیت شده بصورت خودکار

این قابلیت گروه ها/کانال ها را در طی دوره ۱ساعته بررسی کرده و اگر حسابی پاک شده باشد آن را بیرون خواهد کرد.
"""

from telethon import client, events, sessions, errors
from .global_functions import log, cooldown
from asyncio import sleep
import sqlite3


kick_counter = "kick_counter.txt"


@events.register(events.NewMessage(func=lambda e: not e.is_private))
@cooldown(60 * 60, False) # Only activate at minimum once an hour
async def kick_deleted(event):
    group = await event.get_chat() # Get group object
    kicked_users = 0

    response = list()
    async for user in event.client.iter_participants(group.id): # iterate over group members
        if not user.deleted: #  If it's a deleted account; kick
            continue
        try:
            await event.client.kick_participant(group, user)
            kicked_users += 1
        except errors.ChatAdminRequiredError:
            response.append(await event.respond(
                                "خطاب به مدیریت گروه، خطایی رخ داد:  "
                                + "من باید دسترسی Ban User رو داشته باشم تا بتونم حسابی رو پاک کنم."
                                + "بصورت ادمین مرا به اینجا اضافه کنید."))
            await log(event, "Invalid permissions")
            await event.client.kick_participant(group, me)
            break
        except errors.UserAdminInvalidError:
            response.append(await event.respond(
                                "خطاب به مدیریت گروه، اتفاقی غیرمنتظره رخ داد:  "
                                + "یکی از مدیر ها حسابش رو پاک کرد ولی من دسترسی کافی ندارم برای خارج کردن آن فرد.\n\n"
				+ "لطفا به صورت دستی اینکار را انجام دهید."))

    if kicked_users >= 0:
        await log(event, f"Kicked {kicked_users}")

    with open(kick_counter) as f: # Get the old value of kicked deleted accounts
        old_kicked = f.read()
        if not old_kicked:
            old_kicked = 0
    with open(kick_counter, "w") as f: # Write new value
        new_val = kicked_users + int(old_kicked)
        f.write(str(new_val))

    if not response:
        return

    await sleep(60)
    try:
        for m in response:
            await m.delete()
    except errors.ChannelPrivateError:
        return
