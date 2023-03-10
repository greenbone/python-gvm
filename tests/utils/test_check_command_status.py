# -*- coding: utf-8 -*-
# Copyright (C) 2021-2022 Greenbone AG
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

from gvm.utils import check_command_status


class TestCheckCommandStatus(unittest.TestCase):
    def test_check_command_status_empty(self):
        with self.assertLogs("gvm.utils", level="ERROR") as error_logger:
            false = check_command_status(xml=False)
            self.assertFalse(false)

            false = check_command_status(xml=0)
            self.assertFalse(false)
        self.assertEqual(
            error_logger.output,
            [
                "ERROR:gvm.utils:XML Command is empty.",
                "ERROR:gvm.utils:XML Command is empty.",
            ],
        )

    def test_check_command_status_failed(self):
        response = (
            '<authenticatio status="400" ><asaaa<fsd'
            'fsn_response status_text="Auth failed"/>'
        )
        with self.assertLogs("gvm.utils", level="ERROR") as error_logger:
            self.assertFalse(check_command_status(xml=response))
        self.assertEqual(
            error_logger.output,
            [
                "ERROR:gvm.utils:etree.XML(xml): error parsing attribute name, "
                "line 1, column 36 (<string>, line 1)"
            ],
        )

    def test_check_command_status_error(self):
        response = "<a><b/></a>"
        with self.assertLogs("gvm.utils", level="ERROR") as error_logger:
            self.assertFalse(check_command_status(xml=response))
        self.assertEqual(
            error_logger.output,
            [
                "ERROR:gvm.utils:Not received an "
                "status code within the response."
            ],
        )

    def test_check_command_status(self):
        response = (
            '<authentication status="200" status_text="Auth successfully"/>'
        )
        self.assertTrue(check_command_status(xml=response))


if __name__ == "__main__":
    unittest.main()
