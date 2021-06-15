import os

# captcha
GOOGLE_RECAPTCHA_SECRET_KEY = '6LdSc50aAAAAAK6-Q7PA53xrwtm2tX2G3Mjg6N_P'
EMAIL_HOST_PASSWORD = 'tPHOJ.fzvK.ZEC.;R#;|'
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%jq+tdb&qkl+4=wcl71hn&u+%8_$^mjp7mt6cr*u@l_-zjouf#'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "admin",
        'USER': "admin",
        'PASSWORD': "admin",
        "HOST": "paris-reinforce.epu.ntua.gr",
        "PORT": "5435"
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
