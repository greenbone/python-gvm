# -*- coding: utf-8 -*-
# Copyright (C) 2023 Greenbone AG
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

from gvm.errors import InvalidArgumentType, RequiredArgument
from gvm.protocols.gmpv225 import ResourceType


class GmpGetResourceNamesListTestMixin:
    def test_get_resource_names_list(self):
        self.gmp.get_resource_names_list(ResourceType.ALERT)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="ALERT"/>'
        )

        self.gmp.get_resource_names_list(ResourceType.CERT_BUND_ADV)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="CERT_BUND_ADV"/>'
        )

        self.gmp.get_resource_names_list(ResourceType.CONFIG)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="CONFIG"/>'
        )

        self.gmp.get_resource_names_list(resource_type=ResourceType.CPE)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="CPE"/>'
        )

        self.gmp.get_resource_names_list(ResourceType.CREDENTIAL)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="CREDENTIAL"/>'
        )

        self.gmp.get_resource_names_list(ResourceType.CVE)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="CVE"/>'
        )

        self.gmp.get_resource_names_list(ResourceType.DFN_CERT_ADV)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="DFN_CERT_ADV"/>'
        )

        self.gmp.get_resource_names_list(ResourceType.FILTER)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="FILTER"/>'
        )

        self.gmp.get_resource_names_list(ResourceType.GROUP)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="GROUP"/>'
        )

        self.gmp.get_resource_names_list(ResourceType.HOST)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="HOST"/>'
        )

        self.gmp.get_resource_names_list(ResourceType.NOTE)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="NOTE"/>'
        )

        self.gmp.get_resource_names_list(ResourceType.NVT)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="NVT"/>'
        )

        self.gmp.get_resource_names_list(ResourceType.OS)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="OS"/>'
        )

        self.gmp.get_resource_names_list(ResourceType.OVERRIDE)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="OVERRIDE"/>'
        )

        self.gmp.get_resource_names_list(ResourceType.PERMISSION)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="PERMISSION"/>'
        )

        self.gmp.get_resource_names_list(ResourceType.PORT_LIST)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="PORT_LIST"/>'
        )

        self.gmp.get_resource_names_list(ResourceType.REPORT_FORMAT)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="REPORT_FORMAT"/>'
        )

        self.gmp.get_resource_names_list(ResourceType.REPORT)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="REPORT"/>'
        )

        self.gmp.get_resource_names_list(ResourceType.RESULT)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="RESULT"/>'
        )

        self.gmp.get_resource_names_list(ResourceType.ROLE)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="ROLE"/>'
        )

        self.gmp.get_resource_names_list(ResourceType.SCANNER)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="SCANNER"/>'
        )

        self.gmp.get_resource_names_list(ResourceType.SCHEDULE)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="SCHEDULE"/>'
        )

        self.gmp.get_resource_names_list(ResourceType.TARGET)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="TARGET"/>'
        )

        self.gmp.get_resource_names_list(ResourceType.TASK)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="TASK"/>'
        )

        self.gmp.get_resource_names_list(ResourceType.TLS_CERTIFICATE)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="TLS_CERTIFICATE"/>'
        )

        self.gmp.get_resource_names_list(ResourceType.USER)

        self.connection.send.has_been_called_with(
            '<get_resource_names type="USER"/>'
        )

        with self.assertRaises(AttributeError):
            self.gmp.get_resource_names_list(
                ResourceType.ALLRESOURCES  # pylint: disable=no-member
            )

    def test_get_resource_names_list_missing_resource_type(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_resource_names_list(resource_type=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_resource_names_list(resource_type="")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_resource_names_list("")

    def test_get_resource_names_list_invalid_resource_type(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.get_resource_names_list(resource_type="foo")

    def test_get_resource_names_list_with_filter_string(self):
        self.gmp.get_resource_names_list(
            ResourceType.CPE, filter_string="foo=bar"
        )

        self.connection.send.has_been_called_with(
            '<get_resource_names type="CPE" filter="foo=bar"/>'
        )
