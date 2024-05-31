# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import socket as socketlib
from os import PathLike, fspath
from typing import Optional, Union

from gvm.errors import GvmError

from ._connection import DEFAULT_TIMEOUT, AbstractGvmConnection

DEFAULT_UNIX_SOCKET_PATH = "/run/gvmd/gvmd.sock"


class UnixSocketConnection(AbstractGvmConnection):
    """
    UNIX-Socket class to connect, read, write from a daemon via direct
    communicating UNIX-Socket
    """

    def __init__(
        self,
        *,
        path: Optional[Union[str, PathLike[str]]] = DEFAULT_UNIX_SOCKET_PATH,
        timeout: Optional[Union[int, float]] = DEFAULT_TIMEOUT,
    ) -> None:
        """
        Create a new UnixSocketConnection instance.

        Args:
            path: Path to the socket. Default is "/run/gvmd/gvmd.sock".
            timeout: Timeout in seconds for the connection. Default is 60 seconds.
        """
        super().__init__(timeout=timeout)

        self.path = (
            fspath(path) if path is not None else DEFAULT_UNIX_SOCKET_PATH
        )

    def connect(self) -> None:
        """Connect to the UNIX socket"""
        self._socket = socketlib.socket(
            socketlib.AF_UNIX, socketlib.SOCK_STREAM
        )
        self._socket.settimeout(self._timeout)
        try:
            self._socket.connect(self.path)
        except FileNotFoundError:
            raise GvmError(f"Socket {self.path} does not exist") from None
        except ConnectionError as e:
            raise GvmError(
                f"Could not connect to socket {self.path}. Error was {e}"
            ) from None
