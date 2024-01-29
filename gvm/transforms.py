# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""
Module for transforming responses
"""
from lxml import etree

from .errors import GvmError, GvmResponseError, GvmServerError
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


def check_command_status(root: etree.Element):
    status = root.get("status")

    if status is None:
        raise GvmServerError("No status in response.", root)

    if status[0] == "4":
        raise GvmResponseError(status=status, message=root.get("status_text"))
    elif status[0] == "5":
        raise GvmServerError(status=status, message=root.get("status_text"))
    elif status[0] != "2":
        raise GvmError(f"Error in response. {root.get('status_text')}", root)


class CheckCommandTransform(EtreeTransform):
    """
    Check the response code of a response and raise GmpError if
    response was an error response
    """

    def __call__(self, response: str) -> str:
        root = self._convert_response(response)

        check_command_status(root)

        return response


class EtreeCheckCommandTransform(EtreeTransform):
    """
    Transform a response into a lxml.etree root element and raise GmpError if
    response was an error response
    """

    def __call__(self, response: str) -> etree.Element:
        root = self._convert_response(response)

        check_command_status(root)

        return root
