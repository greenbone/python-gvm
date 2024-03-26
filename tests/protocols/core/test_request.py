# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.protocols.core import Request


class RequestMock:
    def __init__(self, data: bytes) -> None:
        self._data = data

    def __bytes__(self) -> bytes:
        return self._data


class RequestTestCase(unittest.TestCase):
    def test_request(self) -> None:
        # request is just a protocol and can be implemented by several classes
        request = RequestMock(b"some data")
        self.assertIsInstance(request, Request)

        self.assertEqual(bytes(request), b"some data")
