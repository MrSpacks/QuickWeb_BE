from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ для Django (НЕ публикуй в проде)
SECRET_KEY = 'django-insecure-$k(g=2eh8w&+4tp)ro%ra-gz3m7c@8mqr536egw_@dtj_x1m#h'

# Включен режим отладки (только для разработки)
# DEBUG = True
DEBUG = False
ALLOWED_HOSTS = ["13.61.13.177"]
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

# Промежуточные слои обработки запросов
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # Поддержка CORS для работы с React-фронтендом
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Собственный middleware (если используешь для аналитики и т.п.)
    'api.middleware.VisitTrackingMiddleware',
]

ROOT_URLCONF = 'quick_web.urls'

# Настройки шаблонов (используются Django Views)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Здесь можно указать путь к HTML-шаблонам (если нужно)
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

# Используем SQLite для локальной разработки
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Проверка надёжности паролей
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Язык и часовой пояс
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Статические файлы (CSS, JS)
STATIC_URL = 'static/'

# Медиа-файлы (загрузки пользователей: фото, фон и т.д.)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Настройки Django REST Framework
REST_FRAMEWORK = {
    # Аутентификация через токен и сессии
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    # По умолчанию доступ только для авторизованных пользователей
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

# CORS (разрешаем доступ с фронтенда, например, React на порту 5173)
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
]

# Разрешённые методы и заголовки для запросов с фронтенда
CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
CORS_ALLOW_HEADERS = ['content-type', 'authorization']
CORS_ALLOW_CREDENTIALS = True  # Нужен, если работаешь с авторизацией через куки/сессии

# Тип поля по умолчанию для моделей
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',  # Вывод в терминал
            'level': 'DEBUG',  # Показывает все уровни (DEBUG, INFO, WARNING, ERROR)
        },
        'file': {
            'class': 'logging.FileHandler',  # Сохранение в файл
            'filename': 'debug.log',
            'level': 'DEBUG',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'api': {  # Логи для твоего приложения 'api'
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}