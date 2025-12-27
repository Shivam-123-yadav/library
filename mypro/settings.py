import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


# =======================
# SECURITY SETTINGS
# =======================

SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-&$32zp$z8sbj#t%cxopoiunbztirx97xw@j-13)xdipxi8tz%d'
)

DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".onrender.com",
    ".ngrok-free.app",
]

SITE_URL = os.getenv('SITE_URL', "https://library-1-u3wy.onrender.com")


# =======================
# APPLICATION DEFINITION
# =======================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'crispy_forms',
    'crispy_bootstrap5',

    'library',
]


# =======================
# MIDDLEWARE
# =======================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# =======================
# URL / TEMPLATE
# =======================

ROOT_URLCONF = 'mypro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'mypro.wsgi.application'


# =======================
# DATABASE
# =======================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# =======================
# PASSWORD VALIDATION
# =======================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# =======================
# INTERNATIONALIZATION
# =======================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# =======================
# STATIC FILES (IMPORTANT FIX)
# =======================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ❌ REMOVE STATICFILES_DIRS (Render me problem deta hai)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# =======================
# MEDIA FILES
# =======================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# =======================
# AUTH SETTINGS
# =======================

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'


# =======================
# EMAIL (SAFE MODE)
# =======================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# =======================
# CRISPY FORMS
# =======================

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# =======================
# GOOGLE CREDENTIALS
# =======================

GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS", "")

if GOOGLE_CREDENTIALS:
    creds_path = BASE_DIR / 'library' / 'utils' / 'credentials.json'
    creds_path.parent.mkdir(parents=True, exist_ok=True)

    if not creds_path.exists():
        with open(creds_path, 'w') as f:
            f.write(GOOGLE_CREDENTIALS)


# =======================
# LOGGING
# =======================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}


# =======================
# DEFAULT PRIMARY KEY
# =======================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
