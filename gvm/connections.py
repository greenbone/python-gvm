# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""
Module for connections to GVM server daemons like gvmd and ospd.
"""
import base64
import errno
import hashlib
import logging
import socket as socketlib
import ssl
import sys
import time
from abc import ABC, abstractmethod
from os import PathLike
from pathlib import Path
from typing import Optional, Protocol, Union, runtime_checkable

import paramiko
import paramiko.ssh_exception
import paramiko.transport
from lxml import etree

from gvm.errors import GvmError

logger = logging.getLogger(__name__)

BUF_SIZE = 16 * 1024
DEFAULT_READ_TIMEOUT = 60  # in seconds
DEFAULT_TIMEOUT = 60  # in seconds
DEFAULT_GVM_PORT = 9390
DEFAULT_UNIX_SOCKET_PATH = "/run/gvmd/gvmd.sock"
DEFAULT_SSH_PORT = 22
DEFAULT_SSH_USERNAME = "gmp"
DEFAULT_SSH_PASSWORD = ""
DEFAULT_HOSTNAME = "127.0.0.1"
DEFAULT_KNOWN_HOSTS_FILE = ".ssh/known_hosts"
MAX_SSH_DATA_LENGTH = 4095

Data = Union[str, bytes]


@runtime_checkable
class GvmConnection(Protocol):
    def connect(self) -> None: ...

    def disconnect(self) -> None: ...

    def send(self, data: Data) -> None: ...

    def read(self) -> str: ...

    def finish_send(self): ...


class XmlReader:
    """
    Read a XML command until its closing element
    """

    def start_xml(self) -> None:
        self._first_element = None
        # act on start and end element events and
        # allow huge text data (for report content)
        self._parser = etree.XMLPullParser(
            events=("start", "end"), huge_tree=True
        )

    def is_end_xml(self) -> bool:
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

    def feed_xml(self, data: Data) -> None:
        try:
            self._parser.feed(data)
        except etree.ParseError as e:
            raise GvmError(
                f"Cannot parse XML response. Response data read {data}",
                e,
            ) from None


class AbstractGvmConnection(ABC):
    """
    Base class for establishing a connection to a remote server daemon.

    Arguments:
        timeout: Timeout in seconds for the connection. None to
            wait indefinitely
    """

    def __init__(self, timeout: Optional[Union[int, float]] = DEFAULT_TIMEOUT):
        self._socket = None
        self._timeout = timeout if timeout is not None else DEFAULT_TIMEOUT
        self._xml_reader = XmlReader()

    def _read(self) -> bytes:
        if self._socket is None:
            raise GvmError("Socket is not connected")

        return self._socket.recv(BUF_SIZE)

    @abstractmethod
    def connect(self) -> None:
        """Establish a connection to a remote server"""
        raise NotImplementedError

    def send(self, data: Data) -> None:
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

        self._xml_reader.start_xml()

        break_timeout = (
            time.time() + self._timeout if self._timeout is not None else None
        )

        while True:
            data = self._read()

            if not data:
                # Connection was closed by server
                raise GvmError("Remote closed the connection")

            self._xml_reader.feed_xml(data)

            response += data.decode("utf-8", errors="ignore")

            if self._xml_reader.is_end_xml():
                break

            if break_timeout and time.time() > break_timeout:
                raise GvmError("Timeout while reading the response")

        return response

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


class SSHConnection(AbstractGvmConnection):
    """
    SSH Class to connect, read and write from GVM via SSH

    Arguments:
        timeout: Timeout in seconds for the connection.
        hostname: DNS name or IP address of the remote server. Default is
            127.0.0.1.
        port: Port of the remote SSH server. Default is port 22.
        username: Username to use for SSH login. Default is "gmp".
        password: Password to use for SSH login. Default is "".
    """

    def __init__(
        self,
        *,
        timeout: Optional[Union[int, float]] = DEFAULT_TIMEOUT,
        hostname: Optional[str] = DEFAULT_HOSTNAME,
        port: Optional[int] = DEFAULT_SSH_PORT,
        username: Optional[str] = DEFAULT_SSH_USERNAME,
        password: Optional[str] = DEFAULT_SSH_PASSWORD,
        known_hosts_file: Optional[Union[str, PathLike]] = None,
        auto_accept_host: Optional[bool] = None,
    ) -> None:
        super().__init__(timeout)
        self.hostname = hostname if hostname is not None else DEFAULT_HOSTNAME
        self.port = int(port) if port is not None else DEFAULT_SSH_PORT
        self.username = (
            username if username is not None else DEFAULT_SSH_USERNAME
        )
        self.password = (
            password if password is not None else DEFAULT_SSH_PASSWORD
        )
        self.known_hosts_file = (
            Path(known_hosts_file)
            if known_hosts_file is not None
            else Path.home() / DEFAULT_KNOWN_HOSTS_FILE
        )
        self.auto_accept_host = auto_accept_host

    def _send_all(self, data: bytes) -> int:
        """Returns the sum of sent bytes if success"""
        sent_sum = 0
        while data:
            sent = self._stdin.channel.send(data)

            if not sent:
                # Connection was closed by server
                raise GvmError("Remote closed the connection")

            sent_sum += sent

            data = data[sent:]
        return sent_sum

    def _auto_accept_host(
        self, hostkeys: paramiko.HostKeys, key: paramiko.PKey
    ) -> None:
        if self.port == DEFAULT_SSH_PORT:
            hostkeys.add(self.hostname, key.get_name(), key)
        elif self.port != DEFAULT_SSH_PORT:
            hostkeys.add(
                "[" + self.hostname + "]:" + str(self.port),
                key.get_name(),
                key,
            )
        try:
            hostkeys.save(filename=str(self.known_hosts_file))
        except OSError as e:
            raise GvmError(
                "Something went wrong with writing "
                f"the known_hosts file: {e}"
            ) from None

        key_type = key.get_name().replace("ssh-", "").upper()

        logger.info(
            "Warning: Permanently added '%s' (%s) to "
            "the list of known hosts.",
            self.hostname,
            key_type,
        )

    def _ssh_authentication_input_loop(
        self, hostkeys: paramiko.HostKeys, key: paramiko.PKey
    ) -> None:
        # Ask user for permission to continue
        # let it look like openssh
        sha64_fingerprint = base64.b64encode(
            hashlib.sha256(base64.b64decode(key.get_base64())).digest()
        ).decode("utf-8")[:-1]
        key_type = key.get_name().replace("ssh-", "").upper()

        print(
            f"The authenticity of host '{self.hostname}' can't "
            "be established."
        )
        print(f"{key_type} key fingerprint is {sha64_fingerprint}.")
        print("Are you sure you want to continue connecting (yes/no)? ", end="")

        add = input()
        while True:
            if add == "yes":
                if self.port == DEFAULT_SSH_PORT:
                    hostkeys.add(self.hostname, key.get_name(), key)
                elif self.port != DEFAULT_SSH_PORT:
                    hostkeys.add(
                        "[" + self.hostname + "]:" + str(self.port),
                        key.get_name(),
                        key,
                    )

                # ask user if the key should be added permanently
                print(
                    f"Do you want to add {self.hostname} "
                    "to known_hosts (yes/no)? ",
                    end="",
                )

                save = input()
                while True:
                    if save == "yes":
                        try:
                            hostkeys.save(filename=str(self.known_hosts_file))
                        except OSError as e:
                            raise GvmError(
                                "Something went wrong with writing "
                                f"the known_hosts file: {e}"
                            ) from None

                        logger.info(
                            "Warning: Permanently added '%s' (%s) to "
                            "the list of known hosts.",
                            self.hostname,
                            key_type,
                        )
                        break
                    elif save == "no":
                        logger.info(
                            "Warning: Host '%s' (%s) not added to "
                            "the list of known hosts.",
                            self.hostname,
                            key_type,
                        )
                        break
                    else:
                        print("Please type 'yes' or 'no': ", end="")
                        save = input()
                break
            elif add == "no":
                sys.exit("User denied key. Host key verification failed.")
            else:
                print("Please type 'yes' or 'no': ", end="")
                add = input()

    def _get_remote_host_key(self) -> paramiko.PKey:
        """Get the remote host key for ssh connection"""
        try:
            tmp_socket = socketlib.socket()
            tmp_socket.settimeout(self._timeout)
            tmp_socket.connect((self.hostname, self.port))
        except OSError as e:
            raise GvmError(
                "Couldn't establish a connection to fetch the"
                f" remote server key: {e}"
            ) from None

        trans = paramiko.transport.Transport(tmp_socket)
        try:
            trans.start_client()
        except paramiko.SSHException as e:
            raise GvmError(
                f"Couldn't fetch the remote server key: {e}"
            ) from None
        key = trans.get_remote_server_key()
        try:
            trans.close()
        except paramiko.SSHException as e:
            raise GvmError(
                f"Couldn't close the connection to the remote server key: {e}"
            ) from None
        return key

    def _ssh_authentication(self) -> None:
        """Search/add/save the servers key for the SSH authentication process"""

        # set to reject policy (avoid MITM attacks)
        self._socket.set_missing_host_key_policy(paramiko.RejectPolicy())
        # openssh is posix, so this might only a posix approach
        # https://stackoverflow.com/q/32945533
        try:
            # load the keys into paramiko and check if remote is in the list
            self._socket.load_host_keys(filename=str(self.known_hosts_file))
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise GvmError(
                    "Something went wrong with reading "
                    f"the known_hosts file: {e}"
                ) from None
        hostkeys = self._socket.get_host_keys()
        # Switch based on SSH Port
        if self.port == DEFAULT_SSH_PORT:
            hostname = self.hostname
        else:
            hostname = f"[{self.hostname}]:{self.port}"

        if not hostkeys.lookup(hostname):
            # Key not found, so connect to remote and fetch the key
            # with the paramiko Transport protocol
            key = self._get_remote_host_key()
            if self.auto_accept_host:
                self._auto_accept_host(hostkeys=hostkeys, key=key)
            else:
                self._ssh_authentication_input_loop(hostkeys=hostkeys, key=key)

    def connect(self) -> None:
        """
        Connect to the SSH server and authenticate to it
        """
        self._socket = paramiko.SSHClient()
        self._ssh_authentication()

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
            paramiko.ssh_exception.NoValidConnectionsError,
            ConnectionError,
        ) as e:
            raise GvmError(f"SSH Connection failed: {e}") from None

    def _read(self) -> bytes:
        return self._stdout.channel.recv(BUF_SIZE)

    def send(self, data: Data) -> None:
        if isinstance(data, str):
            self._send_all(data.encode())
        else:
            self._send_all(data)

    def finish_send(self) -> None:
        # shutdown socket for sending. only allow reading data afterwards
        self._stdout.channel.shutdown(socketlib.SHUT_WR)

    def disconnect(self) -> None:
        """Disconnect and close the connection to the remote server"""
        try:
            if self._socket is not None:
                self._socket.close()
        except OSError as e:
            logger.debug("Connection closing error: %s", e)
            raise e
        except AttributeError:
            logger.debug("Connection might already be closed. No socket found.")

        if self._socket:
            del self._socket, self._stdin, self._stdout, self._stderr


class TLSConnection(AbstractGvmConnection):
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
        timeout: Optional[Union[int, float]] = DEFAULT_TIMEOUT,
    ) -> None:
        super().__init__(timeout=timeout)

        self.hostname = hostname if hostname is not None else DEFAULT_HOSTNAME
        self.port = port if port is not None else DEFAULT_GVM_PORT
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
            context.minimum_version = ssl.TLSVersion.TLSv1_2
        else:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.minimum_version = ssl.TLSVersion.TLSv1_2
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

        sock = context.wrap_socket(transport_socket, server_side=False)

        sock.settimeout(self._timeout)

        return sock

    def connect(self) -> None:
        self._socket = self._new_socket()
        self._socket.connect((self.hostname, int(self.port)))

    def disconnect(self):
        """Close the SSL layer then disconnect from the remote server"""
        try:
            if self._socket is not None:
                self._socket = self._socket.unwrap()
        except OSError as e:
            logger.debug("Connection closing error: %s", e)
        return super().disconnect()


class UnixSocketConnection(AbstractGvmConnection):
    """
    UNIX-Socket class to connect, read, write from a daemon via direct
    communicating UNIX-Socket

    Arguments:
        path: Path to the socket. Default is "/run/gvmd/gvmd.sock".
        timeout: Timeout in seconds for the connection. Default is 60 seconds.
    """

    def __init__(
        self,
        *,
        path: Optional[str] = DEFAULT_UNIX_SOCKET_PATH,
        timeout: Optional[Union[int, float]] = DEFAULT_TIMEOUT,
    ) -> None:
        super().__init__(timeout=timeout)

        self.path = path if path is not None else DEFAULT_UNIX_SOCKET_PATH

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

        socket_connection = UnixSocketConnection(path='/var/run/gvm.sock')
        connection = DebugConnection(socket_connection)
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

    def send(self, data: Data) -> None:
        self.last_send_data = data

        logger.debug("Sending %s characters. Data %s", len(data), data)

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
