import os
import random
import string

DEBUG = bool(int(os.environ.get('DJANGO_DEBUG', 1)))

ALLOWED_HOSTS = ['*']
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    SECRET_KEY = ''.join(random.choice(string.ascii_lowercase) for i in range(32))
