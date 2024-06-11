# Application definition

INSTALLED_APPS = [
    'main.apps.MainConfig',
    'ecp.apps.EcpConfig',
    'cartridge.apps.CartridgeConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mptt',
    'django_cron',
    'rules',
]