# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from types import TracebackType
from typing import Callable, Optional, Type, Union

from gvm.connections import GvmConnection
from gvm.errors import GvmError

from .._protocol import GvmProtocol, T, str_transform
from ._gmp224 import GMPv224
from ._gmp225 import GMPv225
from .core import Response
from .core.requests import Version

SUPPORTED_GMP_VERSIONS = Union[GMPv224, GMPv225]


class GMP(GvmProtocol[T]):
    """Dynamically select supported GMP protocol of the remote manager daemon.

    Must be used as a `Context Manager
    <https://docs.python.org/3/reference/datamodel.html#context-managers>`_

    Example:

        .. code-block:: python

            from gvm.protocols.gmp import Gmp

            with Gmp(connection) as gmp:
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
        transform: Callable[[Response], T] = str_transform,  # type: ignore[assignment] # this should work with mypy 1.9.0 without an ignore
    ):
        super().__init__(connection, transform=transform)

    def determine_remote_gmp_version(self) -> str:
        """Determine the supported GMP version of the remote daemon"""
        self.connect()
        resp = self._send_command(Version.get_version())
        self.disconnect()

        version_el = resp.xml().find("version")
        if version_el is None or not version_el.text:
            raise GvmError(
                "Invalid response from manager daemon while requesting the "
                "version information."
            )

        return version_el.text

    def determine_supported_gmp(self) -> SUPPORTED_GMP_VERSIONS:
        """Determine supported GMP version of the remote daemon and return a
        corresponding Gmp class instance
        """
        version_str = self.determine_remote_gmp_version().split(".", 1)
        major_version = int(version_str[0])
        minor_version = int(version_str[1])
        # if major_version == 22 and minor_version == 4:
        # gmp_class = Gmpv224
        if major_version == 22 and minor_version == 4:
            gmp_class = GMPv224
        elif major_version == 22 and minor_version == 5:
            gmp_class = GMPv225
        else:
            raise GvmError(
                "Remote manager daemon uses an unsupported version of GMP. "
                f"The GMP version was {major_version}.{minor_version}"
            )

        return gmp_class(self._connection, transform=self._transform_callable)

    def __enter__(self):
        self._gmp = self.determine_supported_gmp()

        self._gmp.connect()

        return self._gmp

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self._gmp.disconnect()
        self._gmp = None
