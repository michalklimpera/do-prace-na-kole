# -*- coding: utf-8 -*-

# Author: Hynek Hanke <hynek.hanke@auto-mat.cz>
# Author: Petr Dlouhý <petr.dlouhy@email.cz>
#
# Copyright (C) 2016 o.s. Auto*Mat
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

"""Import all models."""
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .address import Address, get_address_string
from .campaign import Campaign
from .city import City
from .city_in_campaign import CityInCampaign
from .company import Company
from .company_admin import CompanyAdmin
from .competition import Competition, CompetitionForm
from .competition_result import CompetitionResult
from .delivery_batch import DeliveryBatch
from .discount_coupon import DiscountCoupon, DiscountCouponType
from .gpxfile import GpxFile, normalize_gpx_filename
from .invoice import Invoice, change_invoice_payments_status, payments_to_invoice
from .phase import Phase
from .questionnaire import Answer, Choice, ChoiceType, Question, QuestionForm, questionnaire_filename
from .subsidiary import Subsidiary
from .t_shirt_size import TShirtSize
from .team import Team, post_user_team_changed, pre_user_team_changed, validate_length
from .transactions import CommonTransaction, PackageTransaction, Payment, STATUS, Status, Transaction, UserActionTransaction
from .trip import Trip
from .user_attendance import UserAttendance
from .user_profile import UserProfile
from .voucher import Voucher

from .. import mailing

__all__ = (
    Address,
    Campaign,
    CityInCampaign,
    City,
    CompanyAdmin,
    Company,
    Competition,
    CompetitionForm,
    CompetitionResult,
    DeliveryBatch,
    DiscountCoupon,
    DiscountCouponType,
    GpxFile,
    Invoice,
    Phase,
    ChoiceType,
    QuestionForm,
    Question,
    Choice,
    Answer,
    Subsidiary,
    Team,
    Transaction,
    PackageTransaction,
    CommonTransaction,
    Payment,
    UserActionTransaction,
    Trip,
    TShirtSize,
    UserAttendance,
    UserProfile,
    Voucher,
    change_invoice_payments_status,
    pre_user_team_changed,
    post_user_team_changed,
    questionnaire_filename,
    normalize_gpx_filename,
    get_address_string,
    validate_length,
    STATUS,
    Status,
    payments_to_invoice,
)


@receiver(post_save, sender=User)
def update_mailing_user(sender, instance, created, **kwargs):
    try:
        for user_attendance in instance.userprofile.userattendance_set.all():
            if not kwargs.get('raw', False) and user_attendance.campaign:
                mailing.add_or_update_user(user_attendance)
    except UserProfile.DoesNotExist:
        pass


def set_track(sender, instance, changed_fields=None, **kwargs):
    if hasattr(instance, 'track_clean'):
        instance.track = instance.track_clean