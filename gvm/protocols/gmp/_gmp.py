# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import warnings
from types import TracebackType
from typing import Callable, Optional, Type, Union

from gvm.__version__ import __version__
from gvm.connections import GvmConnection
from gvm.errors import GvmError
from gvm.protocols.core import Response

from .._protocol import GvmProtocol, T, str_transform
from ._gmp224 import GMPv224
from ._gmp225 import GMPv225
from ._gmp226 import GMPv226
from ._gmp227 import GMPv227
from ._gmp228 import GMPv228
from .requests import Version

SUPPORTED_GMP_VERSIONS = Union[
    GMPv224[T], GMPv225[T], GMPv226[T], GMPv227[T], GMPv228[T]
]
_SUPPORTED_GMP_VERSION_STRINGS = ["22.4", "22.5", "22.6", "22.7", "22.8"]


class GMP(GvmProtocol[T]):
    """Dynamically select supported GMP protocol of the remote manager daemon.

    Must be used as a `Context Manager <https://docs.python.org/3/reference/datamodel.html#context-managers>`_

    Example:

        .. code-block:: python

            from gvm.protocols.gmp import GMP

            with GMP(connection) as gmp:
                # gmp can be an instance of
                # gvm.protocols.gmp.GMPv224,
                # gvm.protocols.gmp.GMPv225,
                # gvm.protocols.gmp.GMPv226,
                # gvm.protocols.gmp.GMPv227,
                # or gvm.protocols.gmp.GMPv228
                # depending on the supported GMP version of the remote manager daemon
                resp = gmp.get_tasks()
    """

    def __init__(
        self,
        connection: GvmConnection,
        *,
        transform: Callable[[Response], T] = str_transform,  # type: ignore[assignment]
    ):
        """
        Create a new GMP instance.

        Args:
            connection: Connection to use to talk with the remote daemon. See
                :mod:`gvm.connections` for possible connection types.
            transform: Optional transform `callable <https://docs.python.org/3/library/functions.html#callable>`_
                to convert response data. After each request the callable gets passed the plain response data
                which can be used to check the data and/or conversion into different
                representations like a xml dom.

                See :mod:`gvm.transforms` for existing transforms.
        """
        super().__init__(connection, transform=transform)
        self._gmp: Optional[SUPPORTED_GMP_VERSIONS] = None

    def determine_remote_gmp_version(self) -> str:
        """Determine the supported GMP version of the remote daemon"""
        self.connect()
        resp = self._send_request(Version.get_version())
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
        corresponding GMP class instance
        """
        version_str = self.determine_remote_gmp_version().split(".", 1)
        major_version = int(version_str[0])
        minor_version = int(version_str[1])
        if major_version == 22 and minor_version == 4:
            gmp_class = GMPv224
        elif major_version == 22 and minor_version == 5:
            gmp_class = GMPv225
        elif major_version == 22 and minor_version == 6:
            gmp_class = GMPv226
        elif major_version == 22 and minor_version == 7:
            gmp_class = GMPv227
        elif major_version == 22 and minor_version >= 8:
            gmp_class = GMPv228
            if minor_version > 8:
                warnings.warn(
                    "Remote manager daemon uses a newer GMP version than "
                    f"supported by python-gvm {__version__}. Please update to "
                    "a newer release of python-gvm if possible. "
                    f"Remote GMP version is {major_version}.{minor_version}. "
                    f"Supported GMP versions are {', '.join(_SUPPORTED_GMP_VERSION_STRINGS)}."
                )
        else:
            raise GvmError(
                "Remote manager daemon uses an unsupported version of GMP. "
                f"The GMP version was {major_version}.{minor_version}"
                f"Supported GMP versions are {', '.join(_SUPPORTED_GMP_VERSION_STRINGS)}."
            )

        return gmp_class(self._connection, transform=self._transform_callable)  # type: ignore[arg-type]

    def __enter__(self) -> SUPPORTED_GMP_VERSIONS:  # type: ignore[override]
        """
        Returns the corresponding GMP class of the supported GMP version of the
        remote manager daemon.
        """
        self._gmp = self.determine_supported_gmp()

        self._gmp.connect()

        return self._gmp

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        if self._gmp:
            self._gmp.disconnect()
        self._gmp = None
