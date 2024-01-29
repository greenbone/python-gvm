# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from tests import CallableMock


class MockConnection:
    def __init__(self):
        self.connect = CallableMock("connect")
        self.disconnect = CallableMock("disconnect")
        self.send = CallableMock("send")
        self.read = CallableMock("read")
        self.read.return_value('<foo_response status="200"/>')
        self.finish_send = CallableMock("finish_send")


class GmpTestCase(unittest.TestCase):
    gmp_class = None

    def setUp(self):
        self.connection = MockConnection()
        # pylint: disable=not-callable
        self.gmp = self.gmp_class(self.connection)
