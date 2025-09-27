from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# !!! Не забудь потом сменить секретный ключ, если проект выйдет в продакшн
SECRET_KEY = 'django-insecure-$k(g=2eh8w&+4tp)ro%ra-gz3m7c@8mqr536egw_@dtj_x1m#h'

# Оставляем DEBUG включённым везде
DEBUG = True

# Разрешаем доступ как с локали, так и с AWS
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "13.61.13.177",  #  AWS сервер
    "quick-web-fe.vercel.app",
    "webcardss.click"
]

# Установленные приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Сторонние библиотеки
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',

    # Приложения проекта
    'api',
]

# Промежуточные слои
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'api.middleware.VisitTrackingMiddleware',
]

ROOT_URLCONF = 'quick_web.urls'

# Шаблоны
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'quick_web.wsgi.application'

# База данных SQLite (файл в проекте)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Валидаторы паролей
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Локаль
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Статика и медиа
STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

# CORS: разрешаем локальный фронт и AWS по IP
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://13.61.13.177:8000",
    "http://13.62.115.181:8000",  # AWS сервер
    "https://quick-web-fe.vercel.app",
    "https://webcardss.click"

]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "origin",
    "x-csrftoken",
    "x-requested-with",
]
CORS_ALLOW_CREDENTIALS = True

# Primary key type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Логирование
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'level': 'DEBUG'},
        'file': {'class': 'logging.FileHandler', 'filename': 'debug.log', 'level': 'DEBUG'},
    },
    'root': {'handlers': ['console', 'file'], 'level': 'DEBUG'},
    'loggers': {
        'django': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'api': {'handlers': ['console', 'file'], 'level': 'DEBUG', 'propagate': False},
    },
}
