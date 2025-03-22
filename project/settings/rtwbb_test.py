from .base import *  # noqa


RTWBB_FRONTEND_APP_BASE_URL = os.getenv(
    "RTWBB_FRONTEND_APP_BASE_URL",
    "https://rtwbb-test.dopracenakole.net/#/",
)

ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = RTWBB_FRONTEND_APP_BASE_URL

ACCOUNT_EMAIL_CONFIRMATION_URL = f"{RTWBB_FRONTEND_APP_BASE_URL}confirm-email"
ACCOUNT_RESET_PASSWORD_CONFIRMATION_URL = f"{RTWBB_FRONTEND_APP_BASE_URL}reset-password"
ACCOUNT_ADAPTER = "dpnk.allauth.AccountAdapter"
SOCIALACCOUNT_ADAPTER = "dpnk.allauth.SocialAccountAdapter"

REST_AUTH["PASSWORD_RESET_SERIALIZER"] = "dpnk.allauth.UserPasswordResetSerializer"

CORS_ORIGIN_REGEX.append(RTWBB_FRONTEND_APP_BASE_URL.rstrip("/#/"))
