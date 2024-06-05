# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetAlertTestMixin:
    def test_get_alert(self):
        self.gmp.get_alert("a1")

        self.connection.send.has_been_called_with(
            b'<get_alerts alert_id="a1"/>'
        )

        self.gmp.get_alert(alert_id="a1")

        self.connection.send.has_been_called_with(
            b'<get_alerts alert_id="a1"/>'
        )

    def test_get_alert_invalid_alert_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_alert(alert_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_alert(alert_id="")

    def test_get_alert_with_tasks(self):
        self.gmp.get_alert(alert_id="a1", tasks=True)

        self.connection.send.has_been_called_with(
            b'<get_alerts alert_id="a1" tasks="1"/>'
        )

        self.gmp.get_alert(alert_id="a1", tasks=False)

        self.connection.send.has_been_called_with(
            b'<get_alerts alert_id="a1" tasks="0"/>'
        )
