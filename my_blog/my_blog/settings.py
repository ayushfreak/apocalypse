import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR=os.path.join(BASE_DIR,'templates')
STATIC_DIR=os.path.join(BASE_DIR,'static')
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
# PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_cdn')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h2^h_kml09v&kbd)o#a1!p-$wipn-t8ad)y*0qn9li0k!7=$-9'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


#SITE_ID = 4
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'blog',
    'taggit',
    'taggit_templatetags2',
    'ckeditor',
    'ckeditor_uploader',
    'django_cleanup',
    #automatically deletes media files when thier link deleted from database
    'crispy_forms',
     'rest_framework',
     'hitcount',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
      'allauth.socialaccount.providers.google',
      'allauth.socialaccount.providers.facebook',
]

#http://www.marinamele.com/user-authentication-with-google-using-django-allauth
CRISPY_TEMPLATE_PACK = 'bootstrap3'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}
AUTHENTICATION_BACKENDS = (

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    )

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]


class SiteMiddleware(object):
    def process_request(self, request):
        try:
            current_site = Site.objects.get(domain=request.get_host())
        except Site.DoesNotExist:
            current_site = Site.objects.get(id=settings.DEFAULT_SITE_ID)

        request.current_site = current_site
        settings.SITE_ID = current_site.id

ROOT_URLCONF = 'my_blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'my_blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'blog',
        'USER': 'blog_user',
        'PASSWORD': 'ayush504',
        'HOST': 'localhost',
        'PORT': '',
    }
}
# Parse database configuration from $DATABASE_URL
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Ensure EMAIL_BACKEND is set so allauth can proceed to send confirmation emails
# Set to console for development/testing

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
# Make email verification mandatory to avoid junk email accounts
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# Eliminate need to provide username, as it's a very old practice
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_USERNAME_REQUIRED = False
SOCIALACCOUNT_EMAIL_VERIFICATION=None
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'djproject1990@gmail.com'
EMAIL_HOST_PASSWORD = 'ayush1990'
EMAIL_PORT = 587
#EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
#console prints the mail on the terminal
#smtp sends the mail to the mail id
#to use it turn on less secure app.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
LOGIN_REDIRECT_URL = '/blog/'
LOGIN_URL = '/blog/'
STATIC_URL = '/static/'
ALLOWED_HOSTS = ['*']
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_RESTRICT_BY_USER=True
CKEDITOR_BROWSE_SHOW_DIRS=True
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'

CKEDITOR_CONFIGS = {
'default': {
'skin': 'moono',
# 'skin': 'office2013',
'toolbar_Basic': [
['Source', '-', 'Bold', 'Italic']
],
'toolbar_YourCustomToolbarConfig': [
{'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
{'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
{'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
{'name': 'forms',
'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
'HiddenField']},
'/',
{'name': 'basicstyles',
'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
{'name': 'paragraph',
'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
'Language']},
{'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
{'name': 'insert',
'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
'/',
{'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
{'name': 'colors', 'items': ['TextColor', 'BGColor']},
{'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
{'name': 'about', 'items': ['About']},
'/', # put this to force next toolbar on new line
{'name': 'yourcustomtools', 'items': [
# put the name of your editor.ui.addButton here
'Preview',
'Maximize',

]},
],
'toolbar': 'YourCustomToolbarConfig', # put selected toolbar config here
'tabSpaces': 4,
'extraPlugins': ','.join(
[
# your extra plugins here
'div','autolink','autoembed','embedsemantic','autogrow','uploadimage',
# 'devtools',
'widget','lineutils','clipboard','dialog','dialogui','elementspath'
]),}
}

HITCOUNT_KEEP_HIT_ACTIVE = { 'days': 7 }
HITCOUNT_HITS_PER_IP_LIMIT = 0
TAGGIT_TAGCLOUD_MIN = 1.0
TAGGIT_TAGCLOUD_MAX =6.0
#for django allauth for additional information
ACCOUNT_SIGNUP_FORM_CLASS = 'blog.forms.SignupForm'


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    # 'DEFAULT_PARSER_CLASSES': (
    #     'rest_framework.parsers.JSONParser',
    # )
    "DEFAULT_AUTHENTICATION_CLASSES": (
         'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        #'rest_framework.authentication.BasicAuthentication'

    ),
    "DEFAULT_PERMISSION_CLASSES": (
        'rest_framework.permissions.IsAuthenticated',
        #'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    )
}
