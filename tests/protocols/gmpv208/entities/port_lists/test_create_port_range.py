# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgumentType, RequiredArgument
from gvm.protocols.gmpv208.entities.port_lists import PortRangeType


class GmpCreatePortRangeTestMixin:
    def test_create_port_range_missing_port_list_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_port_range(
                port_list_id=None,
                start=1,
                end=1234,
                port_range_type=PortRangeType.TCP,
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_port_range(
                port_list_id="",
                start=1,
                end=1234,
                port_range_type=PortRangeType.TCP,
            )

    def test_create_port_range_missing_start(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_port_range(
                port_list_id="pl1",
                start=None,
                end=1234,
                port_range_type=PortRangeType.TCP,
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_port_range(
                port_list_id="pl1",
                start="",
                end=1234,
                port_range_type=PortRangeType.TCP,
            )

    def test_create_port_range_missing_end(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_port_range(
                port_list_id="pl1",
                start=1,
                end=None,
                port_range_type=PortRangeType.TCP,
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_port_range(
                port_list_id="pl1",
                start=1,
                end="",
                port_range_type=PortRangeType.TCP,
            )

    def test_create_port_range_missing_port_range_type(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_port_range(
                port_list_id="pl1", start=1, end=1234, port_range_type=None
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_port_range(
                port_list_id="pl1", start=1, end=1234, port_range_type=""
            )

    def test_create_port_range_invalid_port_range_type(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_port_range(
                port_list_id="pl1", start=1, end=1234, port_range_type="blubb"
            )

    def test_create_port_range(self):
        self.gmp.create_port_range(
            port_list_id="pl1",
            start=1,
            end=1234,
            port_range_type=PortRangeType.TCP,
        )

        self.connection.send.has_been_called_with(
            "<create_port_range>"
            '<port_list id="pl1"/>'
            "<start>1</start>"
            "<end>1234</end>"
            "<type>TCP</type>"
            "</create_port_range>"
        )

        self.gmp.create_port_range(
            port_list_id="pl1",
            start=1,
            end=1234,
            port_range_type=PortRangeType.UDP,
        )

        self.connection.send.has_been_called_with(
            "<create_port_range>"
            '<port_list id="pl1"/>'
            "<start>1</start>"
            "<end>1234</end>"
            "<type>UDP</type>"
            "</create_port_range>"
        )

        self.gmp.create_port_range(
            port_list_id="pl1",
            start="1",
            end="1234",
            port_range_type=PortRangeType.TCP,
        )

        self.connection.send.has_been_called_with(
            "<create_port_range>"
            '<port_list id="pl1"/>'
            "<start>1</start>"
            "<end>1234</end>"
            "<type>TCP</type>"
            "</create_port_range>"
        )

    def test_create_port_range_with_comment(self):
        self.gmp.create_port_range(
            port_list_id="pl1",
            start=1,
            end=1234,
            port_range_type=PortRangeType.TCP,
            comment="lorem",
        )

        self.connection.send.has_been_called_with(
            "<create_port_range>"
            '<port_list id="pl1"/>'
            "<start>1</start>"
            "<end>1234</end>"
            "<type>TCP</type>"
            "<comment>lorem</comment>"
            "</create_port_range>"
        )
