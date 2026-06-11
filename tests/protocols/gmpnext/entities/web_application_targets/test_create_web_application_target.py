#  SPDX-FileCopyrightText: 2026 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCreateWebApplicationTargetTestMixin:
    def test_create_target_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_web_application_target(
                None, urls=["https://example.com"]
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_web_application_target(
                name=None, urls=["https://example.com"]
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_web_application_target(
                "", urls=["https://example.com"]
            )

    def test_create_target_missing_urls(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_web_application_target(name="foo", urls=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.create_web_application_target(name="foo", urls=[])

    def test_create_target_with_comment(self):
        self.gmp.create_web_application_target(
            "foo", urls=["https://example.com"], comment="bar"
        )

        self.connection.send.has_been_called_with(
            b"<create_web_application_target>"
            b"<name>foo</name>"
            b"<urls>https://example.com</urls>"
            b"<comment>bar</comment>"
            b"</create_web_application_target>"
        )

    def test_create_target_with_exclude_urls(self):
        self.gmp.create_web_application_target(
            "foo",
            urls=["https://example.com"],
            exclude_urls=["https://example.com/logout"],
        )

        self.connection.send.has_been_called_with(
            b"<create_web_application_target>"
            b"<name>foo</name>"
            b"<urls>https://example.com</urls>"
            b"<exclude_urls>https://example.com/logout</exclude_urls>"
            b"</create_web_application_target>"
        )

    def test_create_target_with_multiple_urls(self):
        self.gmp.create_web_application_target(
            "foo",
            urls=["https://example.com", "https://example.com/app"],
        )

        self.connection.send.has_been_called_with(
            b"<create_web_application_target>"
            b"<name>foo</name>"
            b"<urls>https://example.com,https://example.com/app</urls>"
            b"</create_web_application_target>"
        )

    def test_create_target_with_credential_id(self):
        self.gmp.create_web_application_target(
            "foo", urls=["https://example.com"], credential_id="c1"
        )

        self.connection.send.has_been_called_with(
            b"<create_web_application_target>"
            b"<name>foo</name>"
            b"<urls>https://example.com</urls>"
            b'<credential id="c1"/>'
            b"</create_web_application_target>"
        )
