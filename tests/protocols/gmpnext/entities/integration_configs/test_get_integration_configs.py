#  SPDX-FileCopyrightText: 2026 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetIntegrationConfigsTestMixin:
    def test_get_integration_configs(self):
        self.gmp.get_integration_configs()

        self.connection.send.has_been_called_with(b"<get_integration_configs/>")

    def test_get_integration_configs_with_filter_string(self):
        self.gmp.get_integration_configs(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_integration_configs filter="foo=bar"/>'
        )

    def test_get_integration_configs_with_filter_id(self):
        self.gmp.get_integration_configs(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_integration_configs filt_id="f1"/>'
        )
