# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

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
                "ERROR:gvm.utils:Error while parsing the command status: Invalid XML "
                '\'<authenticatio status="400" ><asaaa<fsdfsn_response status_text="Auth '
                "failed\"/>'. Error was error parsing attribute name, line 1, column 36 "
                "(<string>, line 1)"
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
