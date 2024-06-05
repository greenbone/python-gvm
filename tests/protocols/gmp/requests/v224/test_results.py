# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import RequiredArgument
from gvm.protocols.gmp.requests.v224 import Results


class ResultsTestCase(unittest.TestCase):
    def test_get_result(self):
        request = Results.get_result("result_id")
        self.assertEqual(
            bytes(request),
            b'<get_results result_id="result_id" details="1"/>',
        )

    def test_get_result_missing_result_id(self):
        with self.assertRaises(RequiredArgument):
            Results.get_result(None)

        with self.assertRaises(RequiredArgument):
            Results.get_result("")

    def test_get_results(self):
        request = Results.get_results()
        self.assertEqual(
            bytes(request),
            b"<get_results/>",
        )

    def test_get_results_with_filter_string(self):
        request = Results.get_results(filter_string="filter_string")
        self.assertEqual(
            bytes(request),
            b'<get_results filter="filter_string"/>',
        )

    def test_get_results_with_filter_id(self):
        request = Results.get_results(filter_id="filter_id")
        self.assertEqual(
            bytes(request),
            b'<get_results filt_id="filter_id"/>',
        )

    def test_get_results_with_task_id(self):
        request = Results.get_results(task_id="task_id")
        self.assertEqual(
            bytes(request),
            b'<get_results task_id="task_id"/>',
        )

    def test_get_results_with_note_details(self):
        request = Results.get_results(note_details=True)
        self.assertEqual(
            bytes(request),
            b'<get_results note_details="1"/>',
        )

        request = Results.get_results(note_details=False)
        self.assertEqual(
            bytes(request),
            b'<get_results note_details="0"/>',
        )

    def test_get_results_with_override_details(self):
        request = Results.get_results(override_details=True)
        self.assertEqual(
            bytes(request),
            b'<get_results override_details="1"/>',
        )

        request = Results.get_results(override_details=False)
        self.assertEqual(
            bytes(request),
            b'<get_results override_details="0"/>',
        )

    def test_get_results_with_details(self):
        request = Results.get_results(details=True)
        self.assertEqual(
            bytes(request),
            b'<get_results details="1"/>',
        )

        request = Results.get_results(details=False)
        self.assertEqual(
            bytes(request),
            b'<get_results details="0"/>',
        )
