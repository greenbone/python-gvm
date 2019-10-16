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

"""
Module for communication with gvmd
"""
from typing import Any, Optional, Callable

from gvm.errors import GvmError

from gvm.protocols.base import GvmProtocol, GvmConnection

from gvm.protocols.gmpv7 import Gmp as Gmpv7
from gvm.protocols.gmpv8 import Gmp as Gmpv8
from gvm.protocols.gmpv9 import Gmp as Gmpv9

from gvm.transforms import EtreeCheckCommandTransform

from gvm.xml import XmlCommand


class Gmp(GvmProtocol):
    """Dynamically select supported GMP protocol of the remote manager daemon.

    Must be used as a `Context Manager
    <https://docs.python.org/3/reference/datamodel.html#context-managers>`_

    Example:

        .. code-block:: python

            from gvm.protocols.gmp import Gmp

            with Gmp(connection) as gmp:
                # gmp can be an instance of gvm.protocols.gmpv7.Gmp,
                # gvm.protocols.gmpv8.Gmp or gvm.protocols.gmpv9.Gmp depending
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
        transform: Optional[Callable[[str], Any]] = None
    ):
        super().__init__(connection, transform=EtreeCheckCommandTransform())
        self._gmp_transform = transform

    def __enter__(self):
        self.connect()
        resp = self._send_xml_command(XmlCommand("get_version"))
        self.disconnect()

        version_el = resp.find('version')
        if version_el is None:
            raise GvmError(
                'Invalid response from manager daemon while requesting the '
                'version information.'
            )

        version = version_el.text
        major_version = int(version[0])

        if major_version == 7:
            gmp_class = Gmpv7
        elif major_version == 8:
            gmp_class = Gmpv8
        elif major_version >= 9:
            gmp_class = Gmpv9
        else:
            raise GvmError(
                'Remote manager daemon uses an unsupported version of GMP. '
                'The GMP version was {}.'.format(version)
            )

        gmp = gmp_class(self._connection, transform=self._gmp_transform)
        gmp.connect()

        return gmp
