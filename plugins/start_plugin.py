"""پیام آغازین

دستور: 
`/start`
"""

from asyncio import sleep
from .global_functions import log
from telethon import client, events, errors


# /start
@events.register(events.NewMessage(pattern=r"/start$"))
async def on_start(event):
    if event.is_private:    # If command was sent in private
        await log(event)    # Logs the event
        await event.respond(
            "این ربات برای حذف حساب های پاک شده است."
            + "نیازمند دسترسی `ban user` در گفتگوی شماست.\n\n"
            + "[پشتیبانی](https://t.me/MSXadmin)\n"
            + "ارسال /help برای اطلاعات بیشتر.\n\n"
            + "⚡️ @MSXtm",
            link_preview=False)


# Reply when added to group
@events.register(events.ChatAction(func=lambda e:e.user_added and e.is_group))
async def added_to_group(event):
    group = await event.get_chat() # Get group object
    me = (await event.client.get_me()).id

    response = None
    for u in event.users:
        if me == u.id:
            response = await event.respond(
                "من بطور خودکار هر ساعت گروه ها را برای بررسی حساب های کاربری حذف شده بررسی میکنم.\n"
                + "[پشتیبانی](https://t.me/MSXadmin)\n\n"
                + "⚡️ @MSXtm",
                link_preview=False)

    if not response:
        return

    await sleep(60)
    try:
        await response.delete()
    except errors.ChannelPrivateError:
        return
