# -*- coding: utf-8 -*-

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


from django.apps import AppConfig


class DPNKConfig(AppConfig):
    name = "dpnk"
    verbose_name = "Do práce na kole"

    def ready(self):

        from . import models as dpnk_models
        from fieldsignals import post_save_changed, pre_save_changed
        from django.conf import settings

        if not settings.DATABASE_CONFIGURED:
            return

        post_save_changed.connect(
            dpnk_models.change_invoice_payments_status,
            sender=dpnk_models.Invoice,
            fields=["paid_date"],
        )
        pre_save_changed.connect(
            dpnk_models.pre_user_team_changed,
            sender=dpnk_models.UserAttendance,
            fields=["team", "team_id"],
        )
        post_save_changed.connect(
            dpnk_models.post_user_team_changed,
            sender=dpnk_models.UserAttendance,
            fields=["team", "team_id"],
        )
