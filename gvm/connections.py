# -*- coding: utf-8 -*-
# Copyright (C) 2018 Greenbone Networks GmbH
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

import paramiko

from lxml import etree

from gvm.errors import GvmError


logger = logging.getLogger(__name__)

BUF_SIZE = 1024
DEFAULT_READ_TIMEOUT = 60 # in seconds
DEFAULT_TIMEOUT = 60 # in seconds
DEFAULT_GVM_PORT = 9390
DEFAULT_UNIX_SOCKET_PATH = '/usr/local/var/run/gvmd.sock'
MAX_SSH_DATA_LENGTH = 4095

class XmlReader:
    """
    Read a XML command until its closing element
    """

    def _start_xml(self):
        self._first_element = None
        self._parser = etree.XMLPullParser(('start', 'end'))

    def _is_end_xml(self):
        for action, obj in self._parser.read_events():
            if not self._first_element and action in 'start':
                self._first_element = obj.tag

            if self._first_element and action in 'end' and \
                    str(self._first_element) == str(obj.tag):
                return True
        return False

    def _feed_xml(self, data):
        try:
            self._parser.feed(data)
        except etree.ParseError as e:
            raise GvmError("Can't parse xml response. Response data "
                           "read {0}".format(data), e)


class GvmConnection(XmlReader):
    """
    Base class for establishing a connection to a remote server daemon.

    Arguments:
        timeout (int, optional): Timeout in seconds for the connection.
    """

    def __init__(self, timeout=DEFAULT_TIMEOUT):
        self._socket = None
        self._timeout = timeout

    def _read(self):
        return self._socket.recv(BUF_SIZE)

    def connect(self):
        """Establish a connection to a remote server
        """
        raise NotImplementedError

    def send(self, data):
        """Send data to the connected remote server

        Arguments:
            data (str or bytes): Data to be send to the server. Either utf-8
                encoded string or bytes.
        """
        if isinstance(data, str):
            self._socket.sendall(data.encode())
        else:
            self._socket.sendall(data)

    def read(self):
        """Read data from the remote server

        Returns:
            str: data as utf-8 encoded string
        """
        response = ''

        self._start_xml()

        now = time.time()

        break_timeout = now + self._timeout

        while True:
            data = self._read()

            if not data:
                # Connection was closed by server
                raise GvmError('Remote closed the connection')

            self._feed_xml(data)

            response += data.decode('utf-8', errors='ignore')

            if self._is_end_xml():
                break

            now = time.time()

            if now > break_timeout:
                raise GvmError('Timeout while reading the response')

        return response

    def disconnect(self):
        """Disconnect and close the connection to the remote server
        """
        try:
            if self._socket is not None:
                self._socket.close()
        except OSError as e:
            logger.debug('Connection closing error: %s', e)


class SSHConnection(GvmConnection):
    """
    SSH Class to connect, read and write from GVM via SSH

    Arguments:
        timeout (int, optional): Timeout in seconds for the connection.
        hostname (str, optional): DNS name or IP address of the remote server.
            Default is 127.0.0.1.
        port (int, optional): Port of the remote SSH server.
        username (str, optional): Username to use for SSH login.
        password (str, optional): Passwort to use for SSH login.
    """

    def __init__(self, *, timeout=DEFAULT_TIMEOUT, hostname='127.0.0.1',
                 port=22, username='gmp', password=''):
        super().__init__(timeout=timeout)

        self.hostname = hostname
        self.port = int(port)
        self.username = username
        self.password = password

    def _send_in_chunks(self, data, chunk_size):
        i_start = 0
        i_end = chunk_size
        sent_bytes = 0
        length = len(data)

        while sent_bytes < length:
            time.sleep(0.01)

            self._stdin.channel.send(data[i_start:i_end])

            i_start = i_end
            if i_end > length:
                i_end = length
            else:
                i_end = i_end + chunk_size

            sent_bytes += (i_end - i_start)

        return sent_bytes

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
                look_for_keys=False)
            self._stdin, self._stdout, self._stderr = self._socket.exec_command(
                "", get_pty=False)

        except (paramiko.BadHostKeyException,
                paramiko.AuthenticationException,
                paramiko.SSHException,
                ) as e:
            raise GvmError('SSH Connection failed', e)

    def _read(self):
        return self._stdout.channel.recv(BUF_SIZE)

    def send(self, data):
        if len(data) > MAX_SSH_DATA_LENGTH:
            self._send_in_chunks(data, MAX_SSH_DATA_LENGTH)
        else:
            self._stdin.channel.send(data)


class TLSConnection(GvmConnection):
    """
    TLS class to connect, read and write from a remote GVM daemon via TLS
    secured socket.

    Arguments:
        timeout (int, optional): Timeout in seconds for the connection.
        hostname (str, optional): DNS name or IP address of the remote TLS
            server.
        port (str, optional): Port for the TLS connection. Default is 9390.
        certfile (str, optional): Path to PEM encoded certificate file. See
            `python certificates`_ for details.
        cafile (str, optional): Path to PEM encoded CA file. See
            `python certificates`_ for details.
        keyfile (str, optional): Path to PEM encoded private key. See
            `python certificates`_ for details.
        password (str, optional): Password for the private key. If the password
            argument is not specified and a password is required it will be
            interactively prompt the user for a password.

    .. _python certificates:
        https://docs.python.org/3.5/library/ssl.html#certificates
    """

    def __init__(self, *, certfile=None, cafile=None, keyfile=None,
                 hostname='127.0.0.1', port=DEFAULT_GVM_PORT, password=None,
                 timeout=DEFAULT_TIMEOUT):
        super().__init__(timeout=timeout)

        self.hostname = hostname
        self.port = port
        self.certfile = certfile
        self.cafile = cafile
        self.keyfile = keyfile
        self.password = password

    def _new_socket(self):
        transport_socket = socketlib.socket(socketlib.AF_INET,
                                            socketlib.SOCK_STREAM)

        if self.certfile and self.cafile and self.keyfile:
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH,
                                                 cafile=self.cafile)
            context.check_hostname = False
            context.load_cert_chain(
                certfile=self.certfile, keyfile=self.keyfile,
                password=self.password)
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
        path (str, optional): Path to the socket.
        timeout (int, optional): Timeout in seconds for the connection.
    """

    def __init__(self, *, path=DEFAULT_UNIX_SOCKET_PATH,
                 timeout=DEFAULT_TIMEOUT, read_timeout=DEFAULT_READ_TIMEOUT):
        super().__init__(timeout=timeout)

        self.read_timeout = read_timeout
        self.path = path

    def connect(self):
        """Connect to the UNIX socket
        """
        self._socket = socketlib.socket(
            socketlib.AF_UNIX, socketlib.SOCK_STREAM)
        self._socket.settimeout(self._timeout)
        self._socket.connect(self.path)


class DebugConnection:

    def __init__(self, connection):
        self._connection = connection

    def read(self):
        data = self._connection.read()

        logger.debug('Read %s characters. Data %s', len(data), data)

        self.last_read_data = data
        return data

    def send(self, data):
        self.last_send_data = data

        logger.debug('Sending %s characters. Data %s', len(data), data)

        return self._connection.send(data)

    def connect(self):
        logger.debug('Connecting')

        return self._connection.connect()

    def disconnect(self):
        logger.debug('Disconnecting')

        return self._connection.disconnect()
