# -*- coding: utf-8 -*-

# Author: Petr Dlouhý <petr.dlouhy@auto-mat.cz>
#
# Copyright (C) 2015 o.s. Auto*Mat
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
from django.test import TestCase, RequestFactory, TransactionTestCase, Client
from django.core.urlresolvers import reverse
from django.core import mail
from django.test.utils import override_settings
from dpnk import results, models, mailing, views
from dpnk.models import Competition, Team, UserAttendance, Campaign, User, UserProfile
import datetime
import django
from django_admin_smoke_tests import tests
from model_mommy import mommy
import createsend
from unittest.mock import MagicMock, patch


@override_settings(
    SITE_ID=2,
    FAKE_DATE=datetime.date(year=2010, month=11, day=20),
)
class AdminTest(tests.AdminSiteSmokeTest):
    fixtures = ['campaign', 'views', 'users', 'test_results_data', 'transactions', 'batches']

    def get_request(self):
        request = super().get_request()
        request.subdomain = "testing-campaign"
        return request


@override_settings(
    SITE_ID=2,
    FAKE_DATE=datetime.date(year=2010, month=11, day=20),
)
class ViewsTests(TransactionTestCase):
    fixtures = ['campaign', 'views', 'users']

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.client = Client(HTTP_HOST="testing-campaign.testserver")

    def test_admin_views_competition(self):
        self.assertTrue(self.client.login(username='admin', password='admin'))
        response = self.client.get(reverse("admin:dpnk_competition_add"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="id_competitor_type"')

        response = self.client.get(reverse("admin:dpnk_competition_change", args=[3]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="id_competitor_type"')

    def test_dpnk_views_no_login(self):
        address = reverse('registrace')
        response = self.client.get(address)
        self.assertEqual(response.status_code, 200)

    def test_dpnk_registration(self):
        address = reverse('registrace')
        post_data = {
            'email': 'test1@test.cz',
            'password1': 'test11',
            'password2': 'test11',
        }
        response = self.client.post(address, post_data)
        self.assertRedirects(response, reverse('upravit_profil'))
        user = User.objects.get(email='test1@test.cz')
        self.assertNotEquals(user, None)
        self.assertNotEquals(UserProfile.objects.get(user=user), None)
        self.assertNotEquals(UserAttendance.objects.get(userprofile__user=user), None)

    def test_password_recovery(self):
        address = reverse('password_reset')
        post_data = {
            'email': 'test@test.cz',
        }
        response = self.client.post(address, post_data)
        self.assertRedirects(response, reverse('password_reset_done'))
        msg = mail.outbox[0]
        self.assertEqual(msg.recipients(), ['test@test.cz'])
        self.assertEqual(msg.subject, 'Zapomenuté heslo Do práce na kole')
        self.assertTrue('http://testing-campaign.testserver/cs/zapomenute_heslo/zmena/' in msg.body)

    @override_settings(
        FAKE_DATE=datetime.date(year=2010, month=10, day=1),
    )
    def test_dpnk_registration_out_of_phase(self):
        address = reverse('registrace')
        response = self.client.get(address)
        self.assertEqual(response.status_message, "out_of_phase")
        self.assertEqual(response.status_code, 403)

    def test_dpnk_mailing_list(self):
        user_attendance = UserAttendance.objects.get(userprofile__user__username='test')
        user_attendance.campaign.mailing_list_enabled = True
        user_attendance.campaign.save()
        ret_mailing_id = "344ass"
        createsend.Subscriber.add = MagicMock(return_value=ret_mailing_id)
        mailing.add_or_update_user_synchronous(user_attendance)
        createsend.Subscriber.add.assert_called_with(
            '12345abcde', 'test@test.cz', 'Testing User 1',
            [
                {'Key': 'Mesto', 'Value': None}, {'Key': 'Firemni_spravce', 'Value': True},
                {'Key': 'Stav_platby', 'Value': None}, {'Key': 'Aktivni', 'Value': True},
                {'Key': 'Novacek', 'Value': None}, {'Key': 'Kampan', 'Value': 'Testing campaign'},
                {'Key': 'Vstoupil_do_souteze', 'Value': None}, {'Key': 'Pocet_lidi_v_tymu', 'Value': None}
            ],
            True
        )
        self.assertEqual(user_attendance.userprofile.mailing_id, ret_mailing_id)


@override_settings(
    SITE_ID=2,
    FAKE_DATE=datetime.date(year=2010, month=11, day=20),
)
class ViewsTestsLogon(TransactionTestCase):
    fixtures = ['campaign', 'views', 'users', 'transactions', 'batches']

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.client = Client(HTTP_HOST="testing-campaign.testserver")
        self.assertTrue(self.client.login(username='test', password='test'))

    def test_dpnk_team_view(self):
        response = self.client.get(reverse('zmenit_tym'))
        self.assertContains(response, "Testing company")
        self.assertContains(response, "Testing team 1")

    @patch('http.client.HTTPSConnection.getresponse')
    def test_dpnk_payment_status_view(self, payu_response):
        post_data = {
            'pos_id': '2075-1',
            'session_id': '2075-1J1455206433',
            'ts': '1',
            'sig': 'd8122ef998935e2571402d7d73843054',
        }
        payu_response.return_value.read.return_value = \
            b"trans_sig: d8122ef998935e2571402d7d73843054\n"\
            b"trans_pos_id: d8122ef998935e2571402d7d73843054\n"\
            b"trans_session_id: d8122ef998935e2571402d7d73843054\n"\
            b"trans_status: d8122ef998935e2571402d7d73843054\n"\
            b"trans_amount: d8122ef998935e2571402d7d73843054\n"\
            b"trans_desc: d8122ef998935e2571402d7d73843054\n"\
            b"trans_ts: d8122ef998935e2571402d7d73843054\n"\
            b"trans_order_id: d8122ef998935e2571402d7d73843054"
        response = self.client.post(reverse('payment_status'), post_data)
        self.assertRedirects(response, reverse("zmenit_triko"))

    def test_dpnk_team_view_choose(self):
        post_data = {
            'company': '1',
            'subsidiary': '1',
            'team': '1',
            'next': 'Next',
        }
        response = self.client.post(reverse('zmenit_tym'), post_data)
        self.assertRedirects(response, reverse("zmenit_triko"))

    def test_dpnk_team_view_create(self):
        post_data = {
            'company-name': 'Created company',
            'id_company_selected': 'on',
            'subsidiary-city': '1',
            'subsidiary-address_recipient': 'Created name',
            'subsidiary-address_street': 'Created street',
            'subsidiary-address_street_number': '99',
            'subsidiary-address_psc': '99 999',
            'subsidiary-address_city': 'Testing city',
            'id_subsidiary_selected': 'on',
            'team-name': 'Created team',
            'company': '1',
            'subsidiary': '1',
            'team-campaign': '339',
            'id_team_selected': 'on',
            'next': 'Další',
        }
        response = self.client.post(reverse('zmenit_tym'), post_data, follow=True)

        self.assertRedirects(response, reverse("pozvanky"))
        self.assertContains(response, "Tým Created team úspěšně vytvořen")
        user = UserAttendance.objects.get(pk=1115)
        self.assertEquals(user.team.name, "Created team")
        self.assertEquals(user.team.subsidiary.address.street, "Created street")
        self.assertEquals(user.team.subsidiary.company.name, "Created company")

    def test_dpnk_team_view_no_team_set(self):
        post_data = {
            'company': '1',
            'subsidiary': '',
            'team': '',
            'next': 'Next',
        }
        response = self.client.post(reverse('zmenit_tym'), post_data)
        self.assertContains(response, 'error_1_id_team')
        self.assertContains(response, 'var value = undefined;')

    def test_dpnk_views_gpx_file(self):
        user_attendance = UserAttendance.objects.get(userprofile__user__username='test')
        mommy.make(models.Trip, user_attendance=user_attendance, date=datetime.date(year=2010, month=11, day=20))
        gpxfile = mommy.make(models.GpxFile, user_attendance=user_attendance, trip_date=datetime.date(year=2010, month=11, day=20))

        address = reverse('gpx_file', kwargs={"id": gpxfile.pk})
        response = self.client.get(address)
        self.assertEqual(response.status_code, 200)

    def verify_views(self, views, status_code_map):
        for view in views:
            status_code = status_code_map[view] if view in status_code_map else 200
            address = view
            response = self.client.get(address, follow=True)
            filename = view.replace("/", "_")
            if response.status_code != status_code:
                with open("error_%s.html" % filename, "w") as f:
                    f.write(response.content.decode())
            self.assertEqual(response.status_code, status_code, "%s view failed, the failed page is saved to error_%s.html file." % (view, filename))

    views = [
        reverse('profil'),
        reverse('zmenit_tym'),
        reverse('upravit_trasu'),
        reverse('upravit_profil'),
        reverse('zmenit_triko'),
        reverse('working_schedule'),
        reverse('company_admin_pay_for_users'),
        reverse('invoices'),
        reverse('edit_company'),
        reverse('company_admin_competitions'),
        reverse('company_structure'),
        reverse('company_admin_competition'),
        reverse('company_admin_application'),
        reverse('emission_calculator'),
        reverse('package'),
        reverse('platba'),
        reverse('typ_platby'),
        reverse('zmenit_triko'),
        reverse('upravit_trasu'),
        reverse('working_schedule'),
        reverse('competitions'),
        reverse('jizdy'),
        reverse('other_team_members_results'),
        reverse('team_members'),
        reverse('zaslat_zadost_clenstvi'),
        reverse('pozvanky'),
        reverse('registration_access'),
        reverse('registrace'),
        reverse('edit_team'),
        reverse('questionnaire', kwargs={'questionnaire_slug': 'quest'}),
        reverse('edit_subsidiary', kwargs={'pk': 1}),
        'error404.txt',
        reverse(views.daily_distance_json),
        reverse(views.daily_chart),
        reverse(views.statistics, kwargs={'variable': 'ujeta-vzdalenost'}),
        reverse(views.statistics, kwargs={'variable': 'ujeta-vzdalenost-dnes'}),
        reverse(views.statistics, kwargs={'variable': 'pocet-cest'}),
        reverse(views.statistics, kwargs={'variable': 'pocet-cest-dnes'}),
        reverse(views.statistics, kwargs={'variable': 'pocet-zaplacenych'}),
        reverse(views.statistics, kwargs={'variable': 'pocet-prihlasenych'}),
        reverse(views.statistics, kwargs={'variable': 'pocet-soutezicich'}),
        reverse(views.statistics, kwargs={'variable': 'pocet-spolecnosti'}),
        reverse(views.statistics, kwargs={'variable': 'pocet-pobocek'}),
        reverse(views.statistics, kwargs={'variable': 'pocet-soutezicich-firma'}),
    ]

    def test_dpnk_views(self):
        """
        test if the user pages work
        """
        status_code_map = {
            reverse('profil'): 200,
            reverse('registration_access'): 200,
            reverse('jizdy'): 403,
            'error404.txt': 404,
        }

        self.verify_views(self.views, status_code_map)

    def test_dpnk_views_registered(self):
        """
        test if the user pages work after user registration
        """
        user_attendance = UserAttendance.objects.get(userprofile__user__username='test')
        user_attendance.track = 'LINESTRING(0 0,-1 1)'
        user_attendance.t_shirt_size = mommy.make(models.TShirtSize)
        team = Team.objects.get(id=1)
        user_attendance.team = team
        mommy.make(models.Payment, user_attendance=user_attendance, amount=160, status=99)
        user_attendance.save()

        status_code_map = {
            reverse('profil'): 200,
            reverse('registration_access'): 200,
            reverse('typ_platby'): 403,
            'error404.txt': 404,
        }

        self.verify_views(self.views, status_code_map)


class TestTeams(TestCase):
    fixtures = ['campaign', 'users']

    def test_member_count_update(self):
        team = Team.objects.get(id=1)
        team.autoset_member_count()  # TODO: remove this once the signals in tests are repaired
        self.assertEqual(team.member_count, 2)
        campaign = Campaign.objects.get(pk=339)
        user = User.objects.create(first_name="Third", last_name="User", username="third_user")
        userprofile = UserProfile.objects.create(user=user)
        UserAttendance.objects.create(team=team, campaign=campaign, userprofile=userprofile, approved_for_team='approved')
        team.autoset_member_count()  # TODO: remove this once the signals in tests are repaired
        self.assertEqual(team.member_count, 3)


class ResultsTests(TestCase):
    fixtures = ['users', 'campaign', 'test_results_data']

    def test_get_competitors(self):
        team = Team.objects.get(id=1)
        team.autoset_member_count()  # TODO: remove this once the signals in tests are repaired
        query = results.get_competitors(Competition.objects.get(id=0))
        self.assertListEqual(list(query.all()), [team])


class RunChecksTestCase(TestCase):
    def test_checks(self):
        django.setup()
        from django.core import checks
        all_issues = checks.run_checks()
        errors = [str(e) for e in all_issues if e.level >= checks.ERROR]
        if errors:
            self.fail('checks failed:\n' + '\n'.join(errors))