# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import AnyStr, Optional, Protocol

from lxml import etree

from gvm.errors import GvmError

from ._request import Request
from ._response import Response


class XmlReader:
    """
    Read a XML command until its closing element
    """

    def start_xml(self) -> None:
        self._first_element: Optional[etree._Element] = None
        # act on start and end element events and
        # allow huge text data (for report content)
        self._parser = etree.XMLPullParser(
            events=("start", "end"), huge_tree=True
        )

    def is_end_xml(self) -> bool:
        for action, obj in self._parser.read_events():
            if not self._first_element and action in "start":
                self._first_element = obj.tag  # type: ignore

            if (
                self._first_element
                and action in "end"
                and str(self._first_element) == str(obj.tag)  # type: ignore
            ):
                return True
        return False

    def feed_xml(self, data: AnyStr) -> None:
        try:
            self._parser.feed(data)
        except etree.ParseError as e:
            raise GvmError(
                f"Cannot parse XML response. Response data read {data!r}",
                e,
            ) from None


class InvalidStateError(GvmError):
    """
    Error raised if the Connection would be moved into an invalid state
    """

    def __init__(self, message: str = "Invalid State", *args):
        super().__init__(message, *args)


class State(Protocol):
    def __set_context__(self, context: "Context") -> None: ...
    def send(self, request: Request) -> bytes: ...
    def receive_data(self, data: bytes) -> Optional[Response]: ...
    def close(self) -> None: ...


class Context(Protocol):
    def __set_state__(self, state: State) -> None: ...


class AbstractState:
    _context: Context

    def __set_context__(self, context: Context) -> None:
        self._context = context

    def set_next_state(self, next_state: State) -> None:
        self._context.__set_state__(next_state)


class InitialState(AbstractState):
    def send(self, request: Request) -> bytes:
        self.set_next_state(AwaitingResponseState(request))
        return bytes(request)

    def receive_data(self, data: bytes) -> Optional[Response]:
        raise InvalidStateError()

    def close(self) -> None:
        # nothing to do
        return


class AwaitingResponseState(AbstractState):
    def __init__(self, request: Request) -> None:
        self._request = request

    def send(self, request: Request) -> bytes:
        raise InvalidStateError()

    def close(self) -> None:
        self.set_next_state(InitialState())

    def receive_data(self, data: bytes) -> Optional[Response]:
        next_state = ReceivingDataState(self._request)
        self.set_next_state(next_state)
        return next_state.receive_data(data)


class ErrorState(AbstractState):
    message = (
        "The connection is in an error state. Please close the connection."
    )

    def send(self, request: Request) -> bytes:
        raise InvalidStateError(self.message)

    def close(self) -> None:
        self.set_next_state(InitialState())

    def receive_data(self, data: bytes) -> Optional[Response]:
        raise InvalidStateError(self.message)


class ReceivingDataState(AbstractState):
    def __init__(self, request: Request) -> None:
        self._request = request
        self._data = bytearray()
        self._reader = XmlReader()
        self._reader.start_xml()

    def send(self, request: Request) -> bytes:
        raise InvalidStateError()

    def close(self) -> None:
        self.set_next_state(InitialState())

    def receive_data(self, data: bytes) -> Optional[Response]:
        self._data += data
        try:
            self._reader.feed_xml(data)
        except GvmError as e:
            self.set_next_state(ErrorState())
            raise e

        if not self._reader.is_end_xml():
            return None

        self.set_next_state(InitialState())
        return Response(data=bytes(self._data), request=self._request)


class Connection:
    """
    This is a [SansIO](https://sans-io.readthedocs.io) connection for GMP

    It is responsible for creating bytes from GMP XML requests and transforming
    XML response data into GMP responses.
    """

    def __init__(self) -> None:
        self.__set_state__(InitialState())

    def send(self, request: Request) -> bytes:
        """
        Create data from a request to be send

        Returns:
            The data for a request that can be send for example over a socket

        Raises:
            An InvalidStateError if no request can be send currently. For
            example when waiting for a response to a previous request.
        """
        return self._state.send(request)

    def receive_data(self, data: bytes) -> Optional[Response]:
        """
        Feed received data a response is complete

        Returns:
            A Response if the response data is complete and None if data is
            still to be received.

        Raises:
            An InvalidStateError if no data can be received currently. For
            example if no request is send yet.
        """
        return self._state.receive_data(data)

    def close(self) -> None:
        """
        Close the connection and reset the state of the protocol

        Afterwards the connection can be reused for sending a new request.
        """
        return self._state.close()

    def __set_state__(self, state: State) -> None:
        self._state = state
        self._state.__set_context__(self)
