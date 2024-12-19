import aiogram
import asyncio
from aiogram import Bot, Dispatcher, Router
from config import settings
# from applications.handlers import rt
from Database.queries.orm import SyncORM

tk = settings.TOKEN

# SyncORM.create_tables()
# SyncORM.insert_data()
# SyncORM.get_cake_ingrs('Муссовый')


bot = Bot(token=tk)
dp = Dispatcher()
rt = Router()

async def main():
    dp.include_router(rt)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        print('execute')
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')

        {}

#test
