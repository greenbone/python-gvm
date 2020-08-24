# -*- coding: utf-8 -*-
# Copyright (C) 2019 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmpv9 import AlertEvent, get_alert_event_from_string


class GetAlertEventFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            get_alert_event_from_string('foo')

    def test_none_or_empty(self):
        ct = get_alert_event_from_string(None)
        self.assertIsNone(ct)
        ct = get_alert_event_from_string('')
        self.assertIsNone(ct)

    def test_task_run_status_changed(self):
        ct = get_alert_event_from_string('Task run status changed')
        self.assertEqual(ct, AlertEvent.TASK_RUN_STATUS_CHANGED)

    def test_new_secinfo_arrived(self):
        ct = get_alert_event_from_string('New SecInfo arrived')
        self.assertEqual(ct, AlertEvent.NEW_SECINFO_ARRIVED)

    def test_updated_secinfo_arrived(self):
        ct = get_alert_event_from_string('Updated SecInfo arrived')
        self.assertEqual(ct, AlertEvent.UPDATED_SECINFO_ARRIVED)

    def test_ticket_received(self):
        ct = get_alert_event_from_string('ticket received')
        self.assertEqual(ct, AlertEvent.TICKET_RECEIVED)

    def test_assigned_ticket_changed(self):
        ct = get_alert_event_from_string('assigned ticket changed')
        self.assertEqual(ct, AlertEvent.ASSIGNED_TICKET_CHANGED)

    def test_owned_ticket_changed(self):
        ct = get_alert_event_from_string('owned ticket changed')
        self.assertEqual(ct, AlertEvent.OWNED_TICKET_CHANGED)


if __name__ == '__main__':
    unittest.main()
