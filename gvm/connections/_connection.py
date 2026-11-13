# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import socket as socketlib
from abc import ABC, abstractmethod
from time import time
from typing import Protocol, runtime_checkable

from gvm.errors import GvmError

BUF_SIZE = 16 * 1024

DEFAULT_TIMEOUT = 60  # in seconds

logger = logging.getLogger(__name__)


@runtime_checkable
class GvmConnection(Protocol):
    """
    Python `protocol <https://docs.python.org/3/library/typing.html#typing.Protocol>`_
    for GvmConnection classes.
    """

    def connect(self) -> None:
        """Establish a connection to a remote server"""

    def disconnect(self) -> None:
        """Send data to the connected remote server

        Arguments:
            data: Data to be send to the server. Either utf-8 encoded string or
                bytes.
        """

    def send(self, data: bytes) -> None:
        """Send data to the connected remote server

        Args:
            data: Data to be send to the server as bytes.
        """

    def read(self) -> bytes:
        """Read data from the remote server

        Returns:
            data as bytes
        """

    def finish_send(self):
        """Indicate to the remote server you are done with sending data"""


class AbstractGvmConnection(ABC):
    """
    Base class for establishing a connection to a remote server daemon.

    Arguments:
        timeout: Timeout in seconds for the connection. None to
            wait indefinitely
    """

    def __init__(self, timeout: int | float | None = DEFAULT_TIMEOUT):
        self._socket: socketlib.SocketType | None = None
        self._timeout = timeout if timeout is not None else DEFAULT_TIMEOUT

    def _read(self) -> bytes:
        if self._socket is None:
            raise GvmError("Socket is not connected")

        return self._socket.recv(BUF_SIZE)

    @abstractmethod
    def connect(self) -> None:
        """Establish a connection to a remote server"""
        raise NotImplementedError

    def send(self, data: bytes) -> None:
        """Send data to the connected remote server

        Args:
            data: Data to be send to the server as bytes.

        Raises:
            GvmError: If the socket is not connected or the remote server
                has closed the connection. In the latter case the connection
                needs to be re-established via :py:meth:`connect`.
        """
        if self._socket is None:
            raise GvmError("Socket is not connected")

        try:
            self._socket.sendall(data)
        except ConnectionError as e:
            # Connection was closed by server, e.g. after an error response
            raise GvmError(
                f"Remote closed the connection. Error was {e}"
            ) from e

    def read(self) -> bytes:
        """Read data from the remote server

        Returns:
            data as bytes
        """
        break_timeout = (
            time() + self._timeout if self._timeout is not None else None
        )

        try:
            data = self._read()
        except ConnectionError as e:
            # Connection was reset by server
            raise GvmError(
                f"Remote closed the connection. Error was {e}"
            ) from e

        if not data:
            # Connection was closed by server
            raise GvmError("Remote closed the connection")

        if break_timeout and time() > break_timeout:
            raise GvmError("Timeout while reading the response")

        return data

    def disconnect(self) -> None:
        """Disconnect and close the connection to the remote server"""
        try:
            if self._socket is not None:
                self._socket.close()
        except OSError as e:
            logger.debug("Connection closing error: %s", e)

    def finish_send(self):
        """Indicate to the remote server you are done with sending data"""
        if self._socket is not None:
            # shutdown socket for sending. only allow reading data afterwards
            self._socket.shutdown(socketlib.SHUT_WR)
