# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest
from collections import OrderedDict

from gvm.errors import RequiredArgument
from gvm.protocols.ospv1 import Osp

from .. import MockConnection


class OSPStartScanTestCase(unittest.TestCase):
    def setUp(self):
        self.connection = MockConnection()
        self.osp = Osp(self.connection)

    def test_start_scan(self):
        scanner_params = OrderedDict()
        scanner_params["key1"] = "value1"

        targets = list()
        _target1 = OrderedDict()
        _target1["hosts"] = "localhost"
        _target1["ports"] = "22,80"
        targets.append(_target1)

        _target2 = OrderedDict()
        _target2["hosts"] = "192.168.10.1"
        _target2["ports"] = "443"
        _smb = OrderedDict()
        _smb["username"] = "username"
        _smb["password"] = "pass"
        _smb["port"] = "port"
        _smb["type"] = "type"
        _credential1 = {"smb": _smb}
        _target2["credentials"] = _credential1
        targets.append(_target2)

        vts = OrderedDict()
        vts["vt1"] = {"value_id": "value"}
        vts["vt_groups"] = ["family=A", "family=B"]

        self.osp.start_scan(
            scan_id="123-456",
            parallel=10,
            scanner_params=scanner_params,
            targets=targets,
            vt_selection=vts,
        )

        self.connection.send.has_been_called_with(
            '<start_scan scan_id="123-456" parallel="10">'
            '<scanner_params key1="value1"/>'
            "<targets><target><hosts>localhost</hosts>"
            "<ports>22,80</ports></target>"
            "<target><hosts>192.168.10.1</hosts>"
            "<ports>443</ports>"
            "<credentials>"
            '<credential type="type" port="port" service="smb">'
            "<username>username</username>"
            "<password>pass</password>"
            "</credential></credentials>"
            "</target></targets><vt_selection>"
            '<vt_single id="vt1">'
            '<vt_value id="value_id">value</vt_value></vt_single>'
            '<vt_group filter="family=A"/><vt_group filter="family=B"/>'
            "</vt_selection></start_scan>"
        )

    def test_start_scan_without_target(self):
        with self.assertRaises(RequiredArgument):
            self.osp.start_scan()

    def test_start_scan_legacy(self):
        self.osp.start_scan(
            scan_id="123-456", parallel=10, target="localhost", ports="22"
        )
        self.connection.send.has_been_called_with(
            '<start_scan scan_id="123-456" parallel="10" '
            'target="localhost" ports="22">'
            "<scanner_params/></start_scan>"
        )


if __name__ == "__main__":
    unittest.main()
