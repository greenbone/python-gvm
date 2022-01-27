# -*- coding: utf-8 -*-
# Copyright (C) 2019-2022 Greenbone Networks GmbH
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
Module for communication with gvmd
"""
from typing import Any, Optional, Callable, Union

from gvm.errors import GvmClientError, GvmError

from gvm.protocols.base import GvmProtocol, GvmConnection

from gvm.protocols.gmpv208 import Gmp as Gmpv208
from gvm.protocols.gmpv214 import Gmp as Gmpv214
from gvm.protocols.gmpv2110 import Gmp as Gmpv2110

from gvm.transforms import EtreeCheckCommandTransform

from gvm.xml import XmlCommand

SUPPORTED_GMP_VERSIONS = Union[Gmpv208, Gmpv214]  # pylint: disable=invalid-name


class Gmp(GvmProtocol):
    """Dynamically select supported GMP protocol of the remote manager daemon.

    Must be used as a `Context Manager
    <https://docs.python.org/3/reference/datamodel.html#context-managers>`_

    Example:

        .. code-block:: python

            from gvm.protocols.gmp import Gmp

            with Gmp(connection).supported_gmp as gmp:
                # gmp can be an instance of gvm.protocols.gmpv208.Gmp,
                # gvm.protocols.gmpv214.Gmp depending
                # on the supported GMP version of the remote manager daemon
                resp = gmp.get_tasks()

    Attributes:
        connection: Connection to use to talk with the remote daemon. See
            :mod:`gvm.connections` for possible connection types.
        transform: Optional transform `callable`_ to convert response data.
            After each request the callable gets passed the plain response data
            which can be used to check the data and/or conversion into different
            representations like a xml dom.

            See :mod:`gvm.transforms` for existing transforms.

    .. _callable:
        https://docs.python.org/3/library/functions.html#callable
    """

    def __init__(
        self,
        connection: GvmConnection,
        *,
        transform: Optional[Callable[[str], Any]] = None,
    ):
        super().__init__(connection, transform=EtreeCheckCommandTransform())
        self._gmp_transform = transform

    def determine_remote_gmp_version(self) -> str:
        """Determine the supported GMP version of the remote daemon"""
        self.connect()
        resp = self._send_xml_command(XmlCommand("get_version"))
        self.disconnect()

        version_el = resp.find('version')
        if version_el is None:
            raise GvmError(
                'Invalid response from manager daemon while requesting the '
                'version information.'
            )

        return version_el.text

    def determine_supported_gmp(self) -> SUPPORTED_GMP_VERSIONS:
        """Determine supported GMP version of the remote daemon and return a
        corresponding Gmp class instance
        """
        version_str = self.determine_remote_gmp_version().split('.', 1)
        major_version = int(version_str[0])
        minor_version = int(version_str[1])
        if major_version == 20:
            gmp_class = Gmpv208
        elif major_version == 21 and minor_version == 4:
            gmp_class = Gmpv214
        elif major_version == 21 and minor_version == 10:
            gmp_class = Gmpv2110
        else:
            raise GvmError(
                'Remote manager daemon uses an unsupported version of GMP. '
                f'The GMP version was {major_version}.{minor_version}'
            )

        return gmp_class(self._connection, transform=self._gmp_transform)

    @property
    def supported_gmp(self):
        return self.determine_supported_gmp()

    def __enter__(self):
        raise GvmClientError(
            'You may not use Gmp for context directly. Please use property '
            'supported_gmp instead.'
        )
