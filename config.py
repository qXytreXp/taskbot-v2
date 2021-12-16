from os import environ


TOKEN = environ.get("TASKBOT_TOKEN")
CHANNEL_ID = int(environ.get("TASKBOT_CHANNEL_ID"))
INTERVAL = int(environ.get("TASKBOT_INTERVAL", default=43200))

PATH_TO_TASKS = "tasks.json"
LAST_TASK_ID_ENV_VAR_NAME = "LAST_TASK_NUMBER"
