import aiogram
import asyncio
from aiogram import Bot, Dispatcher, Router
from config import settings
from user_bot.handlers import rt as user_rt, bot as user_bot
# from conf_bot.app.handlers import router as conf_rt, bot as conf_bot
from app.data import SyncORM

# SyncORM.create_table()
# SyncORM.insert_data()


class Bot_creator():
    def __init__(self, bot, rt):
        self.rt = rt
        self.dp = Dispatcher()
        self.bot = bot
        
    
    async def run(self):
        self.dp.include_router(self.rt)
        await self.dp.start_polling(self.bot)


user_bot = Bot_creator(user_bot, user_rt)
# conf_bot = Bot_creator(settings.CONF_BOT_TOKEN, conf_rt)

async def main():
    await asyncio.gather(user_bot.run())


if __name__ == '__main__':
    try:
        asyncio.run(main())
        # print('execute')
    except KeyboardInterrupt:
        print('Exit')
