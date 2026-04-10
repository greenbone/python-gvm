# SPDX-FileCopyrightText: 2018-2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCreateContainerTaskTestMixin:
    def test_create_container_task_emits_deprecation_warning_and_sends_xml(
        self,
    ):
        with self.assertWarns(DeprecationWarning):
            self.gmp.create_container_task(name="foo")

        self.connection.send.has_been_called_with(
            b'<create_task><name>foo</name><target id="0"/></create_task>'
        )

    def test_create_container_task_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_container_task(name=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.create_container_task(name="")

    def test_create_container_task_with_comment_emits_warning(self):
        with self.assertWarns(DeprecationWarning):
            self.gmp.create_container_task(name="foo", comment="bar")

        self.connection.send.has_been_called_with(
            b"<create_task>"
            b"<name>foo</name>"
            b'<target id="0"/>'
            b"<comment>bar</comment>"
            b"</create_task>"
        )
