# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCreateContainerTaskTestMixin:
    def test_create_task(self):
        self.gmp.create_container_task(name="foo")

        self.connection.send.has_been_called_with(
            "<create_task>"
            "<name>foo</name>"
            '<target id="0"/>'
            "</create_task>"
        )

    def test_create_task_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_container_task(name=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.create_container_task(name="")

    def test_create_task_with_comment(self):
        self.gmp.create_container_task(name="foo", comment="bar")

        self.connection.send.has_been_called_with(
            "<create_task>"
            "<name>foo</name>"
            '<target id="0"/>'
            "<comment>bar</comment>"
            "</create_task>"
        )
