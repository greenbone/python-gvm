# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from unittest.mock import MagicMock, patch

from gvm.http.core._api import GvmHttpApi


class GvmHttpApiTestCase(unittest.TestCase):
    # pylint: disable=protected-access

    @patch("gvm.http.core.connector.HttpApiConnector")
    def test_basic_init(self, connector_mock: MagicMock):
        api = GvmHttpApi(connector_mock)
        self.assertEqual(connector_mock, api._connector)

    @patch("gvm.http.core.connector.HttpApiConnector")
    def test_init_with_key(self, connector_mock: MagicMock):
        api = GvmHttpApi(connector_mock, api_key="my-api-key")
        self.assertEqual(connector_mock, api._connector)
        self.assertEqual("my-api-key", api._api_key)
