# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCreatePolicyTestMixin:
    def test_create_policy(self):
        self.gmp.create_policy("foo")

        self.connection.send.has_been_called_with(
            b"<create_config>"
            b"<copy>085569ce-73ed-11df-83c3-002264764cea</copy>"
            b"<name>foo</name>"
            b"<usage_type>policy</usage_type>"
            b"</create_config>"
        )

    def test_create_with_policy_id_and_comment(self):
        self.gmp.create_policy("foo", policy_id="p1", comment="foo")

        self.connection.send.has_been_called_with(
            b"<create_config>"
            b"<comment>foo</comment>"
            b"<copy>p1</copy>"
            b"<name>foo</name>"
            b"<usage_type>policy</usage_type>"
            b"</create_config>"
        )

    def test_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_policy(policy_id="c1", name=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.create_policy(policy_id="c1", name="")
