# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""
Module for communication to a daemon speaking `Open Scanner Protocol version 1`_

.. _Open Scanner Protocol version 1:
    https://docs.greenbone.net/API/OSP/osp-20.08.html
"""

import logging
from typing import Any, Optional

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.utils import to_bool
from gvm.xml import XmlCommand, XmlCommandElement

from ._protocol import GvmProtocol, T
from .core import Request, Response

logger = logging.getLogger(__name__)

PROTOCOL_VERSION = (1, 2)


def create_credentials_element(
    xml_credentials: XmlCommandElement, credentials: dict[str, dict[str, str]]
):
    """Generates an xml element with credentials."""
    for service, credential in credentials.items():
        cred_type = credential.get("type", "")
        server_port = credential.get("port", "")
        username = credential.get("username")
        password = credential.get("password")

        xml_credential = xml_credentials.add_element("credential")
        xml_credential.set_attribute("type", cred_type)
        xml_credential.set_attribute("port", server_port)
        xml_credential.set_attribute("service", service)

        xml_credential.add_element("username", username)
        xml_credential.add_element("password", password)
    return xml_credentials


def create_vt_selection_element(
    xml_vt_selection: XmlCommandElement, vt_selection: dict[str, Any]
):
    """Generates an xml element with a selection of Vulnerability tests."""
    for vt_id, vt_values in vt_selection.items():
        if vt_id != "vt_groups" and isinstance(vt_values, dict):
            xml_vt = xml_vt_selection.add_element(
                "vt_single", attrs={"id": vt_id}
            )
            if vt_values:
                for key, value in vt_values.items():
                    xml_vt.add_element("vt_value", value, attrs={"id": key})
        elif vt_id == "vt_groups" and isinstance(vt_values, list):
            for group in vt_values:
                xml_vt_selection.add_element(
                    "vt_group", attrs={"filter": group}
                )
        else:
            raise InvalidArgument(
                f"It was not possible to add {vt_id} to the VTs selection."
            )

    return xml_vt_selection


class Osp(GvmProtocol[T]):
    @staticmethod
    def get_protocol_version() -> tuple[int, int]:
        """Determine the Open Scanner Protocol version.

        Returns:
            tuple: Implemented version of the Open Scanner Protocol
        """
        return PROTOCOL_VERSION

    def _send_request(self, cmd: Request) -> Response:
        try:
            return super()._send_request(cmd)
        finally:
            # OSP is stateless. Therefore the connection is closed after each
            # response and we must reset the connection
            self.disconnect()

    def get_version(self) -> T:
        """Get the version of the OSPD server which is connected to."""
        cmd = XmlCommand("get_version")
        return self._send_request_and_transform_response(cmd)

    def help(self) -> T:
        """Get the help text."""
        cmd = XmlCommand("help")
        return self._send_request_and_transform_response(cmd)

    def get_scans(
        self,
        scan_id: Optional[str] = None,
        details: bool = True,
        pop_results: bool = False,
    ) -> T:
        """Get the stored scans.

        Arguments:
            scan_id (str, optional): UUID identifier for a scan.
            details (boolean, optional): Whether to get full scan reports.
                Default: True
            pop_results (boolean, optional) Whether to remove the fetched
                results. Default: False
        """
        cmd = XmlCommand("get_scans")
        if scan_id:
            cmd.set_attribute("scan_id", scan_id)

        cmd.set_attribute("details", to_bool(details))
        cmd.set_attribute("pop_results", to_bool(pop_results))

        return self._send_request_and_transform_response(cmd)

    def delete_scan(self, scan_id: str) -> T:
        """Delete a finished scan.

        Arguments:
            scan_id: UUID identifier for a finished scan.
        """
        if not scan_id:
            raise ValueError("delete_scan requires a scan_id element")

        cmd = XmlCommand("delete_scan")
        cmd.set_attribute("scan_id", scan_id)

        return self._send_request_and_transform_response(cmd)

    def get_scanner_details(self) -> T:
        """Return scanner description and parameters."""
        cmd = XmlCommand("get_scanner_details")
        return self._send_request_and_transform_response(cmd)

    def get_vts(self, vt_id: Optional[str] = None) -> T:
        """Return information about vulnerability tests,
        if offered by scanner.

        Args:
            vt_id: UUID identifier for a vulnerability test.
        """
        cmd = XmlCommand("get_vts")
        if vt_id:
            cmd.set_attribute("vt_id", vt_id)

        return self._send_request_and_transform_response(cmd)

    def start_scan(
        self,
        scan_id: Optional[str] = None,
        parallel: int = 1,
        target=None,
        ports=None,
        targets: Optional[list[dict[str, str]]] = None,
        scanner_params: Optional[dict[str, Any]] = None,
        vt_selection: Optional[dict[str, Any]] = None,
    ) -> T:
        """Start a new scan.

        Args:
            scan_id: UUID identifier for a running scan.
            parallel: Number of parallel scanned targets.
                Default 1.
            target: Deprecated. Please use targets instead.
            targets: List of dictionaries. See example.
            ports: Deprecated. Ports to use for target parameter.
            scanner_params:: Dictionary of scanner parameters.
            vt_selection:: Vulnerability tests to select. See example.

        Examples:

            Scanner Parameters::

                scanner_parameters = {
                    'scan_param1': 'scan_param1_value',
                    'scan_param2': 'scan_param2_value',
                }

            Targets::

                targets = [{
                    'hosts': 'localhost',
                    'ports': '80,43'
                }, {
                    'hosts': '192.168.0.0/24',
                    'ports': '22',
                }, {
                    'credentials': {
                        'smb': {
                            'password': 'pass',
                            'port': 'port',
                            'type': 'type',
                            'username': 'username',
                        }
                    }
                }]

            VT Selection::

                vt_selection = {
                    'vt1': {},
                    'vt2': {'value_id': 'value'},
                    'vt_groups': ['family=debian', 'family=general']
                }
        """
        cmd = XmlCommand("start_scan")

        if scan_id:
            cmd.set_attribute("scan_id", scan_id)

        cmd.set_attribute("parallel", str(parallel))

        # Add <scanner_params> even if it is empty, since it is mandatory
        xml_scan_params = cmd.add_element("scanner_params")
        if scanner_params:
            xml_scan_params.set_attributes(scanner_params)

        if targets:
            xml_targets = cmd.add_element("targets")
            for target in targets:
                xml_target = xml_targets.add_element("target")
                hosts = target.get("hosts")
                ports = target.get("ports")
                credentials = target.get("credentials")
                xml_target.add_element("hosts", hosts)
                xml_target.add_element("ports", ports)
                if credentials:
                    create_credentials_element(
                        xml_target.add_element("credentials"), credentials
                    )
        # Check target as attribute for legacy mode compatibility. Deprecated.
        elif target:
            cmd.set_attribute("target", target)
            if ports:
                cmd.set_attribute("ports", ports)
        else:
            raise RequiredArgument(
                function=self.start_scan.__name__, argument="targets"
            )

        if vt_selection:
            create_vt_selection_element(
                cmd.add_element("vt_selection"), vt_selection
            )

        return self._send_request_and_transform_response(cmd)

    def stop_scan(self, scan_id: str) -> T:
        """Stop a currently running scan.

        Args:
            scan_id: UUID identifier for a running scan.
        """
        if not scan_id:
            raise RequiredArgument(
                function=self.stop_scan.__name__, argument="scan_id"
            )

        cmd = XmlCommand("stop_scan")
        cmd.set_attribute("scan_id", scan_id)

        return self._send_request_and_transform_response(cmd)
