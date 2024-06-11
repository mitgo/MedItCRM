from split_settings.tools import optional, include

include(
    'base/env.py',

    'base/assets.py',
    'base/apps.py',
    'base/middleware.py',
    'base/debug_toolbar.py',
    'base/*.py',
)