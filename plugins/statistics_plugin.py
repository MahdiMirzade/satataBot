"""دریافت آمار اکانت های حذف شده.

دستور:  
`/stats‍‍`
`/statistics`
"""

from telethon import client, events
from .global_functions import log

@events.register(events.NewMessage(pattern=r"/stat(s|istics)?$"))
async def stats(event):
    if not event.is_private:
        return

    with open("kick_counter.txt") as f:
        kick_counter = f.read()

    if not kick_counter:
        kick_counter = 0

    await event.reply(f"من درحال حاضر `{kick_counter}` حساب کاربری پاک شده رو بن کردم.")
    await log(event, kick_counter)
