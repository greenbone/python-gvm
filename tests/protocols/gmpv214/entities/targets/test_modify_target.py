# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgumentType, RequiredArgument
from gvm.protocols.gmpv214.entities.targets import AliveTest


class GmpModifyTargetTestMixin:
    def test_modify_target(self):
        self.gmp.modify_target(target_id="t1")

        self.connection.send.has_been_called_with(
            '<modify_target target_id="t1"/>'
        )

    def test_modify_target_missing_target_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_target(target_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_target(target_id="")

    def test_modify_target_with_comment(self):
        self.gmp.modify_target(target_id="t1", comment="foo")

        self.connection.send.has_been_called_with(
            '<modify_target target_id="t1">'
            "<comment>foo</comment>"
            "</modify_target>"
        )

    def test_modify_target_with_hosts(self):
        self.gmp.modify_target(target_id="t1", hosts=["foo"])

        self.connection.send.has_been_called_with(
            '<modify_target target_id="t1">'
            "<hosts>foo</hosts>"
            "<exclude_hosts></exclude_hosts>"
            "</modify_target>"
        )

        self.gmp.modify_target(target_id="t1", hosts=["foo", "bar"])

        self.connection.send.has_been_called_with(
            '<modify_target target_id="t1">'
            "<hosts>foo,bar</hosts>"
            "<exclude_hosts></exclude_hosts>"
            "</modify_target>"
        )

    def test_modify_target_with_hosts_and_exclude_hosts(self):
        self.gmp.modify_target(
            target_id="t1", hosts=["foo", "bar"], exclude_hosts=["foo"]
        )

        self.connection.send.has_been_called_with(
            '<modify_target target_id="t1">'
            "<hosts>foo,bar</hosts>"
            "<exclude_hosts>foo</exclude_hosts>"
            "</modify_target>"
        )

    def test_modify_target_with_name(self):
        self.gmp.modify_target(target_id="t1", name="foo")

        self.connection.send.has_been_called_with(
            '<modify_target target_id="t1">'
            "<name>foo</name>"
            "</modify_target>"
        )

    def test_modify_target_with_exclude_hosts(self):
        self.gmp.modify_target(target_id="t1", exclude_hosts=["foo"])

        self.connection.send.has_been_called_with(
            '<modify_target target_id="t1">'
            "<exclude_hosts>foo</exclude_hosts>"
            "</modify_target>"
        )

        self.gmp.modify_target(target_id="t1", exclude_hosts=["foo", "bar"])

        self.connection.send.has_been_called_with(
            '<modify_target target_id="t1">'
            "<exclude_hosts>foo,bar</exclude_hosts>"
            "</modify_target>"
        )

    def test_modify_target_with_ssh_credential(self):
        self.gmp.modify_target(target_id="t1", ssh_credential_id="c1")

        self.connection.send.has_been_called_with(
            '<modify_target target_id="t1">'
            '<ssh_credential id="c1"/>'
            "</modify_target>"
        )

    def test_modify_target_with_ssh_credential_port(self):
        self.gmp.modify_target(
            target_id="t1", ssh_credential_id="c1", ssh_credential_port=123
        )

        self.connection.send.has_been_called_with(
            '<modify_target target_id="t1">'
            '<ssh_credential id="c1">'
            "<port>123</port>"
            "</ssh_credential>"
            "</modify_target>"
        )

    def test_modify_target_with_smb_credential_id(self):
        self.gmp.modify_target(target_id="t1", smb_credential_id="c1")

        self.connection.send.has_been_called_with(
            '<modify_target target_id="t1">'
            '<smb_credential id="c1"/>'
            "</modify_target>"
        )

    def test_modify_target_with_esxi_credential_id(self):
        self.gmp.modify_target(target_id="t1", esxi_credential_id="c1")

        self.connection.send.has_been_called_with(
            '<modify_target target_id="t1">'
            '<esxi_credential id="c1"/>'
            "</modify_target>"
        )

    def test_modify_target_with_snmp_credential_id(self):
        self.gmp.modify_target(target_id="t1", snmp_credential_id="c1")

        self.connection.send.has_been_called_with(
            '<modify_target target_id="t1">'
            '<snmp_credential id="c1"/>'
            "</modify_target>"
        )

    def test_modify_target_with_alive_tests(self):
        self.gmp.modify_target(target_id="t1", alive_test=AliveTest.ICMP_PING)

        self.connection.send.has_been_called_with(
            '<modify_target target_id="t1">'
            "<alive_tests>ICMP Ping</alive_tests>"
            "</modify_target>"
        )

    def test_modify_target_invalid_alive_tests(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_target(target_id="t1", alive_test="foo")

    def test_modify_target_with_allow_simultaneous_ips(self):
        self.gmp.modify_target(target_id="t1", allow_simultaneous_ips=True)

        self.connection.send.has_been_called_with(
            '<modify_target target_id="t1">'
            "<allow_simultaneous_ips>1</allow_simultaneous_ips>"
            "</modify_target>"
        )

        self.gmp.modify_target(target_id="t1", allow_simultaneous_ips=False)

        self.connection.send.has_been_called_with(
            '<modify_target target_id="t1">'
            "<allow_simultaneous_ips>0</allow_simultaneous_ips>"
            "</modify_target>"
        )

    def test_modify_target_with_reverse_lookup_only(self):
        self.gmp.modify_target(target_id="t1", reverse_lookup_only=True)

        self.connection.send.has_been_called_with(
            '<modify_target target_id="t1">'
            "<reverse_lookup_only>1</reverse_lookup_only>"
            "</modify_target>"
        )

        self.gmp.modify_target(target_id="t1", reverse_lookup_only=False)

        self.connection.send.has_been_called_with(
            '<modify_target target_id="t1">'
            "<reverse_lookup_only>0</reverse_lookup_only>"
            "</modify_target>"
        )

    def test_modify_target_with_reverse_lookup_unify(self):
        self.gmp.modify_target(target_id="t1", reverse_lookup_unify=True)

        self.connection.send.has_been_called_with(
            '<modify_target target_id="t1">'
            "<reverse_lookup_unify>1</reverse_lookup_unify>"
            "</modify_target>"
        )

        self.gmp.modify_target(target_id="t1", reverse_lookup_unify=False)

        self.connection.send.has_been_called_with(
            '<modify_target target_id="t1">'
            "<reverse_lookup_unify>0</reverse_lookup_unify>"
            "</modify_target>"
        )

    def test_modify_target_with_port_list_id(self):
        self.gmp.modify_target(target_id="t1", port_list_id="pl1")

        self.connection.send.has_been_called_with(
            '<modify_target target_id="t1">'
            '<port_list id="pl1"/>'
            "</modify_target>"
        )
