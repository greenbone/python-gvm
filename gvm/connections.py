# -*- coding: utf-8 -*-
# Copyright (C) 2018 - 2019 Greenbone Networks GmbH
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
Module for connections to GVM server daemons like gvmd and ospd.
"""
import logging
import socket as socketlib
import ssl
import time

from typing import Optional, Union

import paramiko

from lxml import etree

from gvm.errors import GvmError


logger = logging.getLogger(__name__)

BUF_SIZE = 16 * 1024
DEFAULT_READ_TIMEOUT = 60  # in seconds
DEFAULT_TIMEOUT = 60  # in seconds
DEFAULT_GVM_PORT = 9390
DEFAULT_UNIX_SOCKET_PATH = "/var/run/gvmd.sock"
DEFAULT_SSH_PORT = 22
DEFAULT_HOSTNAME = '127.0.0.1'
MAX_SSH_DATA_LENGTH = 4095


class XmlReader:
    """
    Read a XML command until its closing element
    """

    def _start_xml(self):
        self._first_element = None
        # act on start and end element events and
        # allow huge text data (for report content)
        self._parser = etree.XMLPullParser(
            events=("start", "end"), huge_tree=True
        )

    def _is_end_xml(self):
        for action, obj in self._parser.read_events():
            if not self._first_element and action in "start":
                self._first_element = obj.tag

            if (
                self._first_element
                and action in "end"
                and str(self._first_element) == str(obj.tag)
            ):
                return True
        return False

    def _feed_xml(self, data):
        try:
            self._parser.feed(data)
        except etree.ParseError as e:
            raise GvmError(
                "Cannot parse XML response. Response data "
                "read {0}".format(data),
                e,
            )


class GvmConnection(XmlReader):
    """
    Base class for establishing a connection to a remote server daemon.

    Arguments:
        timeout: Timeout in seconds for the connection. None to
            wait indefinitely
    """

    def __init__(self, timeout: Optional[int] = DEFAULT_TIMEOUT):
        self._socket = None
        self._timeout = timeout

    def _read(self):
        return self._socket.recv(BUF_SIZE)

    def connect(self):
        """Establish a connection to a remote server
        """
        raise NotImplementedError

    def send(self, data: Union[bytes, str]):
        """Send data to the connected remote server

        Arguments:
            data: Data to be send to the server. Either utf-8 encoded string or
                bytes.
        """
        if self._socket is None:
            raise GvmError("Socket is not connected")

        if isinstance(data, str):
            self._socket.sendall(data.encode())
        else:
            self._socket.sendall(data)

    def read(self) -> str:
        """Read data from the remote server

        Returns:
            str: data as utf-8 encoded string
        """
        response = ""

        self._start_xml()

        if self._timeout is not None:
            now = time.time()

            break_timeout = now + self._timeout

        while True:
            data = self._read()

            if not data:
                # Connection was closed by server
                raise GvmError("Remote closed the connection")

            self._feed_xml(data)

            response += data.decode("utf-8", errors="ignore")

            if self._is_end_xml():
                break

            if self._timeout is not None:
                now = time.time()

                if now > break_timeout:
                    raise GvmError("Timeout while reading the response")

        return response

    def disconnect(self):
        """Disconnect and close the connection to the remote server
        """
        try:
            if self._socket is not None:
                self._socket.close()
        except OSError as e:
            logger.debug("Connection closing error: %s", e)

    def finish_send(self):
        """Indicate to the remote server you are done with sending data
        """
        # shutdown socket for sending. only allow reading data afterwards
        self._socket.shutdown(socketlib.SHUT_WR)


class SSHConnection(GvmConnection):
    """
    SSH Class to connect, read and write from GVM via SSH

    Arguments:
        timeout: Timeout in seconds for the connection.
        hostname: DNS name or IP address of the remote server. Default is
            127.0.0.1.
        port: Port of the remote SSH server. Default is port 22.
        username: Username to use for SSH login. Default is "gmp".
        password: Passwort to use for SSH login. Default is "".
    """

    def __init__(
        self,
        *,
        timeout: Optional[int] = DEFAULT_TIMEOUT,
        hostname: Optional[str] = DEFAULT_HOSTNAME,
        port: Optional[int] = DEFAULT_SSH_PORT,
        username: Optional[str] = "gmp",
        password: Optional[str] = ""
    ):
        super().__init__(timeout=timeout)

        self.hostname = hostname
        self.port = int(port)
        self.username = username
        self.password = password

    def _send_all(self, data):
        while data:
            sent = self._stdin.channel.send(data)

            if not sent:
                # Connection was closed by server
                raise GvmError("Remote closed the connection")

            data = data[sent:]

    def connect(self):
        """
        Connect to the SSH server and authenticate to it
        """
        self._socket = paramiko.SSHClient()
        self._socket.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            self._socket.connect(
                hostname=self.hostname,
                username=self.username,
                password=self.password,
                timeout=self._timeout,
                port=int(self.port),
                allow_agent=False,
                look_for_keys=False,
            )
            self._stdin, self._stdout, self._stderr = self._socket.exec_command(
                "", get_pty=False
            )

        except (
            paramiko.BadHostKeyException,
            paramiko.AuthenticationException,
            paramiko.SSHException,
        ) as e:
            raise GvmError("SSH Connection failed", e)

    def _read(self):
        return self._stdout.channel.recv(BUF_SIZE)

    def send(self, data: Union[bytes, str]):
        self._send_all(data)

    def finish_send(self):
        # shutdown socket for sending. only allow reading data afterwards
        self._stdout.channel.shutdown(socketlib.SHUT_WR)


class TLSConnection(GvmConnection):
    """
    TLS class to connect, read and write from a remote GVM daemon via TLS
    secured socket.

    Arguments:
        timeout: Timeout in seconds for the connection.
        hostname: DNS name or IP address of the remote TLS server.
        port: Port for the TLS connection. Default is 9390.
        certfile: Path to PEM encoded certificate file. See
            `python certificates`_ for details.
        cafile: Path to PEM encoded CA file. See `python certificates`_
            for details.
        keyfile: Path to PEM encoded private key. See `python certificates`_
            for details.
        password: Password for the private key. If the password argument is not
            specified and a password is required it will be interactively prompt
            the user for a password.

    .. _python certificates:
        https://docs.python.org/3/library/ssl.html#certificates
    """

    def __init__(
        self,
        *,
        certfile: Optional[str] = None,
        cafile: Optional[str] = None,
        keyfile: Optional[str] = None,
        hostname: Optional[str] = DEFAULT_HOSTNAME,
        port: Optional[int] = DEFAULT_GVM_PORT,
        password: Optional[str] = None,
        timeout: Optional[int] = DEFAULT_TIMEOUT
    ):
        super().__init__(timeout=timeout)

        self.hostname = hostname
        self.port = port
        self.certfile = certfile
        self.cafile = cafile
        self.keyfile = keyfile
        self.password = password

    def _new_socket(self):
        transport_socket = socketlib.socket(
            socketlib.AF_INET, socketlib.SOCK_STREAM
        )

        if self.certfile and self.cafile and self.keyfile:
            context = ssl.create_default_context(
                ssl.Purpose.SERVER_AUTH, cafile=self.cafile
            )
            context.check_hostname = False
            context.load_cert_chain(
                certfile=self.certfile,
                keyfile=self.keyfile,
                password=self.password,
            )
            sock = context.wrap_socket(transport_socket, server_side=False)
        else:
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            sock = context.wrap_socket(transport_socket)

        sock.settimeout(self._timeout)

        return sock

    def connect(self):
        self._socket = self._new_socket()
        self._socket.connect((self.hostname, int(self.port)))


class UnixSocketConnection(GvmConnection):
    """
    UNIX-Socket class to connect, read, write from a GVM server daemon via
    direct communicating UNIX-Socket

    Arguments:
        path: Path to the socket. Default is "/var/run/gvmd.sock".
        timeout: Timeout in seconds for the connection. Default is 60 seconds.
    """

    def __init__(
        self,
        *,
        path: Optional[str] = DEFAULT_UNIX_SOCKET_PATH,
        timeout: Optional[int] = DEFAULT_TIMEOUT
    ):
        super().__init__(timeout=timeout)

        self.path = path

    def connect(self):
        """Connect to the UNIX socket
        """
        self._socket = socketlib.socket(
            socketlib.AF_UNIX, socketlib.SOCK_STREAM
        )
        self._socket.settimeout(self._timeout)
        try:
            self._socket.connect(self.path)
        except FileNotFoundError:
            raise GvmError(
                "Socket {path} does not exist".format(path=self.path)
            ) from None
        except ConnectionError:
            raise GvmError(
                "Could not connect to socket {}".format(self.path)
            ) from None


class DebugConnection:
    """Wrapper around a connection for debugging purposes

    Allows to debug the connection flow including send and read data. Internally
    it uses the python `logging`_ framework to create debug messages. Please
    take a look at `the logging tutorial
    <https://docs.python.org/3/howto/logging.html#logging-basic-tutorial>`_
    for further details.

    Usage example:

    .. code-block:: python

        import logging

        logging.basicConfig(level=logging.DEBUG)

        socketconnection = UnixSocketConnection(path='/var/run/gvm.sock')
        connection = DebugConnection(socketconnection)
        gmp = Gmp(connection=connection)

    Arguments:
        connection: GvmConnection to observe

    .. _logging:
        https://docs.python.org/3/library/logging.html
    """

    def __init__(self, connection: GvmConnection):
        self._connection = connection

    def read(self) -> str:
        data = self._connection.read()

        logger.debug("Read %s characters. Data %s", len(data), data)

        self.last_read_data = data
        return data

    def send(self, data):
        self.last_send_data = data

        logger.debug("Sending %s characters. Data %s", len(data), data)

        return self._connection.send(data)

    def connect(self):
        logger.debug("Connecting")

        return self._connection.connect()

    def disconnect(self):
        logger.debug("Disconnecting")

        return self._connection.disconnect()

    def finish_send(self):
        logger.debug("Finish send")

        self._connection.finish_send()
