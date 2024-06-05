# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import AliveTest, Targets


class TargetsTestCase(unittest.TestCase):
    def test_create_target_missing_name(self):
        with self.assertRaises(RequiredArgument):
            Targets.create_target(None, hosts=["foo"])

        with self.assertRaises(RequiredArgument):
            Targets.create_target(name=None, hosts=["foo"])

        with self.assertRaises(RequiredArgument):
            Targets.create_target("", hosts=["foo"])

    def test_create_target_missing_hosts(self):
        with self.assertRaises(RequiredArgument):
            Targets.create_target(name="foo")

    def test_create_target_with_hosts(self):
        request = Targets.create_target("foo", hosts=["foo"])

        self.assertEqual(
            bytes(request),
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b"</create_target>",
        )

        request = Targets.create_target("foo", hosts=["foo", "bar"])

        self.assertEqual(
            bytes(request),
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo,bar</hosts>"
            b"</create_target>",
        )

    def test_create_target_with_asset_hosts_filter(self):
        request = Targets.create_target("foo", asset_hosts_filter="name=foo")

        self.assertEqual(
            bytes(request),
            b"<create_target>"
            b"<name>foo</name>"
            b'<asset_hosts filter="name=foo"/>'
            b"</create_target>",
        )

    def test_create_target_with_comment(self):
        request = Targets.create_target("foo", hosts=["foo"], comment="bar")

        self.assertEqual(
            bytes(request),
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b"<comment>bar</comment>"
            b"</create_target>",
        )

    def test_create_target_with_exclude_hosts(self):
        request = Targets.create_target(
            "foo", hosts=["foo", "bar"], exclude_hosts=["bar", "ipsum"]
        )

        self.assertEqual(
            bytes(request),
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo,bar</hosts>"
            b"<exclude_hosts>bar,ipsum</exclude_hosts>"
            b"</create_target>",
        )

    def test_create_target_with_ssh_credential(self):
        request = Targets.create_target(
            "foo", hosts=["foo"], ssh_credential_id="c1"
        )

        self.assertEqual(
            bytes(request),
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b'<ssh_credential id="c1"/>'
            b"</create_target>",
        )

    def test_create_target_with_ssh_credential_port(self):
        request = Targets.create_target(
            "foo", hosts=["foo"], ssh_credential_id="c1", ssh_credential_port=22
        )

        self.assertEqual(
            bytes(request),
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b'<ssh_credential id="c1"><port>22</port></ssh_credential>'
            b"</create_target>",
        )

    def test_create_target_with_smb_credential_id(self):
        request = Targets.create_target(
            "foo", hosts=["foo"], smb_credential_id="c1"
        )

        self.assertEqual(
            bytes(request),
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b'<smb_credential id="c1"/>'
            b"</create_target>",
        )

    def test_create_target_with_esxi_credential_id(self):
        request = Targets.create_target(
            "foo", hosts=["foo"], esxi_credential_id="c1"
        )

        self.assertEqual(
            bytes(request),
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b'<esxi_credential id="c1"/>'
            b"</create_target>",
        )

    def test_create_target_with_snmp_credential_id(self):
        request = Targets.create_target(
            "foo", hosts=["foo"], snmp_credential_id="c1"
        )

        self.assertEqual(
            bytes(request),
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b'<snmp_credential id="c1"/>'
            b"</create_target>",
        )

    def test_create_target_with_alive_tests(self):
        request = Targets.create_target(
            "foo", hosts=["foo"], alive_test=AliveTest.ICMP_PING
        )

        self.assertEqual(
            bytes(request),
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b"<alive_tests>ICMP Ping</alive_tests>"
            b"</create_target>",
        )

        request = Targets.create_target(
            "foo", hosts=["foo"], alive_test="icmp ping"
        )

        self.assertEqual(
            bytes(request),
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b"<alive_tests>ICMP Ping</alive_tests>"
            b"</create_target>",
        )

    def test_create_target_invalid_alive_tests(self):
        with self.assertRaises(InvalidArgument):
            Targets.create_target("foo", hosts=["foo"], alive_test="foo")

    def test_create_target_with_allow_simultaneous_ips(self):
        request = Targets.create_target(
            "foo", hosts=["foo"], allow_simultaneous_ips=True
        )

        self.assertEqual(
            bytes(request),
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b"<allow_simultaneous_ips>1</allow_simultaneous_ips>"
            b"</create_target>",
        )

        request = Targets.create_target(
            "foo", hosts=["foo"], allow_simultaneous_ips=False
        )

        self.assertEqual(
            bytes(request),
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b"<allow_simultaneous_ips>0</allow_simultaneous_ips>"
            b"</create_target>",
        )

    def test_create_target_with_reverse_lookup_only(self):
        request = Targets.create_target(
            "foo", hosts=["foo"], reverse_lookup_only=True
        )

        self.assertEqual(
            bytes(request),
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b"<reverse_lookup_only>1</reverse_lookup_only>"
            b"</create_target>",
        )

        request = Targets.create_target(
            "foo", hosts=["foo"], reverse_lookup_only=False
        )

        self.assertEqual(
            bytes(request),
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b"<reverse_lookup_only>0</reverse_lookup_only>"
            b"</create_target>",
        )

    def test_create_target_with_reverse_lookup_unify(self):
        request = Targets.create_target(
            "foo", hosts=["foo"], reverse_lookup_unify=True
        )

        self.assertEqual(
            bytes(request),
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b"<reverse_lookup_unify>1</reverse_lookup_unify>"
            b"</create_target>",
        )

        request = Targets.create_target(
            "foo", hosts=["foo"], reverse_lookup_unify=False
        )

        self.assertEqual(
            bytes(request),
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b"<reverse_lookup_unify>0</reverse_lookup_unify>"
            b"</create_target>",
        )

    def test_create_target_with_port_range(self):
        request = Targets.create_target(
            "foo", hosts=["foo"], port_range="1-65535"
        )

        self.assertEqual(
            bytes(request),
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b"<port_range>1-65535</port_range>"
            b"</create_target>",
        )

    def test_create_target_with_port_list_id(self):
        request = Targets.create_target(
            "foo", hosts=["foo"], port_list_id="pl1"
        )

        self.assertEqual(
            bytes(request),
            b"<create_target>"
            b"<name>foo</name>"
            b"<hosts>foo</hosts>"
            b'<port_list id="pl1"/>'
            b"</create_target>",
        )

    def test_modify_target(self):
        request = Targets.modify_target("t1")

        self.assertEqual(
            bytes(request),
            b'<modify_target target_id="t1"/>',
        )

    def test_modify_target_missing_target_id(self):
        with self.assertRaises(RequiredArgument):
            Targets.modify_target(None)

        with self.assertRaises(RequiredArgument):
            Targets.modify_target("")

    def test_modify_target_with_comment(self):
        request = Targets.modify_target("t1", comment="foo")

        self.assertEqual(
            bytes(request),
            b'<modify_target target_id="t1"><comment>foo</comment></modify_target>',
        )

    def test_modify_target_with_hosts(self):
        request = Targets.modify_target("t1", hosts=["foo"])

        self.assertEqual(
            bytes(request),
            b'<modify_target target_id="t1">'
            b"<hosts>foo</hosts>"
            b"<exclude_hosts></exclude_hosts>"
            b"</modify_target>",
        )

        request = Targets.modify_target("t1", hosts=["foo", "bar"])

        self.assertEqual(
            bytes(request),
            b'<modify_target target_id="t1">'
            b"<hosts>foo,bar</hosts>"
            b"<exclude_hosts></exclude_hosts>"
            b"</modify_target>",
        )

    def test_modify_target_with_hosts_and_exclude_hosts(self):
        request = Targets.modify_target(
            "t1", hosts=["foo", "bar"], exclude_hosts=["foo"]
        )

        self.assertEqual(
            bytes(request),
            b'<modify_target target_id="t1">'
            b"<hosts>foo,bar</hosts>"
            b"<exclude_hosts>foo</exclude_hosts>"
            b"</modify_target>",
        )

    def test_modify_target_with_name(self):
        request = Targets.modify_target("t1", name="foo")

        self.assertEqual(
            bytes(request),
            b'<modify_target target_id="t1">'
            b"<name>foo</name>"
            b"</modify_target>",
        )

    def test_modify_target_with_exclude_hosts(self):
        request = Targets.modify_target("t1", exclude_hosts=["foo"])

        self.assertEqual(
            bytes(request),
            b'<modify_target target_id="t1">'
            b"<exclude_hosts>foo</exclude_hosts>"
            b"</modify_target>",
        )

        request = Targets.modify_target("t1", exclude_hosts=["foo", "bar"])

        self.assertEqual(
            bytes(request),
            b'<modify_target target_id="t1">'
            b"<exclude_hosts>foo,bar</exclude_hosts>"
            b"</modify_target>",
        )

    def test_modify_target_with_ssh_credential_id(self):
        request = Targets.modify_target("t1", ssh_credential_id="c1")

        self.assertEqual(
            bytes(request),
            b'<modify_target target_id="t1">'
            b'<ssh_credential id="c1"/>'
            b"</modify_target>",
        )

    def test_modify_target_with_ssh_credential_id_and_port(self):
        request = Targets.modify_target(
            "t1", ssh_credential_id="c1", ssh_credential_port=22
        )

        self.assertEqual(
            bytes(request),
            b'<modify_target target_id="t1">'
            b'<ssh_credential id="c1"><port>22</port></ssh_credential>'
            b"</modify_target>",
        )

    def test_modify_target_with_smb_credential_id(self):
        request = Targets.modify_target("t1", smb_credential_id="c1")

        self.assertEqual(
            bytes(request),
            b'<modify_target target_id="t1">'
            b'<smb_credential id="c1"/>'
            b"</modify_target>",
        )

    def test_modify_target_with_esxi_credential_id(self):
        request = Targets.modify_target("t1", esxi_credential_id="c1")

        self.assertEqual(
            bytes(request),
            b'<modify_target target_id="t1">'
            b'<esxi_credential id="c1"/>'
            b"</modify_target>",
        )

    def test_modify_target_with_snmp_credential_id(self):
        request = Targets.modify_target("t1", snmp_credential_id="c1")

        self.assertEqual(
            bytes(request),
            b'<modify_target target_id="t1">'
            b'<snmp_credential id="c1"/>'
            b"</modify_target>",
        )

    def test_modify_target_with_alive_tests(self):
        request = Targets.modify_target("t1", alive_test=AliveTest.ICMP_PING)

        self.assertEqual(
            bytes(request),
            b'<modify_target target_id="t1">'
            b"<alive_tests>ICMP Ping</alive_tests>"
            b"</modify_target>",
        )

        request = Targets.modify_target("t1", alive_test="icmp ping")

        self.assertEqual(
            bytes(request),
            b'<modify_target target_id="t1">'
            b"<alive_tests>ICMP Ping</alive_tests>"
            b"</modify_target>",
        )

    def test_modify_target_invalid_alive_tests(self):
        with self.assertRaises(InvalidArgument):
            Targets.modify_target("t1", alive_test="foo")

    def test_modify_target_with_allow_simultaneous_ips(self):
        request = Targets.modify_target("t1", allow_simultaneous_ips=True)

        self.assertEqual(
            bytes(request),
            b'<modify_target target_id="t1">'
            b"<allow_simultaneous_ips>1</allow_simultaneous_ips>"
            b"</modify_target>",
        )

        request = Targets.modify_target("t1", allow_simultaneous_ips=False)

        self.assertEqual(
            bytes(request),
            b'<modify_target target_id="t1">'
            b"<allow_simultaneous_ips>0</allow_simultaneous_ips>"
            b"</modify_target>",
        )

    def test_modify_target_with_reverse_lookup_only(self):
        request = Targets.modify_target("t1", reverse_lookup_only=True)

        self.assertEqual(
            bytes(request),
            b'<modify_target target_id="t1">'
            b"<reverse_lookup_only>1</reverse_lookup_only>"
            b"</modify_target>",
        )

        request = Targets.modify_target("t1", reverse_lookup_only=False)

        self.assertEqual(
            bytes(request),
            b'<modify_target target_id="t1">'
            b"<reverse_lookup_only>0</reverse_lookup_only>"
            b"</modify_target>",
        )

    def test_modify_target_with_reverse_lookup_unify(self):
        request = Targets.modify_target("t1", reverse_lookup_unify=True)

        self.assertEqual(
            bytes(request),
            b'<modify_target target_id="t1">'
            b"<reverse_lookup_unify>1</reverse_lookup_unify>"
            b"</modify_target>",
        )

        request = Targets.modify_target("t1", reverse_lookup_unify=False)

        self.assertEqual(
            bytes(request),
            b'<modify_target target_id="t1">'
            b"<reverse_lookup_unify>0</reverse_lookup_unify>"
            b"</modify_target>",
        )

    def test_modify_target_with_port_list_id(self):
        request = Targets.modify_target("t1", port_list_id="pl1")

        self.assertEqual(
            bytes(request),
            b'<modify_target target_id="t1">'
            b'<port_list id="pl1"/>'
            b"</modify_target>",
        )

    def test_clone_target(self):
        request = Targets.clone_target("t1")

        self.assertEqual(
            bytes(request),
            b"<create_target><copy>t1</copy></create_target>",
        )

    def test_clone_target_missing_target_id(self):
        with self.assertRaises(RequiredArgument):
            Targets.clone_target(None)

        with self.assertRaises(RequiredArgument):
            Targets.clone_target("")

    def test_delete_target(self):
        request = Targets.delete_target("t1")

        self.assertEqual(
            bytes(request),
            b'<delete_target target_id="t1" ultimate="0"/>',
        )

    def test_delete_ultimate(self):
        request = Targets.delete_target("t1", ultimate=True)

        self.assertEqual(
            bytes(request),
            b'<delete_target target_id="t1" ultimate="1"/>',
        )

        request = Targets.delete_target("t1", ultimate=False)

        self.assertEqual(
            bytes(request),
            b'<delete_target target_id="t1" ultimate="0"/>',
        )

    def test_delete_target_missing_target_id(self):
        with self.assertRaises(RequiredArgument):
            Targets.delete_target(None)

        with self.assertRaises(RequiredArgument):
            Targets.delete_target("")

    def test_get_target(self):
        request = Targets.get_target("t1")

        self.assertEqual(
            bytes(request),
            b'<get_targets target_id="t1"/>',
        )

    def test_get_target_with_tasks(self):
        request = Targets.get_target("t1", tasks=True)

        self.assertEqual(
            bytes(request),
            b'<get_targets target_id="t1" tasks="1"/>',
        )

        request = Targets.get_target("t1", tasks=False)

        self.assertEqual(
            bytes(request),
            b'<get_targets target_id="t1" tasks="0"/>',
        )

    def test_get_target_missing_target_id(self):
        with self.assertRaises(RequiredArgument):
            Targets.get_target(None)

        with self.assertRaises(RequiredArgument):
            Targets.get_target("")

    def test_get_targets(self):
        request = Targets.get_targets()

        self.assertEqual(
            bytes(request),
            b"<get_targets/>",
        )

    def test_get_targets_with_filter_string(self):
        request = Targets.get_targets(filter_string="foo=bar")

        self.assertEqual(
            bytes(request),
            b'<get_targets filter="foo=bar"/>',
        )

    def test_get_targets_with_filter_id(self):
        request = Targets.get_targets(filter_id="f1")

        self.assertEqual(
            bytes(request),
            b'<get_targets filt_id="f1"/>',
        )

    def test_get_targets_with_trash(self):
        request = Targets.get_targets(trash=True)

        self.assertEqual(
            bytes(request),
            b'<get_targets trash="1"/>',
        )

        request = Targets.get_targets(trash=False)

        self.assertEqual(
            bytes(request),
            b'<get_targets trash="0"/>',
        )

    def test_get_targets_with_tasks(self):
        request = Targets.get_targets(tasks=True)

        self.assertEqual(
            bytes(request),
            b'<get_targets tasks="1"/>',
        )

        request = Targets.get_targets(tasks=False)

        self.assertEqual(
            bytes(request),
            b'<get_targets tasks="0"/>',
        )
