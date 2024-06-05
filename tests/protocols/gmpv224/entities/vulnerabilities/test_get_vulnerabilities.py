# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetVulnerabilitiesTestMixin:
    def test_get_vulnerabilities(self):
        self.gmp.get_vulnerabilities()

        self.connection.send.has_been_called_with(b"<get_vulns/>")

    def test_get_vulnerabilities_with_filter_string(self):
        self.gmp.get_vulnerabilities(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_vulns filter="foo=bar"/>'
        )

    def test_get_vulnerabilities_with_filter_id(self):
        self.gmp.get_vulnerabilities(filter_id="f1")

        self.connection.send.has_been_called_with(b'<get_vulns filt_id="f1"/>')
