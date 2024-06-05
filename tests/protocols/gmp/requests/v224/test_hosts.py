# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import RequiredArgument
from gvm.protocols.gmp.requests.v224 import Hosts


class HostsTestCase(unittest.TestCase):
    def test_create_host(self):
        request = Hosts.create_host("host_name")
        self.assertEqual(
            bytes(request),
            b"<create_asset><asset>"
            b"<type>host</type>"
            b"<name>host_name</name>"
            b"</asset></create_asset>",
        )

    def test_create_host_with_comment(self):
        request = Hosts.create_host("host_name", comment="comment")
        self.assertEqual(
            bytes(request),
            b"<create_asset><asset>"
            b"<type>host</type>"
            b"<name>host_name</name>"
            b"<comment>comment</comment>"
            b"</asset></create_asset>",
        )

    def test_create_host_missing_name(self):
        with self.assertRaises(RequiredArgument):
            Hosts.create_host(None)

        with self.assertRaises(RequiredArgument):
            Hosts.create_host("")

    def test_delete_host(self):
        request = Hosts.delete_host("host_id")
        self.assertEqual(
            bytes(request),
            b'<delete_asset asset_id="host_id"/>',
        )

    def test_delete_host_missing_host_id(self):
        with self.assertRaises(RequiredArgument):
            Hosts.delete_host(None)

        with self.assertRaises(RequiredArgument):
            Hosts.delete_host("")

    def test_get_hosts(self):
        request = Hosts.get_hosts()
        self.assertEqual(
            bytes(request),
            b'<get_assets type="host"/>',
        )

    def test_get_hosts_with_filter_string(self):
        request = Hosts.get_hosts(filter_string="filter_string")
        self.assertEqual(
            bytes(request),
            b'<get_assets type="host" filter="filter_string"/>',
        )

    def test_get_hosts_with_filter_id(self):
        request = Hosts.get_hosts(filter_id="filter_id")
        self.assertEqual(
            bytes(request),
            b'<get_assets type="host" filt_id="filter_id"/>',
        )

    def test_get_hosts_with_details(self):
        request = Hosts.get_hosts(details=True)
        self.assertEqual(
            bytes(request),
            b'<get_assets type="host" details="1"/>',
        )

        request = Hosts.get_hosts(details=False)
        self.assertEqual(
            bytes(request),
            b'<get_assets type="host" details="0"/>',
        )

    def test_get_host(self):
        request = Hosts.get_host("host_id")
        self.assertEqual(
            bytes(request),
            b'<get_assets asset_id="host_id" type="host"/>',
        )

    def test_get_host_with_details(self):
        request = Hosts.get_host("host_id", details=True)
        self.assertEqual(
            bytes(request),
            b'<get_assets asset_id="host_id" type="host" details="1"/>',
        )

        request = Hosts.get_host("host_id", details=False)
        self.assertEqual(
            bytes(request),
            b'<get_assets asset_id="host_id" type="host" details="0"/>',
        )

    def test_get_host_missing_host_id(self):
        with self.assertRaises(RequiredArgument):
            Hosts.get_host(None)

        with self.assertRaises(RequiredArgument):
            Hosts.get_host("")

    def test_modify_host(self):
        request = Hosts.modify_host("host_id")
        self.assertEqual(
            bytes(request),
            b'<modify_asset asset_id="host_id">'
            b"<comment></comment>"
            b"</modify_asset>",
        )

    def test_modify_host_with_comment(self):
        request = Hosts.modify_host("host_id", comment="comment")
        self.assertEqual(
            bytes(request),
            b'<modify_asset asset_id="host_id">'
            b"<comment>comment</comment>"
            b"</modify_asset>",
        )

    def test_modify_host_missing_host_id(self):
        with self.assertRaises(RequiredArgument):
            Hosts.modify_host(None)

        with self.assertRaises(RequiredArgument):
            Hosts.modify_host("")
