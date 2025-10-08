"""
Django settings for config project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# -------------------------------------------------------------------
# BASE CONFIGURATION
# -------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')  # charge les variables d’environnement
os.environ["PGCLIENTENCODING"] = "utf8"

# -------------------------------------------------------------------
# SECURITY
# -------------------------------------------------------------------

SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-blhdrts6==6n+r9+!2s1p#%0x@250lk+4r#1r@$tt#t*4m9c)k'
)

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.getenv(
    'ALLOWED_HOSTS',
    '127.0.0.1,localhost,medium-style-blog-django.onrender.com'
).split(',')

# -------------------------------------------------------------------
# APPLICATIONS
# -------------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps
    'blog',
    'authenticated',
]

# -------------------------------------------------------------------
# MIDDLEWARE
# -------------------------------------------------------------------

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

ROOT_URLCONF = 'config.urls'

# -------------------------------------------------------------------
# TEMPLATES
# -------------------------------------------------------------------

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

WSGI_APPLICATION = 'config.wsgi.application'

# -------------------------------------------------------------------
# DATABASE
# -------------------------------------------------------------------

DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

# -------------------------------------------------------------------
# PASSWORD VALIDATION
# -------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------------------------------------------
# INTERNATIONALIZATION
# -------------------------------------------------------------------

LANGUAGE_CODE = 'fr-FR'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------------------
# STATIC FILES
# -------------------------------------------------------------------

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'public']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# -------------------------------------------------------------------
# MEDIA FILES (UPLOADS)
# -------------------------------------------------------------------
# ✅ IMPORTANT POUR RENDER :
# Le disk Render doit être monté sur /media
# (dans le Dashboard Render → onglet “Disks” → Mount Path = /media)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', '/opt/render/project/src/media')

# -------------------------------------------------------------------
# DEFAULT PRIMARY KEY
# -------------------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==============================================================
# MEDIA FILES - CLOUDINARY CONFIGURATION
# ==============================================================

import os
from django.core.exceptions import ImproperlyConfigured

# Vérifie la variable Cloudinary
CLOUDINARY_URL = os.getenv('CLOUDINARY_URL')
if not CLOUDINARY_URL:
    raise ImproperlyConfigured(
        "⚠️  La variable CLOUDINARY_URL est manquante. "
        "Ajoute-la dans ton fichier .env et dans Render → Environment."
    )

INSTALLED_APPS += [
    'cloudinary',
    'cloudinary_storage',
]

# Utilise Cloudinary pour tous les fichiers uploadés
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# (Optionnel) Fallback local pour le dev
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
