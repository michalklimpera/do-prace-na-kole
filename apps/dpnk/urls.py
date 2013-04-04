from django.conf.urls.defaults import patterns, include, url

from django.conf import settings
from views import *

urlpatterns = patterns('',
    url(r'^registrace/$', 
        register,
        {'success_url': 'typ_platby'}),
    url(r'^registrace/(?P<token>[0-9A-Za-z]+)/(?P<initial_email>[^&]+)/$$',
        register,
        {'success_url': 'typ_platby'}),
    url(r'^pozvanky/$',
        invite,
        {'success_url': 'typ_platby'}),
    url(r'^zaslat_zadost_clenstvi/$',
        team_approval_request),
    url(r'^login/$',
        login),
    url(r'^zmena_hesla/$',
        'django.contrib.auth.views.password_change'),
    url(r'^zmena_hesla_hotovo/$',
        'django.contrib.auth.views.password_change_done'),
    url(r'^profil/$',
        profile),
    url(r'^jizdy/$',
        rides),
    url(r'^profil_pristup/$',
        profile_access),
    url(r'^team_admin_team/$',
        team_admin_team,
        {'success_url': 'profil'}),
    url(r'^team_admin_members/$',
        team_admin_members,
        ),
    url(r'^vysledky_zavodnika/(?P<username>[0-9A-Za-z_\-]+)/$',
        results_user,
        {'template': 'registration/results_user.html'}),
    url(r'^vysledky_zavodnika/(?P<username>[0-9A-Za-z_\-]+)/(?P<limit>[0-9]+)/$',
        results_user,
        {'template': 'registration/results_user.html'}),
    url(r'^vysledky_souteze/(?P<competition_slug>[0-9A-Za-z_\-]+)/$',
        competition_results,
        {'template': 'registration/competition_results.html'}),
    url(r'^vysledky_souteze/(?P<competition_slug>[0-9A-Za-z_\-]+)/(?P<limit>[0-9]+)/$',
        competition_results,
        {'template': 'registration/competition_results.html'}),
    url(r'^vysledky/$',
        results,
        {'template': 'registration/results'}),
    url(r'^kratke_vysledky/$',
        results,
        {'template': 'registration/results_short'}),
    url(r'^otazka/$',
        questionaire),
    url(r'^cyklozamestnavatel_roku/$', questionaire,
        {'template': 'registration/company_survey'}),
    url(r'^upravit_profil/$',
        update_profile),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': settings.LOGOUT_NEXT_PAGE}
        ),
    url(r'^typ_platby/$',
        payment_type),
    url(r'^platba/$',
        payment),
    url(r'^platba_uspesna/(?P<trans_id>[0-9]+)/(?P<session_id>[0-9A-Za-z\-]+)/(?P<pay_type>[0-9A-Za-z]+)/$$',
        payment_result,
        {'success': True}),
    url(r'^platba_neuspesna/(?P<trans_id>[0-9]+)/(?P<session_id>[0-9A-Za-z\-]+)/(?P<pay_type>[0-9A-Za-z]+)/(?P<error>[^&]+)/$$',
        payment_result,
        {'success': False}),
    url(r'^platba_status$',
        payment_status),
    url(r'^zapomenute_heslo/$',
        'django.contrib.auth.views.password_reset'),
    url(r'^zapomenute_heslo/odeslano/$',
        'django.contrib.auth.views.password_reset_done'),
    url(r'^zapomenute_heslo/zmena/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$$',
        'django.contrib.auth.views.password_reset_confirm'),
    url(r'^zapomenute_heslo/dokonceno/$',
        'django.contrib.auth.views.password_reset_complete'),
    url(r'^otazky/$',
        questions),
    url(r'^cyklozamestnavatel_firmy/$',
        company_survey),
    url(r'^cyklozamestnavatel_odpovedi/$',
        company_survey_answers),
    url(r'^odpovedi/$',
        answers),
    url(r'^facebook_app/$',
        facebook_app),
)
