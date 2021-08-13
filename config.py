from os import environ


TOKEN = environ.get('TASKBOT_TOKEN')
CHANNEL_ID = environ.get('TASKBOT_CHANNEL_ID')
INTERVAL = environ.get('TASKBOT_INTERVAL', default=43200)

PATH_TO_TASKS = 'tasks.json'
PATH_TO_LAST_ID = 'lasttaskid.txt'
