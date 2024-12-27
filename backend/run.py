import aiogram
import asyncio
from aiogram import Bot, Dispatcher, Router
from config import settings
from user_bot.handlers import rt as user_rt, bot as user_bot
from conf_bot.handlers import router as conf_rt, bot as conf_bot
from app.data import SyncORM

# SyncORM.create_table()
# SyncORM.insert_data()
from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from app.frontend_requests.views import router as frontend_router
from main import app

import multiprocessing


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(frontend_router)


class Bot_creator():
    def __init__(self, bot, rt):
        self.rt = rt
        self.dp = Dispatcher()
        self.bot = bot
        
    
    async def run(self):
        self.dp.include_router(self.rt)
        await self.dp.start_polling(self.bot)

def start_fastapi():
    uvicorn.run('run:app', reload=True)


user_bot = Bot_creator(user_bot, user_rt)
conf_bot = Bot_creator(conf_bot, conf_rt)

async def main():
    await asyncio.gather(user_bot.run(), conf_bot.run())

def run_bots():
    asyncio.run(main())


if __name__ == '__main__':
    try:
        SyncORM.create_table()
        SyncORM.insert_data()
        # SyncORM.create_test_confectioners(5616937568)

        bot_process = multiprocessing.Process(target=run_bots)
        app_process = multiprocessing.Process(target=start_fastapi)

        bot_process.start()
        app_process.start()

        bot_process.join()
        app_process.join()
        asyncio.run(main())

        
    except KeyboardInterrupt:
        print('Exit')
