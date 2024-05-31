# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import base64
import errno
import hashlib
import logging
import socket as socketlib
import sys
from os import PathLike
from pathlib import Path
from time import time
from typing import Any, Callable, Optional, TextIO, Union

import paramiko
import paramiko.ssh_exception
import paramiko.transport

from gvm.errors import GvmError

from ._connection import BUF_SIZE, DEFAULT_TIMEOUT

logger = logging.getLogger("gvm.connections.ssh")

DEFAULT_SSH_PORT = 22
DEFAULT_SSH_USERNAME = "gmp"
DEFAULT_SSH_PASSWORD = ""
DEFAULT_HOSTNAME = "127.0.0.1"
DEFAULT_KNOWN_HOSTS_FILE = ".ssh/known_hosts"


class SSHConnection:
    """
    SSH Class to connect, read and write from GVM via SSH

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
        file: TextIO = sys.stdout,
        input: Callable[[], str] = input,
        exit: Callable[[str], Any] = sys.exit,
    ) -> None:
        """
        Create a new SSH connection instance.

        Args:
            timeout: Timeout in seconds for the connection.
            hostname: DNS name or IP address of the remote server. Default is
                127.0.0.1.
            port: Port of the remote SSH server. Default is port 22.
            username: Username to use for SSH login. Default is "gmp".
            password: Password to use for SSH login. Default is "".
        """
        self._client: Optional[paramiko.SSHClient] = None
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
        self._timeout = timeout
        self._file = file
        self._input = input
        self._exit = exit

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
                f"the known_hosts file {self.known_hosts_file.absolute()}: {e}"
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
            "be established.",
            file=self._file,
        )
        print(
            f"{key_type} key fingerprint is {sha64_fingerprint}.",
            file=self._file,
        )
        print(
            "Are you sure you want to continue connecting (yes/no)? ",
            end="",
            file=self._file,
        )

        add = self._input()
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
                    file=self._file,
                )

                save = self._input()
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
                        print(
                            "Please type 'yes' or 'no': ",
                            end="",
                            file=self._file,
                        )
                        save = self._input()
                break
            elif add == "no":
                self._exit("User denied key. Host key verification failed.")
            else:
                print("Please type 'yes' or 'no': ", end="", file=self._file)
                add = self._input()

    def _get_remote_host_key(self) -> paramiko.PKey:
        """Get the remote host key for ssh connection"""
        try:
            tmp_socket = socketlib.socket()
            tmp_socket.settimeout(self._timeout)
            tmp_socket.connect((self.hostname, self.port))
        except OSError as e:
            tmp_socket.close()
            raise GvmError(
                "Couldn't establish a connection to fetch the"
                f" remote server key: {e}"
            ) from None

        trans = paramiko.transport.Transport(tmp_socket)
        try:
            trans.start_client()
        except paramiko.SSHException as e:
            tmp_socket.close()
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
        finally:
            tmp_socket.close()

        return key

    def _ssh_authentication(self) -> None:
        """Search/add/save the servers key for the SSH authentication process"""

        if not self._client:
            raise GvmError("SSH Client not connected.")

        # set to reject policy (avoid MITM attacks)
        self._client.set_missing_host_key_policy(paramiko.RejectPolicy())

        # openssh is posix, so this might only a posix approach
        # https://stackoverflow.com/q/32945533
        try:
            # load the keys into paramiko and check if remote is in the list
            self._client.load_host_keys(filename=str(self.known_hosts_file))
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise GvmError(
                    "Something went wrong with reading "
                    f"the known_hosts file: {e}"
                ) from None

        hostkeys = self._client.get_host_keys()

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

    def _read(self) -> bytes:
        return self._stdout.channel.recv(BUF_SIZE)

    def send(self, data: bytes) -> None:
        self._send_all(data)

    def read(self) -> bytes:
        break_timeout = (
            time() + self._timeout if self._timeout is not None else None
        )

        data = self._read()

        if not data:
            # Connection was closed by server
            raise GvmError("Remote closed the connection")

        if break_timeout and time() > break_timeout:
            raise GvmError("Timeout while reading the response")

        return data

    def connect(self) -> None:
        """
        Connect to the SSH server and authenticate to it
        """
        self._client = paramiko.SSHClient()
        self._ssh_authentication()

        try:
            self._client.connect(
                hostname=self.hostname,
                username=self.username,
                password=self.password,
                timeout=self._timeout,
                port=int(self.port),
                allow_agent=False,
                look_for_keys=False,
            )

        except (
            paramiko.BadHostKeyException,
            paramiko.AuthenticationException,
            paramiko.SSHException,
            paramiko.ssh_exception.NoValidConnectionsError,
            ConnectionError,
        ) as e:
            raise GvmError(f"SSH Connection failed: {e}") from None

        self._stdin, self._stdout, self._stderr = self._client.exec_command(
            "", get_pty=False
        )

    def disconnect(self) -> None:
        """Disconnect and close the connection to the remote server"""
        try:
            if self._client is not None:
                self._client.close()
        except OSError as e:
            logger.debug("Connection closing error: %s", e)
            raise e

        if self._client is not None:
            self._client = None
            del self._stdin, self._stdout, self._stderr

    def finish_send(self) -> None:
        # shutdown socket for sending. only allow reading data afterwards
        self._stdout.channel.shutdown(socketlib.SHUT_WR)
