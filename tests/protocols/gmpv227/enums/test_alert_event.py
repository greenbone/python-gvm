# SPDX-FileCopyrightText: 2023-2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmp.requests.v227 import AlertEvent


class GetAlertEventFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            AlertEvent.from_string("foo")

    def test_none_or_empty(self):
        ct = AlertEvent.from_string(None)
        self.assertIsNone(ct)
        ct = AlertEvent.from_string("")
        self.assertIsNone(ct)

    def test_task_run_status_changed(self):
        ct = AlertEvent.from_string("Task run status changed")
        self.assertEqual(ct, AlertEvent.TASK_RUN_STATUS_CHANGED)

    def test_new_secinfo_arrived(self):
        ct = AlertEvent.from_string("New SecInfo arrived")
        self.assertEqual(ct, AlertEvent.NEW_SECINFO_ARRIVED)

    def test_updated_secinfo_arrived(self):
        ct = AlertEvent.from_string("Updated SecInfo arrived")
        self.assertEqual(ct, AlertEvent.UPDATED_SECINFO_ARRIVED)

    def test_ticket_received(self):
        ct = AlertEvent.from_string("ticket received")
        self.assertEqual(ct, AlertEvent.TICKET_RECEIVED)

    def test_assigned_ticket_changed(self):
        ct = AlertEvent.from_string("assigned ticket changed")
        self.assertEqual(ct, AlertEvent.ASSIGNED_TICKET_CHANGED)

    def test_owned_ticket_changed(self):
        ct = AlertEvent.from_string("owned ticket changed")
        self.assertEqual(ct, AlertEvent.OWNED_TICKET_CHANGED)
