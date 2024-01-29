# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCreatePolicyTestMixin:
    def test_create_policy(self):
        self.gmp.create_policy("foo")

        self.connection.send.has_been_called_with(
            "<create_config>"
            "<copy>085569ce-73ed-11df-83c3-002264764cea</copy>"
            "<name>foo</name>"
            "<usage_type>policy</usage_type>"
            "</create_config>"
        )

    def test_create_with_policy_id_and_comment(self):
        self.gmp.create_policy("foo", policy_id="p1", comment="foo")

        self.connection.send.has_been_called_with(
            "<create_config>"
            "<comment>foo</comment>"
            "<copy>p1</copy>"
            "<name>foo</name>"
            "<usage_type>policy</usage_type>"
            "</create_config>"
        )

    def test_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_policy(policy_id="c1", name=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.create_policy(policy_id="c1", name="")
