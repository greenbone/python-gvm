# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgumentType, RequiredArgument
from gvm.protocols.gmpv208 import FilterType


class GmpModifyFilterTestMixin:
    def test_modify_filter(self):
        self.gmp.modify_filter(filter_id="f1")

        self.connection.send.has_been_called_with(
            '<modify_filter filter_id="f1"/>'
        )

    def test_modify_filter_with_filter_type(self):
        self.gmp.modify_filter(filter_id="f1", filter_type=FilterType.TASK)

        self.connection.send.has_been_called_with(
            '<modify_filter filter_id="f1">'
            "<type>task</type>"
            "</modify_filter>"
        )

    def test_modify_filter_invalid_filter_type(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_filter(filter_id="f1", filter_type="foo")

    def test_modify_filter_missing_filter_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_filter(filter_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_filter(filter_id="")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_filter("")

    def test_modify_filter_with_comment(self):
        self.gmp.modify_filter(filter_id="f1", comment="foo")

        self.connection.send.has_been_called_with(
            '<modify_filter filter_id="f1">'
            "<comment>foo</comment>"
            "</modify_filter>"
        )

    def test_modify_filter_with_name(self):
        self.gmp.modify_filter(filter_id="f1", name="foo")

        self.connection.send.has_been_called_with(
            '<modify_filter filter_id="f1">'
            "<name>foo</name>"
            "</modify_filter>"
        )

    def test_modify_filter_with_term(self):
        self.gmp.modify_filter(filter_id="f1", term="foo=bar")

        self.connection.send.has_been_called_with(
            '<modify_filter filter_id="f1">'
            "<term>foo=bar</term>"
            "</modify_filter>"
        )
