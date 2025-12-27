"""
Django settings for mypro project.
"""

import os
from pathlib import Path
import environ
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize django-environ
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# =======================
# SECURITY SETTINGS
# =======================

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-&$32zp$z8sbj#t%cxopoiunbztirx97xw@j-13)xdipxi8tz%d')
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    "library-1-u3wy.onrender.com",
    "localhost",
    "127.0.0.1",
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
    'library',
    'crispy_forms', 
    'crispy_bootstrap5',
]

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

ROOT_URLCONF = 'mypro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',  
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'library.views.recent_books_and_authors',
            ], 
        },
    },
]

WSGI_APPLICATION = 'mypro.wsgi.application'


# =======================
# DATABASE
# =======================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
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
# STATIC FILES (CSS, JavaScript, Images)
# =======================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Static files directories
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Whitenoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Tell whitenoise to serve all files (including images)
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True if DEBUG else False

# Only include STATICFILES_DIRS if the directory exists
if os.path.exists(os.path.join(BASE_DIR, 'static')):
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]

# Whitenoise - don't use manifest storage to avoid errors with missing files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'


# =======================
# MEDIA FILES (User Uploads)
# =======================

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# =======================
# EMAIL CONFIGURATION
# =======================

# Use console backend to avoid SMTP timeout issues on Render
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Uncomment below when you setup proper email service
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'klickitshivam@gmail.com')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER', 'klickitshivam@gmail.com')
# EMAIL_TIMEOUT = 10

ORDER_NOTIFICATION_EMAIL = os.getenv('ORDER_NOTIFICATION_EMAIL', 'klickitshivam@gmail.com')


# =======================
# TWILIO WHATSAPP CONFIG
# =======================

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")


# =======================
# GOOGLE CREDENTIALS
# =======================

GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")

# Write Google credentials to file if present in environment
if GOOGLE_CREDENTIALS:
    creds_path = BASE_DIR / 'library' / 'utils' / 'credentials.json'
    creds_path.parent.mkdir(parents=True, exist_ok=True)
    
    if not creds_path.exists():
        try:
            with open(creds_path, 'w') as f:
                f.write(GOOGLE_CREDENTIALS)
        except Exception as e:
            print(f"Could not write Google credentials: {e}")


# =======================
# CRISPY FORMS
# =======================

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# =======================
# AUTHENTICATION
# =======================

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/book_list/'
LOGOUT_REDIRECT_URL = '/login/'


# =======================
# LOGGING CONFIGURATION
# =======================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'library': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


# =======================
# DEFAULT PRIMARY KEY FIELD TYPE
# =======================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
