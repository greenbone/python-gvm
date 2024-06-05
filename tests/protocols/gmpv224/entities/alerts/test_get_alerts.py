# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetAlertsTestMixin:
    def test_get_alerts(self):
        self.gmp.get_alerts()

        self.connection.send.has_been_called_with(b"<get_alerts/>")

    def test_get_alerts_with_trash(self):
        self.gmp.get_alerts(trash=True)

        self.connection.send.has_been_called_with(b'<get_alerts trash="1"/>')

        self.gmp.get_alerts(trash=False)

        self.connection.send.has_been_called_with(b'<get_alerts trash="0"/>')

    def test_get_alerts_with_filter_string(self):
        self.gmp.get_alerts(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_alerts filter="foo=bar"/>'
        )

    def test_get_alerts_with_filter_id(self):
        self.gmp.get_alerts(filter_id="f1")

        self.connection.send.has_been_called_with(b'<get_alerts filt_id="f1"/>')

    def test_get_alerts_with_tasks(self):
        self.gmp.get_alerts(tasks=True)

        self.connection.send.has_been_called_with(b'<get_alerts tasks="1"/>')

        self.gmp.get_alerts(tasks=False)

        self.connection.send.has_been_called_with(b'<get_alerts tasks="0"/>')
