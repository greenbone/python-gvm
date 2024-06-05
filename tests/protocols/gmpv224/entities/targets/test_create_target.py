# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import AliveTest


class GmpCreateTargetTestMixin:
    def test_create_target_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_target(None, hosts=["foo"])

        with self.assertRaises(RequiredArgument):
            self.gmp.create_target(name=None, hosts=["foo"])

        with self.assertRaises(RequiredArgument):
            self.gmp.create_target("", hosts=["foo"])

    def test_create_target_with_asset_hosts_filter(self):
        self.gmp.create_target("foo", asset_hosts_filter="name=foo")

        self.connection.send.has_been_called_with(
            b"<create_target>"
            b"<name>foo</name>"
            b'<asset_hosts filter="name=foo"/>'
            b"</create_target>"
        )

    def test_create_target_missing_hosts(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_target(name="foo")

    def test_create_target_with_comment(self):
        self.gmp.create_target("foo", hosts=["foo"], comment="bar")

        self.connection.send.has_been_called_with(
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b"<comment>bar</comment>"
            b"</create_target>"
        )

    def test_create_target_with_exclude_hosts(self):
        self.gmp.create_target(
            "foo", hosts=["foo", "bar"], exclude_hosts=["bar", "ipsum"]
        )

        self.connection.send.has_been_called_with(
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo,bar</hosts>"
            b"<exclude_hosts>bar,ipsum</exclude_hosts>"
            b"</create_target>"
        )

    def test_create_target_with_ssh_credential(self):
        self.gmp.create_target("foo", hosts=["foo"], ssh_credential_id="c1")

        self.connection.send.has_been_called_with(
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b'<ssh_credential id="c1"/>'
            b"</create_target>"
        )

    def test_create_target_with_ssh_credential_port(self):
        self.gmp.create_target(
            "foo",
            hosts=["foo"],
            ssh_credential_id="c1",
            ssh_credential_port=123,
        )

        self.connection.send.has_been_called_with(
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b'<ssh_credential id="c1">'
            b"<port>123</port>"
            b"</ssh_credential>"
            b"</create_target>"
        )

    def test_create_target_with_smb_credential_id(self):
        self.gmp.create_target("foo", hosts=["foo"], smb_credential_id="c1")

        self.connection.send.has_been_called_with(
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b'<smb_credential id="c1"/>'
            b"</create_target>"
        )

    def test_create_target_with_esxi_credential_id(self):
        self.gmp.create_target("foo", hosts=["foo"], esxi_credential_id="c1")

        self.connection.send.has_been_called_with(
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b'<esxi_credential id="c1"/>'
            b"</create_target>"
        )

    def test_create_target_with_snmp_credential_id(self):
        self.gmp.create_target("foo", hosts=["foo"], snmp_credential_id="c1")

        self.connection.send.has_been_called_with(
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b'<snmp_credential id="c1"/>'
            b"</create_target>"
        )

    def test_create_target_with_alive_tests(self):
        self.gmp.create_target(
            "foo", hosts=["foo"], alive_test=AliveTest.ICMP_PING
        )

        self.connection.send.has_been_called_with(
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b"<alive_tests>ICMP Ping</alive_tests>"
            b"</create_target>"
        )

    def test_create_target_invalid_alive_tests(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_target("foo", hosts=["foo"], alive_test="foo")

    def test_create_target_with_allow_simultaneous_ips(self):
        self.gmp.create_target(
            "foo", hosts=["foo"], allow_simultaneous_ips=True
        )

        self.connection.send.has_been_called_with(
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b"<allow_simultaneous_ips>1</allow_simultaneous_ips>"
            b"</create_target>"
        )

        self.gmp.create_target(
            "foo", hosts=["foo"], allow_simultaneous_ips=False
        )

        self.connection.send.has_been_called_with(
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b"<allow_simultaneous_ips>0</allow_simultaneous_ips>"
            b"</create_target>"
        )

    def test_create_target_with_reverse_lookup_only(self):
        self.gmp.create_target("foo", hosts=["foo"], reverse_lookup_only=True)

        self.connection.send.has_been_called_with(
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b"<reverse_lookup_only>1</reverse_lookup_only>"
            b"</create_target>"
        )

        self.gmp.create_target("foo", hosts=["foo"], reverse_lookup_only=False)

        self.connection.send.has_been_called_with(
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b"<reverse_lookup_only>0</reverse_lookup_only>"
            b"</create_target>"
        )

    def test_create_target_with_reverse_lookup_unify(self):
        self.gmp.create_target("foo", hosts=["foo"], reverse_lookup_unify=True)

        self.connection.send.has_been_called_with(
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b"<reverse_lookup_unify>1</reverse_lookup_unify>"
            b"</create_target>"
        )

        self.gmp.create_target("foo", hosts=["foo"], reverse_lookup_unify=False)

        self.connection.send.has_been_called_with(
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b"<reverse_lookup_unify>0</reverse_lookup_unify>"
            b"</create_target>"
        )

    def test_create_target_with_port_range(self):
        self.gmp.create_target("foo", hosts=["foo"], port_range="bar")

        self.connection.send.has_been_called_with(
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b"<port_range>bar</port_range>"
            b"</create_target>"
        )

    def test_create_target_with_port_list_id(self):
        self.gmp.create_target("foo", hosts=["foo"], port_list_id="pl1")

        self.connection.send.has_been_called_with(
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b'<port_list id="pl1"/>'
            b"</create_target>"
        )
