# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from unittest.mock import MagicMock

from gvm.protocols.core import InvalidStateError, Response
from gvm.protocols.core._connection import (
    AwaitingResponseState,
    Context,
    ErrorState,
    InitialState,
    ReceivingDataState,
)


class RequestMock:
    def __init__(self, data: bytes) -> None:
        self._data = data

    def __bytes__(self) -> bytes:
        return self._data


class InitialStateTestCase(unittest.TestCase):
    def test_receive_data(self) -> None:
        context = MagicMock(spec=Context)
        state = InitialState()
        state.__set_context__(context)

        with self.assertRaisesRegex(InvalidStateError, "Invalid State"):
            state.receive_data(b"some data")

    def test_close(self) -> None:
        context = MagicMock(spec=Context)
        state = InitialState()
        state.__set_context__(context)

        state.close()

        context.__set_state__.assert_not_called()

    def test_send(self) -> None:
        context = MagicMock(spec=Context)
        state = InitialState()
        state.__set_context__(context)
        request = RequestMock(b"some data")

        data = state.send(request)
        self.assertEqual(data, b"some data")

        self.assertIsInstance(
            context.__set_state__.call_args[0][0], AwaitingResponseState
        )


class AwaitingResponseStateTestCase(unittest.TestCase):

    def test_receive_data(self) -> None:
        context = MagicMock(spec=Context)
        request = RequestMock(b"<start>")
        state = AwaitingResponseState(request)
        state.__set_context__(context)

        response = state.receive_data(b"<element>")
        self.assertIsNone(response)

        self.assertIsInstance(
            context.__set_state__.call_args[0][0], ReceivingDataState
        )

    def test_close(self) -> None:
        context = MagicMock(spec=Context)
        request = RequestMock(b"<start>")
        state = AwaitingResponseState(request)
        state.__set_context__(context)

        state.close()

        self.assertIsInstance(
            context.__set_state__.call_args[0][0], InitialState
        )

    def test_send(self) -> None:
        context = MagicMock(spec=Context)
        request = RequestMock(b"<start>")
        state = AwaitingResponseState(request)
        state.__set_context__(context)

        with self.assertRaisesRegex(InvalidStateError, "Invalid State"):
            another_request = RequestMock(b"<element>")
            state.send(another_request)


class ErrorStateTestCase(unittest.TestCase):

    def test_receive_data(self) -> None:
        context = MagicMock(spec=Context)
        state = ErrorState()
        state.__set_context__(context)

        with self.assertRaisesRegex(
            InvalidStateError,
            "^The connection is in an error state. Please close the connection.$",
        ):
            state.receive_data(b"some data")

    def test_close(self) -> None:
        context = MagicMock(spec=Context)
        state = ErrorState()
        state.__set_context__(context)

        state.close()

        self.assertIsInstance(
            context.__set_state__.call_args[0][0], InitialState
        )

    def test_send(self) -> None:
        context = MagicMock(spec=Context)
        state = ErrorState()
        state.__set_context__(context)

        with self.assertRaisesRegex(
            InvalidStateError,
            "^The connection is in an error state. Please close the connection.$",
        ):
            state.receive_data(b"some data")


class ReceivingDataStateTestCase(unittest.TestCase):

    def test_receive_data(self) -> None:
        context = MagicMock(spec=Context)
        request = RequestMock(b"<start/>")
        state = ReceivingDataState(request)
        state.__set_context__(context)

        response = state.receive_data(b"<response>")
        self.assertIsNone(response)

        response = state.receive_data(b"</response>")
        self.assertIsNotNone(response)
        self.assertIsInstance(response, Response)
        self.assertEqual(response.data, b"<response></response>")  # type: ignore

        self.assertIsInstance(
            context.__set_state__.call_args[0][0], InitialState
        )

    def test_close(self) -> None:
        context = MagicMock(spec=Context)
        request = RequestMock(b"<start/>")
        state = ReceivingDataState(request)
        state.__set_context__(context)

        state.close()

        self.assertIsInstance(
            context.__set_state__.call_args[0][0], InitialState
        )

    def test_send(self) -> None:
        context = MagicMock(spec=Context)
        request = RequestMock(b"<start/>")
        state = ReceivingDataState(request)
        state.__set_context__(context)

        with self.assertRaisesRegex(InvalidStateError, "Invalid State"):
            another_request = RequestMock(b"<element>")
            state.send(another_request)
