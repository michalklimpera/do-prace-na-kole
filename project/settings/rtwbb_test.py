from .base import *  # noqa


CORS_ALLOW_ALL_ORIGINS = True

RTWBB_FRONTEND_APP_BASE_URL = os.getenv(
    "RTWBB_FRONTEND_APP_BASE_URL",
    "https://rtwbb-test.dopracenakole.net/#/",
)

ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = RTWBB_FRONTEND_APP_BASE_URL

ACCOUNT_EMAIL_CONFIRMATION_URL = f"{RTWBB_FRONTEND_APP_BASE_URL}confirm-email"
ACCOUNT_RESET_PASSWORD_CONFIRMATION_URL = f"{RTWBB_FRONTEND_APP_BASE_URL}reset-password"
ACCOUNT_ADAPTER = "dpnk.allauth.AccountAdapter"

REST_AUTH["PASSWORD_RESET_SERIALIZER"] = "dpnk.allauth.UserPasswordResetSerializer"

SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = (
    True
    if os.getenv("SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT", False) == "True"
    else False
)

CORS_ORIGIN_REGEX.append("https://rtwbb-test.dopracenakole.net")
