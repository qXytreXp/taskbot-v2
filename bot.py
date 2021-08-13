import asyncio
import logging
import json

from config import (
    CHANNEL_ID, 
    INTERVAL, 
    TOKEN, 
    PATH_TO_TASKS, 
    PATH_TO_LAST_ID
)
from aiogram import Dispatcher, Bot, executor
from aiogram.utils.exceptions import CantParseEntities


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

    
def write_last_task_id(path_to_file: str, task_id) -> None:
    with open(path_to_file, 'w') as f:
        f.write(str(task_id))
        f.truncate()


def get_last_task_id(path_to_file):
    with open(path_to_file, 'r') as f:
        id_ = f.read()
    if id_:
        return int(id_) if int(id_) != 0 else 1
    else:
        write_last_task_id(PATH_TO_LAST_ID, 1)
        return 1


def get_task_from_json(path_to_file: str, task_id: int) -> int:
    with open(path_to_file, 'r') as f:
        data = json.loads(f.read())
    task = data[task_id+1]

    return task


def generate_level_for_task(task: dict) -> str:
    task_id = int(task['id'])

    if task_id <= 200:
        level = '😃'
    elif task_id <= 400:
        level = '😐'
    elif task_id <= 752:
        level = '😡'
    return level


async def send_task_to_channell(interval: int) -> None:
    for task_id in range(get_last_task_id(PATH_TO_LAST_ID)+1, 753):
        task = get_task_from_json(PATH_TO_TASKS, task_id)

        title = task['title']
        url = task['url']
        level = generate_level_for_task(task)
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

        write_last_task_id(PATH_TO_LAST_ID, task_id)
        await asyncio.sleep(interval)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(send_task_to_channell(INTERVAL))

    executor.start_polling(dp, skip_updates=True)
