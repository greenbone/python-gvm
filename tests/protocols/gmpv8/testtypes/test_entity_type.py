# -*- coding: utf-8 -*-
# Copyright (C) 2019 Greenbone Networks GmbH
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

from gvm.errors import InvalidArgument
from gvm.protocols.gmpv8 import EntityType, get_entity_type_from_string


class GetEntityTypeFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            get_entity_type_from_string('foo')

    def test_none_or_empty(self):
        ct = get_entity_type_from_string(None)
        self.assertIsNone(ct)
        ct = get_entity_type_from_string('')
        self.assertIsNone(ct)

    def test_agent(self):
        ct = get_entity_type_from_string('agent')
        self.assertEqual(ct, EntityType.AGENT)

    def test_alert(self):
        ct = get_entity_type_from_string('alert')
        self.assertEqual(ct, EntityType.ALERT)

    def test_asset(self):
        ct = get_entity_type_from_string('asset')
        self.assertEqual(ct, EntityType.ASSET)

    def test_cert_bund_adv(self):
        ct = get_entity_type_from_string('cert_bund_adv')
        self.assertEqual(ct, EntityType.CERT_BUND_ADV)

    def test_cpe(self):
        ct = get_entity_type_from_string('cpe')
        self.assertEqual(ct, EntityType.CPE)

    def test_credential(self):
        ct = get_entity_type_from_string('credential')
        self.assertEqual(ct, EntityType.CREDENTIAL)

    def test_dfn_cert_adv(self):
        ct = get_entity_type_from_string('dfn_cert_adv')
        self.assertEqual(ct, EntityType.DFN_CERT_ADV)

    def test_filter(self):
        ct = get_entity_type_from_string('filter')
        self.assertEqual(ct, EntityType.FILTER)

    def test_group(self):
        ct = get_entity_type_from_string('group')
        self.assertEqual(ct, EntityType.GROUP)

    def test_host(self):
        ct = get_entity_type_from_string('host')
        self.assertEqual(ct, EntityType.HOST)

    def test_info(self):
        ct = get_entity_type_from_string('info')
        self.assertEqual(ct, EntityType.INFO)

    def test_note(self):
        ct = get_entity_type_from_string('note')
        self.assertEqual(ct, EntityType.NOTE)

    def test_nvt(self):
        ct = get_entity_type_from_string('nvt')
        self.assertEqual(ct, EntityType.NVT)

    def test_operating_system(self):
        ct = get_entity_type_from_string('os')
        self.assertEqual(ct, EntityType.OPERATING_SYSTEM)

        ct = get_entity_type_from_string('operating_system')
        self.assertEqual(ct, EntityType.OPERATING_SYSTEM)

    def test_ovaldef(self):
        ct = get_entity_type_from_string('ovaldef')
        self.assertEqual(ct, EntityType.OVALDEF)

    def test_override(self):
        ct = get_entity_type_from_string('override')
        self.assertEqual(ct, EntityType.OVERRIDE)

    def test_permission(self):
        ct = get_entity_type_from_string('permission')
        self.assertEqual(ct, EntityType.PERMISSION)

    def test_port_list(self):
        ct = get_entity_type_from_string('port_list')
        self.assertEqual(ct, EntityType.PORT_LIST)

    def test_report(self):
        ct = get_entity_type_from_string('report')
        self.assertEqual(ct, EntityType.REPORT)

    def test_report_format(self):
        ct = get_entity_type_from_string('report_format')
        self.assertEqual(ct, EntityType.REPORT_FORMAT)

    def test_result(self):
        ct = get_entity_type_from_string('result')
        self.assertEqual(ct, EntityType.RESULT)

    def test_role(self):
        ct = get_entity_type_from_string('role')
        self.assertEqual(ct, EntityType.ROLE)

    def test_scan_config(self):
        ct = get_entity_type_from_string('config')
        self.assertEqual(ct, EntityType.SCAN_CONFIG)

        ct = get_entity_type_from_string('scan_config')
        self.assertEqual(ct, EntityType.SCAN_CONFIG)

    def test_scanner(self):
        ct = get_entity_type_from_string('scanner')
        self.assertEqual(ct, EntityType.SCANNER)

    def test_schedule(self):
        ct = get_entity_type_from_string('schedule')
        self.assertEqual(ct, EntityType.SCHEDULE)

    def test_tag(self):
        ct = get_entity_type_from_string('tag')
        self.assertEqual(ct, EntityType.TAG)

    def test_target(self):
        ct = get_entity_type_from_string('target')
        self.assertEqual(ct, EntityType.TARGET)

    def test_task(self):
        ct = get_entity_type_from_string('task')
        self.assertEqual(ct, EntityType.TASK)

    def test_user(self):
        ct = get_entity_type_from_string('user')
        self.assertEqual(ct, EntityType.USER)

    def test_ticket(self):
        ct = get_entity_type_from_string('ticket')
        self.assertEqual(ct, EntityType.TICKET)

    def test_vulnerability(self):
        ct = get_entity_type_from_string('vuln')
        self.assertEqual(ct, EntityType.VULNERABILITY)

        ct = get_entity_type_from_string('vulnerability')
        self.assertEqual(ct, EntityType.VULNERABILITY)


if __name__ == '__main__':
    unittest.main()
