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

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True


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
    'django.contrib.humanize',  # For human readable numbers
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

# Database configuration for Render (if using PostgreSQL)
if os.getenv('RENDER'):
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )


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

# Ensure static directory exists
if not os.path.exists(os.path.join(BASE_DIR, 'static')):
    os.makedirs(os.path.join(BASE_DIR, 'static'), exist_ok=True)

# Create subdirectories in static folder
static_subdirs = ['css', 'js', 'images', 'fonts']
for subdir in static_subdirs:
    dir_path = os.path.join(BASE_DIR, 'static', subdir)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)

# Whitenoise configuration
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Whitenoise settings
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = DEBUG  # Auto-refresh only in debug mode
WHITENOISE_MANIFEST_STRICT = False  # Don't raise errors for missing files

# Static files finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


# =======================
# MEDIA FILES (User Uploads)
# =======================

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Ensure media directory exists
if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT, exist_ok=True)

# Create subdirectories in media folder
media_subdirs = ['logo', 'images', 'books', 'authors', 'uploads']
for subdir in media_subdirs:
    dir_path = os.path.join(MEDIA_ROOT, subdir)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)


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

# Session settings
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False


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
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'library': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


# =======================
# DEFAULT PRIMARY KEY FIELD TYPE
# =======================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =======================
# ADDITIONAL SETTINGS
# =======================

# File upload settings
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
FILE_UPLOAD_PERMISSIONS = 0o644

# Add mimetypes for better file serving
import mimetypes
mimetypes.add_type("image/svg+xml", ".svg", True)
mimetypes.add_type("image/webp", ".webp", True)

# Auto-create missing files on startup
def create_missing_files():
    """Create essential static and media files if they don't exist."""
    
    # Create basic CSS file if missing
    css_file = os.path.join(BASE_DIR, 'static', 'css', 'style.css')
    if not os.path.exists(css_file):
        css_content = """/* Basic CSS for Library Management System */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f8f9fa;
    margin: 0;
    padding: 0;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.navbar {
    background-color: #343a40;
    color: white;
    padding: 15px 0;
}

.navbar a {
    color: white;
    text-decoration: none;
    margin: 0 15px;
}

.card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    padding: 20px;
    margin-bottom: 20px;
}

.btn {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    text-decoration: none;
    display: inline-block;
}

.btn-primary {
    background-color: #007bff;
    color: white;
}

.btn-success {
    background-color: #28a745;
    color: white;
}

.btn-danger {
    background-color: #dc3545;
    color: white;
}

.table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}

.table th, .table td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

.table th {
    background-color: #f8f9fa;
    font-weight: bold;
}

.alert {
    padding: 15px;
    border-radius: 4px;
    margin: 20px 0;
}

.alert-success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.alert-danger {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

.alert-warning {
    background-color: #fff3cd;
    color: #856404;
    border: 1px solid #ffeaa7;
}

/* Responsive design */
@media (max-width: 768px) {
    .container {
        padding: 10px;
    }
    
    .navbar {
        padding: 10px 0;
    }
    
    .table {
        display: block;
        overflow-x: auto;
    }
}"""
        
        os.makedirs(os.path.dirname(css_file), exist_ok=True)
        with open(css_file, 'w') as f:
            f.write(css_content)
        print(f"Created missing CSS file: {css_file}")

# Run file creation on startup
if DEBUG:
    create_missing_files()
