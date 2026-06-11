#  SPDX-FileCopyrightText: 2026 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetWebApplicationTargetsTestMixin:
    def test_get_targets(self):
        self.gmp.get_web_application_targets()

        self.connection.send.has_been_called_with(
            b"<get_web_application_targets/>"
        )

    def test_get_targets_with_filter_string(self):
        self.gmp.get_web_application_targets(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_web_application_targets filter="foo=bar"/>'
        )

    def test_get_targets_with_filter_id(self):
        self.gmp.get_web_application_targets(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_web_application_targets filt_id="f1"/>'
        )

    def test_get_targets_with_trash(self):
        self.gmp.get_web_application_targets(trash=True)

        self.connection.send.has_been_called_with(
            b'<get_web_application_targets trash="1"/>'
        )

        self.gmp.get_web_application_targets(trash=False)

        self.connection.send.has_been_called_with(
            b'<get_web_application_targets trash="0"/>'
        )

    def test_get_targets_with_tasks(self):
        self.gmp.get_web_application_targets(tasks=True)

        self.connection.send.has_been_called_with(
            b'<get_web_application_targets tasks="1"/>'
        )

        self.gmp.get_web_application_targets(tasks=False)

        self.connection.send.has_been_called_with(
            b'<get_web_application_targets tasks="0"/>'
        )
