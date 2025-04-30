# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from ._connection import GvmConnection

logger = logging.getLogger("gvm.connections.debug")


class DebugConnection:
    """Wrapper around a connection for debugging purposes

    Allows to debug the connection flow including send and read data. Internally
    it uses the python `logging <https://docs.python.org/3/library/logging.html>`_
    framework to create debug messages. Please take a look at
    `the logging tutorial <https://docs.python.org/3/howto/logging.html#logging-basic-tutorial>`_
    for further details.

    Example:

    .. code-block:: python

        import logging

        logging.basicConfig(level=logging.DEBUG)

        socket_connection = UnixSocketConnection(path='/var/run/gvm.sock')
        connection = DebugConnection(socket_connection)
        gmp = Gmp(connection=connection)
    """

    def __init__(self, connection: GvmConnection):
        """
        Create a new DebugConnection instance.

        Args:
            connection: GvmConnection to observe
        """
        self._connection = connection

    def read(self) -> bytes:
        data = self._connection.read()

        logger.debug("Read %s characters. Data %r", len(data), data)

        self.last_read_data = data
        return data

    def send(self, data: bytes) -> None:
        self.last_send_data = data

        logger.debug("Sending %s characters. Data %r", len(data), data)

        return self._connection.send(data)

    def connect(self) -> None:
        logger.debug("Connecting")

        return self._connection.connect()

    def disconnect(self) -> None:
        logger.debug("Disconnecting")

        return self._connection.disconnect()

    def finish_send(self) -> None:
        logger.debug("Finish send")

        self._connection.finish_send()
