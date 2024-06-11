import os
from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

STATIC_URL = '/static/'
if DEBUG:
        STATICFILES_DIRS = [
                os.path.join(BASE_DIR, 'static'),
        ]
else:
        STATIC_ROOT = os.path.join(BASE_DIR, 'static')


LOGIN_REDIRECT_URL = '/'

# For disable errors in browser - The Cross-Origin-Opener-Policy header has been ignored, because the URL's origin was untrustworthy. It was defined either
SECURE_CROSS_ORIGIN_OPENER_POLICY = None
# Activate if no database connection
# SESSION_COOKIE_SECURE = False

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

