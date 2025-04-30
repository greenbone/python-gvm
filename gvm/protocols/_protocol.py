# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from types import TracebackType
from typing import Callable, Generic, Optional, Type, TypeVar

from gvm.connections import GvmConnection

from .core import Connection, Request, Response

T = TypeVar("T")
Self = TypeVar("Self", bound="GvmProtocol")


def str_transform(response: Response) -> str:
    return str(response)


class GvmProtocol(Generic[T]):
    """Base class for different GVM protocols"""

    def __init__(
        self,
        connection: GvmConnection,
        *,
        transform: Callable[[Response], T] = str_transform,  # type: ignore[assignment]
    ):
        """
        Create a new GvmProtocol instance.

        Args:
            connection: Connection to use to talk with the remote daemon. See
                :mod:`gvm.connections` for possible connection types.
            transform: Optional transform callable to convert response data.
                After each request the callable gets passed the plain response data
                which can be used to check the data and/or conversion into different
                representations like a xml dom.
        """
        self._connection = connection
        self._protocol = Connection()

        self._connected = False

        self._transform_callable = transform

    def __enter__(self: Self) -> Self:
        self.connect()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.disconnect()

    def _read(self) -> bytes:
        """Read a command response from gvmd

        Returns:
            str: Response from server.
        """
        return self._connection.read()

    def _send(self, data: bytes) -> None:
        """Send a command to the server

        Arguments:
            data (str): Data to be send over the connection to the server
        """
        self.connect()
        self._connection.send(data)

    def is_connected(self) -> bool:
        """Status of the current connection

        Returns:
            True if a connection to the remote server has been established.
        """
        return self._connected

    def connect(self) -> None:
        """Initiates a protocol connection

        Normally connect is not called directly. Either it is called
        automatically when sending a protocol command or when using a
        `with statement <https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers>`_.
        """
        if not self.is_connected():
            self._connection.connect()
            self._connected = True

    def disconnect(self) -> None:
        """Disconnect the connection

        Ends and closes the connection.
        """
        if self.is_connected():
            self._connection.disconnect()
            self._connected = False

        self._protocol.close()

    def send_command(self, cmd: str) -> str:
        """
        Send a string command to the remote daemon and return the response as
        string
        """
        return bytes(
            self._send_request(cmd.encode("utf-8", errors="ignore"))  # type: ignore[arg-type] # it seems mypy on Python < 3.11 can't handle bytes here
        ).decode("utf-8", errors="ignore")

    def _transform(self, response: Response) -> T:
        transform = self._transform_callable
        return transform(response)

    def _send_request(self, request: Request) -> Response:
        """
        Send a request to the remote daemon and return the response

        Args:
            request: The request to be send.
        """
        try:
            send_data = self._protocol.send(request)
            self._send(send_data)
            response: Optional[Response] = None
            while not response:
                received_data = self._read()
                response = self._protocol.receive_data(received_data)
            return response
        except Exception as e:
            self.disconnect()
            raise e

    def _send_request_and_transform_response(self, request: Request) -> T:
        """
        Send a request and transform its response using the transform callable.

        Args:
            request: The request to be send.
        """
        return self._transform(self._send_request(request))
