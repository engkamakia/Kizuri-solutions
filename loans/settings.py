#from decouple import config

#from dotenv import load_dotenv
#load_dotenv()
import dj_database_url
from pathlib import Path
import os

import cloudinary
import cloudinary.uploader
import cloudinary.api

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'django-insecure-(@v5_!wq8s3o&m16ec+4cwff+)*l6v0pw3x7ynfz)37@i4=v@-'
SECRET_KEY = os.environ.get("SECRET_KEY")
#SECRET_KEY = 'django-insecure-(@v5_!wq8s3o&m16ec+4cwff+)*l6v0pw3x7ynfz)37@i4=v@-'

#SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = os.environ.get("DEBUG", "False").lower()== "true"
DEBUG = True

#ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split("")
ALLOWED_HOSTS = ['https://kizuri-solutions-app.onrender.com','localhost', 'kizuri-solutions-app.onrender.com', '*']





INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'kopa',
    #'django_daraja',
    'cloudinary',
    'django.contrib.humanize', 
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




ROOT_URLCONF = 'loans.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
            ],
            'builtins': ['django.contrib.humanize.templatetags.humanize'],
        },
    },
]

WSGI_APPLICATION = 'loans.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'JVHUxvKUWbqOaUywrwZoBeXTfeeUwQbX',
        'HOST': 'junction.proxy.rlwy.net',
        'PORT': '11183',  # Use the correct port from the URL
    }
}
#postgresql://postgres:JVHUxvKUWbqOaUywrwZoBeXTfeeUwQbX@junction.proxy.rlwy.net:11183/railway
#database_url = os.environ.get("postgresql://kizuri_django_render_user:nuZ9iLVjYvGZOTrp8gAGZQ5737uKfdoR@dpg-cr7bmla3esus738688lg-a/kizuri_django_render")
'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'kizuri_django_render',  # Database name
        'USER': 'kizuri_django_render_user',  # Username
        'PASSWORD': 'nuZ9iLVjYvGZOTrp8gAGZQ5737uKfdoR',  # Password
        'HOST': 'dpg-cr7bmla3esus738688lg-a',  # Host
        'PORT': '5432',  # Default PostgreSQL port
    }
}'''

'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'kizuri',
        'USER': 'kizuri',
        'PASSWORD': 'Kamakia@91',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
'''

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'kopa.backends.IDNumberBackend',  # Replace 'your_app' with your actual app name
    'django.contrib.auth.backends.ModelBackend',  # Keep the default backend
]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Use database-backed sessions
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Keep the session alive even after closing the browser
SESSION_COOKIE_AGE = 1209600  # Session will last for 2 weeks
SESSION_SAVE_EVERY_REQUEST = True  # Save the session on every request

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


'''
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]



MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/img')

'''
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



MEDIA_URL = '/media/'
#MEDIA_ROOT = os.path.join(BASE_DIR, 'static/img')
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# adding config
cloudinary.config( 
  cloud_name = "dz7uhvnkh", 
  api_key = "818913352874198", 
  api_secret = "916WgWrEqpUg0E3sFdAPqdPj8Ak" 
)


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

