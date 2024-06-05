# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetPoliciesTestMixin:
    def test_get_policies_simple(self):
        self.gmp.get_policies()

        self.connection.send.has_been_called_with(
            b'<get_configs usage_type="policy"/>'
        )

    def test_get_policies_with_filter_string(self):
        self.gmp.get_policies(filter_string="name=foo")

        self.connection.send.has_been_called_with(
            b'<get_configs usage_type="policy" filter="name=foo"/>'
        )

    def test_get_policies_with_filter_id(self):
        self.gmp.get_policies(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_configs usage_type="policy" filt_id="f1"/>'
        )

    def test_get_policies_from_trash(self):
        self.gmp.get_policies(trash=True)

        self.connection.send.has_been_called_with(
            b'<get_configs usage_type="policy" trash="1"/>'
        )

    def test_get_policies_with_details(self):
        self.gmp.get_policies(details=True)

        self.connection.send.has_been_called_with(
            b'<get_configs usage_type="policy" details="1"/>'
        )

    def test_get_policies_without_details(self):
        self.gmp.get_policies(details=False)

        self.connection.send.has_been_called_with(
            b'<get_configs usage_type="policy" details="0"/>'
        )

    def test_get_policies_with_families(self):
        self.gmp.get_policies(families=True)

        self.connection.send.has_been_called_with(
            b'<get_configs usage_type="policy" families="1"/>'
        )

    def test_get_policies_without_families(self):
        self.gmp.get_policies(families=False)

        self.connection.send.has_been_called_with(
            b'<get_configs usage_type="policy" families="0"/>'
        )

    def test_get_policies_with_preferences(self):
        self.gmp.get_policies(preferences=True)

        self.connection.send.has_been_called_with(
            b'<get_configs usage_type="policy" preferences="1"/>'
        )

    def test_get_policies_without_preferences(self):
        self.gmp.get_policies(preferences=False)

        self.connection.send.has_been_called_with(
            b'<get_configs usage_type="policy" preferences="0"/>'
        )

    def test_get_policies_with_audits(self):
        self.gmp.get_policies(audits=True)

        self.connection.send.has_been_called_with(
            b'<get_configs usage_type="policy" tasks="1"/>'
        )

    def test_get_policies_without_audits(self):
        self.gmp.get_policies(audits=False)

        self.connection.send.has_been_called_with(
            b'<get_configs usage_type="policy" tasks="0"/>'
        )
