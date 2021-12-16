import asyncio
import logging
import json

from config import (
    CHANNEL_ID, 
    INTERVAL, 
    TOKEN, 
    PATH_TO_TASKS, 
    LAST_TASK_ID_ENV_VAR_NAME
)
from os import environ

from aiogram import Dispatcher, Bot, executor
from aiogram.utils.exceptions import CantParseEntities


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

    
def save_last_task_number(task_id: int) -> None:
    """ Save last task number to enviroment variable """
    environ[LAST_TASK_ID_ENV_VAR_NAME] = str(task_id)
    print(environ[LAST_TASK_ID_ENV_VAR_NAME])


def get_last_task_id() -> int:
    """ Get last task id from enviroment variable """
    try:
        return int(environ[LAST_TASK_ID_ENV_VAR_NAME])
    except KeyError:
        return 0


def get_task_from_json(task_id: int) -> dict:
    with open(PATH_TO_TASKS, 'r') as f:
        data = json.loads(f.read())
    task = data[task_id+1]

    return task


def generate_level_for_task(task_id: int) -> str:
    if task_id <= 200:
        level = '😃'
    elif task_id <= 400:
        level = '😐'
    elif task_id <= 752:
        level = '😡'
    return level


async def send_task_to_channel(interval: int) -> None:
    for task_id in range(get_last_task_id(), 753):
        task_id += 1
        task = get_task_from_json(task_id)

        title = task['title']
        url = task['url']
        level = generate_level_for_task(task_id)
        text = task['text']

        message = f'**Task number {task_id}**\n'\
            f'**Level: {level}**\n{url}\n'\
            f'Bot: @EulerMossBot\n**{title}**\n{text}\n'\
            '**👇 More about the task**'

        if len(message) > 4096:
            text = text[:((len(message)+3)-len(text))]+'...'

        message = f'**Task number {task_id}**\n'\
            f'**Level: {level}**\n{url}\n'\
            f'Bot: @EulerMossBot\n**{title}**\n{text}\n'\
            '**👇 More about the task**'

        try:
            await bot.send_message(
                chat_id=CHANNEL_ID, 
                text=message, 
                parse_mode='markdown'
            )
        except CantParseEntities:
            await bot.send_message(
                chat_id=CHANNEL_ID, 
                text=message.replace('**', ''), 
                parse_mode='html'
            )

        save_last_task_number(task_id)
        await asyncio.sleep(interval)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(send_task_to_channel(INTERVAL))

    executor.start_polling(dp)
