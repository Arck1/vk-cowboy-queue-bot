import os

DEBUG = os.environ.get("DEBUG", 'false') == 'false'

LOGIN = os.environ.get("LOGIN", "user")
PASSWORD = os.environ.get("PASSWORD", "mysecretpassword")
GROUP_ID = int(os.environ.get("GROUP_ID", '-1'))
TIMEOUT = int(os.environ.get("TIMEOUT", 1000))
MESSAGE = os.environ.get("MESSAGE", "+")

try:
    from local_settings import *
except:
    pass
