"""
It's an example how to setup config.py file in this service.
The config.py file must be situated in the same directory as this
config_example.py file.
"""


from pathlib import Path

# In this folder there is a settings.py file
BASE_DIR = Path('/.../online_tests/online_tests')

SECRET_KEY = 'your_secret_key'

DEBUG = True

DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

INTERNAL_IPS = [
    '127.0.0.1',
]

ALLOWED_HOSTS = [
    '127.0.0.1',
]
