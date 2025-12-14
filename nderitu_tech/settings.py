from pathlib import Path

# -------------------- BASE --------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------- SECURITY --------------------
SECRET_KEY = 'django-insecure-7i9mc-7yj)zrale(@64$l9t9f49yo6umno4(czqo9@^%d^kza3'
DEBUG = True
ALLOWED_HOSTS = []

# -------------------- APPLICATIONS --------------------
INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Our apps
    'users',
    'products',
    'orders',
    'pesapal_app',  # <--- renamed payments app
]

# -------------------- MIDDLEWARE --------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -------------------- URL CONFIG --------------------
ROOT_URLCONF = 'nderitu_tech.urls'

# -------------------- TEMPLATES --------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Add custom template dirs if needed
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # required for admin
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# -------------------- WSGI --------------------
WSGI_APPLICATION = 'nderitu_tech.wsgi.application'

# -------------------- DATABASE --------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -------------------- PASSWORD VALIDATORS --------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# -------------------- INTERNATIONALIZATION --------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# -------------------- STATIC FILES --------------------
STATIC_URL = 'static/'

# -------------------- DEFAULT PRIMARY KEY --------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------- CUSTOM USER MODEL --------------------
AUTH_USER_MODEL = 'users.User'  # <--- Custom user model

# -------------------- PESAPAL PAYMENT SETTINGS --------------------
# Sandbox URL (use live URL when going live)
PESAPAL_POST_URL = 'https://demo.pesapal.com/api/PostPesapalDirectOrderV4'

# Your PesaPal credentials
PESAPAL_CONSUMER_KEY = 'h2axiYExlt3F58xYxZkPOjjL+U7aCVLn'
PESAPAL_CONSUMER_SECRET = 'gGtaa4qXIxP0x0/qqHRPCmEgAJU='

# Optional: Currency to use
PESAPAL_CURRENCY = 'KES'
