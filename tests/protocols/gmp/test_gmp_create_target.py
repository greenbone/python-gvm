# -*- coding: utf-8 -*-
# Copyright (C) 2018 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest

from gvm.errors import RequiredArgument
from gvm.protocols.gmpv7 import Gmp

from .. import MockConnection

def hosts(hostlist):
    return ', '.join(hostlist)

class GMPCreateTargetCommandTestCase(unittest.TestCase):

    TARGET_NAME = 'Unittest Target'
    TARGET_HOSTS = ['127.0.0.1', 'foo.bar']
    COMMENT = 'This is a comment'
    UUID = '00000000-0000-0000-0000-000000000000'
    PORT = '1234'
    ALIVE_TEST = 'ICMP Ping'
    PORT_RANGE = 'T:10-20,U:10-30'

    def setUp(self):
        self.connection = MockConnection()
        self.gmp = Gmp(self.connection)

    def test_valid_name_make_unique_true_correct(self):
        self.gmp.create_target(self.TARGET_NAME, make_unique=True,
                               hosts=self.TARGET_HOSTS)

        self.connection.send.has_been_called_with(
            '<create_target><name>{target}<make_unique>1</make_unique></name>'
            '<hosts>{hosts}</hosts>'
            '</create_target>'.format(
                target=self.TARGET_NAME, hosts=hosts(self.TARGET_HOSTS))
        )

    def test_valid_name_make_unique_false_correct(self):
        self.gmp.create_target(self.TARGET_NAME, make_unique=False,
                               hosts=self.TARGET_HOSTS)

        self.connection.send.has_been_called_with(
            '<create_target><name>{target}</name>'
            '<hosts>{hosts}</hosts>'
            '</create_target>'.format(
                target=self.TARGET_NAME, hosts=hosts(self.TARGET_HOSTS))
        )

    def test_empty_name_value_error(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_target(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.create_target("")

    def test_asset_hosts_correct(self):
        self.gmp.create_target(self.TARGET_NAME, asset_hosts_filter='name=foo')

        self.connection.send.has_been_called_with(
            '<create_target><name>{target}</name>'
            '<asset_hosts filter="name=foo"/>'
            '</create_target>'.format(target=self.TARGET_NAME)
        )

    def test_no_host_no_asset_hosts_value_error(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_target(self.TARGET_NAME)

    def test_comment_correct(self):
        self.gmp.create_target(self.TARGET_NAME, hosts=self.TARGET_HOSTS,
                               comment=self.COMMENT)

        self.connection.send.has_been_called_with(
            '<create_target><name>{target}</name>'
            '<hosts>{hosts}</hosts>'
            '<comment>{comment}</comment>'
            '</create_target>'.format(
                target=self.TARGET_NAME, hosts=hosts(self.TARGET_HOSTS),
                comment=self.COMMENT)
        )

    def test_copy_correct(self):
        self.gmp.create_target(self.TARGET_NAME, hosts=self.TARGET_HOSTS,
                               copy=self.UUID)

        self.connection.send.has_been_called_with(
            '<create_target><name>{target}</name>'
            '<hosts>{hosts}</hosts>'
            '<copy>{copy}</copy>'
            '</create_target>'.format(
                target=self.TARGET_NAME, hosts=hosts(self.TARGET_HOSTS),
                copy=self.UUID,
            )
        )

    def test_exclude_hosts_correct(self):
        self.gmp.create_target(self.TARGET_NAME,
                               hosts=self.TARGET_HOSTS,
                               exclude_hosts=self.TARGET_HOSTS)

        self.connection.send.has_been_called_with(
            '<create_target><name>{target}</name>'
            '<hosts>{hosts}</hosts>'
            '<exclude_hosts>{hosts}</exclude_hosts>'
            '</create_target>'.format(
                target=self.TARGET_NAME, hosts=hosts(self.TARGET_HOSTS),
            )
        )

    def test_ssh_credential_correct(self):
        self.gmp.create_target(self.TARGET_NAME,
                               hosts=self.TARGET_HOSTS,
                               ssh_credential_id=self.UUID)

        self.connection.send.has_been_called_with(
            '<create_target><name>{target}</name>'
            '<hosts>{hosts}</hosts>'
            '<ssh_credential id="{uuid}"/>'
            '</create_target>'.format(
                target=self.TARGET_NAME, hosts=hosts(self.TARGET_HOSTS),
                uuid=self.UUID,
            )
        )

    def test_ssh_credential_with_port_correct(self):
        self.gmp.create_target(self.TARGET_NAME,
                               hosts=self.TARGET_HOSTS,
                               ssh_credential_id=self.UUID,
                               ssh_credential_port=self.PORT)

        self.connection.send.has_been_called_with(
            '<create_target><name>{target}</name>'
            '<hosts>{hosts}</hosts>'
            '<ssh_credential id="{uuid}">'
            '<port>{port}</port>'
            '</ssh_credential>'
            '</create_target>'.format(
                target=self.TARGET_NAME, hosts=hosts(self.TARGET_HOSTS),
                uuid=self.UUID, port=self.PORT,
            )
        )

    def test_smb_credential_correct(self):
        self.gmp.create_target(self.TARGET_NAME,
                               hosts=self.TARGET_HOSTS,
                               smb_credential_id=self.UUID)

        self.connection.send.has_been_called_with(
            '<create_target><name>{target}</name>'
            '<hosts>{hosts}</hosts>'
            '<smb_credential id="{uuid}"/>'
            '</create_target>'.format(
                target=self.TARGET_NAME, hosts=hosts(self.TARGET_HOSTS),
                uuid=self.UUID,
            )
        )

    def test_esxi_credential_correct(self):
        self.gmp.create_target(self.TARGET_NAME,
                               hosts=self.TARGET_HOSTS,
                               esxi_credential_id=self.UUID)

        self.connection.send.has_been_called_with(
            '<create_target><name>{target}</name>'
            '<hosts>{hosts}</hosts>'
            '<esxi_credential id="{uuid}"/>'
            '</create_target>'.format(
                target=self.TARGET_NAME, hosts=hosts(self.TARGET_HOSTS),
                uuid=self.UUID,
            )
        )

    def test_snmp_credential_correct_cmd(self):
        self.gmp.create_target(self.TARGET_NAME,
                               hosts=self.TARGET_HOSTS,
                               snmp_credential_id=self.UUID)

        self.connection.send.has_been_called_with(
            '<create_target><name>{target}</name>'
            '<hosts>{hosts}</hosts>'
            '<snmp_credential id="{uuid}"/>'
            '</create_target>'.format(
                target=self.TARGET_NAME, hosts=hosts(self.TARGET_HOSTS),
                uuid=self.UUID,
            )
        )

    def test_alive_tests_correct(self):
        self.gmp.create_target(self.TARGET_NAME,
                               hosts=self.TARGET_HOSTS,
                               alive_tests=self.ALIVE_TEST)

        self.connection.send.has_been_called_with(
            '<create_target><name>{target}</name>'
            '<hosts>{hosts}</hosts>'
            '<alive_tests>{alive}</alive_tests>'
            '</create_target>'.format(
                target=self.TARGET_NAME, hosts=hosts(self.TARGET_HOSTS),
                alive=self.ALIVE_TEST,
            )
        )

    def test_reverse_lookup_only_true_correct(self):
        self.gmp.create_target(self.TARGET_NAME,
                               hosts=self.TARGET_HOSTS,
                               reverse_lookup_only=True)

        self.connection.send.has_been_called_with(
            '<create_target><name>{target}</name>'
            '<hosts>{hosts}</hosts>'
            '<reverse_lookup_only>1</reverse_lookup_only>'
            '</create_target>'.format(
                target=self.TARGET_NAME, hosts=hosts(self.TARGET_HOSTS),
            )
        )

    def test_reverse_lookup_only_false_correct(self):
        self.gmp.create_target(self.TARGET_NAME,
                               hosts=self.TARGET_HOSTS,
                               reverse_lookup_only=False)

        self.connection.send.has_been_called_with(
            '<create_target><name>{target}</name>'
            '<hosts>{hosts}</hosts>'
            '<reverse_lookup_only>0</reverse_lookup_only>'
            '</create_target>'.format(
                target=self.TARGET_NAME, hosts=hosts(self.TARGET_HOSTS),
            )
        )

    def test_reverse_lookup_unify_true_correct(self):
        self.gmp.create_target(self.TARGET_NAME,
                               hosts=self.TARGET_HOSTS,
                               reverse_lookup_unify=True)

        self.connection.send.has_been_called_with(
            '<create_target><name>{target}</name>'
            '<hosts>{hosts}</hosts>'
            '<reverse_lookup_unify>1</reverse_lookup_unify>'
            '</create_target>'.format(
                target=self.TARGET_NAME, hosts=hosts(self.TARGET_HOSTS),
            )
        )

    def test_reverse_lookup_unify_false_correct_cmd(self):
        self.gmp.create_target(self.TARGET_NAME,
                               hosts=self.TARGET_HOSTS,
                               reverse_lookup_unify=False)

        self.connection.send.has_been_called_with(
            '<create_target><name>{target}</name>'
            '<hosts>{hosts}</hosts>'
            '<reverse_lookup_unify>0</reverse_lookup_unify>'
            '</create_target>'.format(
                target=self.TARGET_NAME, hosts=hosts(self.TARGET_HOSTS),
            )
        )

    def test_port_range_correct(self):
        self.gmp.create_target(self.TARGET_NAME,
                               hosts=self.TARGET_HOSTS,
                               port_range=self.PORT_RANGE)

        self.connection.send.has_been_called_with(
            '<create_target><name>{target}</name>'
            '<hosts>{hosts}</hosts>'
            '<port_range>{range}</port_range>'
            '</create_target>'.format(
                target=self.TARGET_NAME, hosts=hosts(self.TARGET_HOSTS),
                range=self.PORT_RANGE,
            )
        )

    def test_port_list_correct_cmd(self):
        self.gmp.create_target(self.TARGET_NAME,
                               hosts=self.TARGET_HOSTS,
                               port_list_id=self.UUID)

        self.connection.send.has_been_called_with(
            '<create_target><name>{target}</name>'
            '<hosts>{hosts}</hosts>'
            '<port_list id="{uuid}"/>'
            '</create_target>'.format(
                target=self.TARGET_NAME, hosts=hosts(self.TARGET_HOSTS),
                uuid=self.UUID,
            )
        )


if __name__ == '__main__':
    unittest.main()
