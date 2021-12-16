from os import environ


TOKEN = environ.get("TASKBOT_TOKEN", default="1368878751:AAFBJ2Zxbaed8Fr9rgrsMFZ0LMlP4QDuBbM")
CHANNEL_ID = int(environ.get("TASKBOT_CHANNEL_ID", default=-1001725420403))
INTERVAL = int(environ.get("TASKBOT_INTERVAL", default=10))  # 43200

PATH_TO_TASKS = "tasks.json"
PATH_TO_LAST_ID = "lasttaskid.txt"
LAST_TASK_ID_ENV_VAR_NAME = "LAST_TASK_ID"
