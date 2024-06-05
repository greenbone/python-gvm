# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import FilterType


class GmpCreateFilterTestMixin:
    def test_all_available_filters_types_correct(self):
        for filter_type in list(FilterType):
            self.gmp.create_filter(
                name="f1",
                term="sort-reverse=threat first=1 rows=1000",
                filter_type=filter_type,
            )

            self.connection.send.has_been_called_with(
                "<create_filter>"
                "<name>f1</name>"
                "<term>sort-reverse=threat first=1 rows=1000</term>"
                f"<type>{filter_type.value}</type>"
                "</create_filter>".encode("utf-8")
            )

    def test_create_filter_invalid_filter_type(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_filter(
                name="f1",
                term="sort-reverse=threat result_hosts_only=1 "
                "notes=1 overrides=1 levels=hml first=1 rows=1000",
                filter_type="foo",
            )

    def test_create_filter_no_filter_type(self):
        self.gmp.create_filter(
            name="f1",
            term="sort-reverse=threat result_hosts_only=1 "
            "notes=1 overrides=1 levels=hml first=1 rows=1000",
            comment="foo",
        )

        self.connection.send.has_been_called_with(
            b"<create_filter>"
            b"<name>f1</name>"
            b"<comment>foo</comment>"
            b"<term>sort-reverse=threat result_hosts_only=1 notes=1 "
            b"overrides=1 levels=hml first=1 rows=1000</term>"
            b"</create_filter>"
        )

    def test_create_filter(self):
        self.gmp.create_filter(
            name="f1",
            term="sort-reverse=threat result_hosts_only=1 "
            "notes=1 overrides=1 levels=hml first=1 rows=1000",
            filter_type=FilterType.TASK,
            comment="foo",
        )

        self.connection.send.has_been_called_with(
            b"<create_filter>"
            b"<name>f1</name>"
            b"<comment>foo</comment>"
            b"<term>sort-reverse=threat result_hosts_only=1 notes=1 "
            b"overrides=1 levels=hml first=1 rows=1000</term>"
            b"<type>task</type>"
            b"</create_filter>"
        )

    def test_create_filter_without_term(self):
        self.gmp.create_filter(
            name="f1",
            filter_type=FilterType.TASK,
            comment="foo",
        )

        self.connection.send.has_been_called_with(
            b"<create_filter>"
            b"<name>f1</name>"
            b"<comment>foo</comment>"
            b"<type>task</type>"
            b"</create_filter>"
        )

    def test_create_filter_make_unique(self):
        with self.assertRaises(TypeError):
            self.gmp.create_filter(
                name="f1",
                term="sort-reverse=threat result_hosts_only=1 "
                "notes=1 overrides=1 levels=hml first=1 rows=1000",
                filter_type=FilterType.TASK,
                make_unique=True,
                comment="foo",
            )

    def test_create_filter_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_filter("")

        with self.assertRaises(RequiredArgument):
            self.gmp.create_filter(None)
