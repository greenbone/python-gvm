#  SPDX-FileCopyrightText: 2026 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpModifyWebApplicationTargetTestMixin:
    def test_modify_web_application_target(self):
        self.gmp.modify_web_application_target(web_application_target_id="t1")

        self.connection.send.has_been_called_with(
            b'<modify_web_application_target web_application_target_id="t1"/>'
        )

    def test_modify_target_missing_target_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_web_application_target(
                web_application_target_id=None
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_web_application_target(web_application_target_id="")

    def test_modify_target_with_comment(self):
        self.gmp.modify_web_application_target(
            web_application_target_id="t1", comment="foo"
        )

        self.connection.send.has_been_called_with(
            b'<modify_web_application_target web_application_target_id="t1">'
            b"<comment>foo</comment>"
            b"</modify_web_application_target>"
        )

    def test_modify_target_with_urls(self):
        self.gmp.modify_web_application_target(
            web_application_target_id="t1", urls=["https://example.com"]
        )

        self.connection.send.has_been_called_with(
            b'<modify_web_application_target web_application_target_id="t1">'
            b"<urls>https://example.com</urls>"
            b"</modify_web_application_target>"
        )

        self.gmp.modify_web_application_target(
            web_application_target_id="t1",
            urls=["https://example.com", "https://example.com/app"],
        )

        self.connection.send.has_been_called_with(
            b'<modify_web_application_target web_application_target_id="t1">'
            b"<urls>https://example.com,https://example.com/app</urls>"
            b"</modify_web_application_target>"
        )

    def test_modify_target_with_exclude_urls(self):
        self.gmp.modify_web_application_target(
            web_application_target_id="t1",
            exclude_urls=["https://example.com/logout"],
        )

        self.connection.send.has_been_called_with(
            b'<modify_web_application_target web_application_target_id="t1">'
            b"<exclude_urls>https://example.com/logout</exclude_urls>"
            b"</modify_web_application_target>"
        )

    def test_modify_target_with_name(self):
        self.gmp.modify_web_application_target(
            web_application_target_id="t1", name="foo"
        )

        self.connection.send.has_been_called_with(
            b'<modify_web_application_target web_application_target_id="t1">'
            b"<name>foo</name>"
            b"</modify_web_application_target>"
        )

    def test_modify_target_with_credential_id(self):
        self.gmp.modify_web_application_target(
            web_application_target_id="t1", credential_id="c1"
        )

        self.connection.send.has_been_called_with(
            b'<modify_web_application_target web_application_target_id="t1">'
            b'<credential id="c1"/>'
            b"</modify_web_application_target>"
        )
