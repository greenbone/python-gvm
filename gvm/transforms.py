# -*- coding: utf-8 -*-
# Copyright (C) 2018 - 2019 Greenbone Networks GmbH
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
"""
Module for transforming responses
"""
from lxml import etree

from .errors import GvmError, GvmServerError, GvmResponseError
from .xml import create_parser


class EtreeTransform:
    """
    Transform a response into a lxml.etree root element
    """

    def __init__(self):
        self._parser = create_parser()

    def _convert_response(self, response: str) -> etree.Element:
        return etree.XML(response, parser=self._parser)

    def __call__(self, response: str) -> etree.Element:
        return self._convert_response(response)


def _check_command_status(root: etree.Element):
    status = root.get("status")

    if status is None:
        raise GvmServerError("No status in response.", root)

    if status[0] == "4":
        raise GvmResponseError(status=status, message=root.get("status_text"))
    elif status[0] == "5":
        raise GvmServerError(status=status, message=root.get("status_text"))
    elif status[0] != "2":
        raise GvmError(
            "Error in response. {0}".format(root.get("status_text")), root
        )


class CheckCommandTransform(EtreeTransform):
    """
    Check the response code of a response and raise GmpError if
    response was an error response
    """

    def __call__(self, response: str) -> str:
        root = self._convert_response(response)

        _check_command_status(root)

        return response


class EtreeCheckCommandTransform(EtreeTransform):
    """
    Transform a response into a lxml.etree root element and raise GmpError if
    response was an error response
    """

    def __call__(self, response: str) -> etree.Element:
        root = self._convert_response(response)

        _check_command_status(root)

        return root
