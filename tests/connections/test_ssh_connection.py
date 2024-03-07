# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import paramiko

from gvm.connections import (
    DEFAULT_HOSTNAME,
    DEFAULT_KNOWN_HOSTS_FILE,
    DEFAULT_SSH_PASSWORD,
    DEFAULT_SSH_PORT,
    DEFAULT_SSH_USERNAME,
    GvmConnection,
    SSHConnection,
)
from gvm.errors import GvmError


class AbortException(Exception):
    """Just for testing purposes"""


class SSHConnectionTestCase(unittest.TestCase):
    # pylint: disable=protected-access, invalid-name
    def setUp(self):
        self.known_hosts_file = Path("known_hosts")
        self.known_hosts_file.write_text(
            "127.0.0.1 ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBOZWi"
            "fs+DoMqIa5Nr0wiVrzQNpMbUwaLzuSTN6rNrYA\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.known_hosts_file.unlink(missing_ok=True)

    def test_init_no_args(self):
        ssh_connection = SSHConnection()

        self.check_ssh_connection_for_default_values(ssh_connection)

    def test_init_with_none(self):
        ssh_connection = SSHConnection(
            timeout=None, hostname=None, port=None, username=None, password=None
        )

        self.check_ssh_connection_for_default_values(ssh_connection)

    def check_ssh_connection_for_default_values(
        self, ssh_connection: SSHConnection
    ):
        self.assertIsInstance(ssh_connection, SSHConnection)
        self.assertEqual(ssh_connection.hostname, DEFAULT_HOSTNAME)
        self.assertEqual(ssh_connection.port, DEFAULT_SSH_PORT)
        self.assertEqual(ssh_connection.username, DEFAULT_SSH_USERNAME)
        self.assertEqual(ssh_connection.password, DEFAULT_SSH_PASSWORD)
        self.assertEqual(
            ssh_connection.known_hosts_file,
            Path.home() / DEFAULT_KNOWN_HOSTS_FILE,
        )

    def test_connect_error(self):
        ssh_connection = SSHConnection(known_hosts_file=self.known_hosts_file)
        with self.assertRaises(GvmError, msg="SSH Connection failed"):
            ssh_connection.connect()

    def test_connect_error_auto_accept_host(self):
        ssh_connection = SSHConnection(
            known_hosts_file=self.known_hosts_file, auto_accept_host=True
        )
        with self.assertRaises(GvmError, msg="SSH Connection failed"):
            ssh_connection.connect()

    def test_connect(self):
        with patch("paramiko.SSHClient") as SSHClientMock:
            client_mock = SSHClientMock.return_value
            client_mock.exec_command.return_value = ["a", "b", "c"]
            ssh_connection = SSHConnection(
                known_hosts_file=self.known_hosts_file
            )

            ssh_connection.connect()
            self.assertEqual(ssh_connection._stdin, "a")
            self.assertEqual(ssh_connection._stdout, "b")
            self.assertEqual(ssh_connection._stderr, "c")
            ssh_connection.disconnect()

    def test_connect_auto_accept_host(self):
        with patch("paramiko.SSHClient", autospec=True) as SSHClientMock:
            client_mock = SSHClientMock.return_value
            client_mock.exec_command.return_value = ["a", "b", "c"]
            ssh_connection = SSHConnection(
                known_hosts_file=self.known_hosts_file, auto_accept_host=True
            )

            ssh_connection.connect()
            self.assertEqual(ssh_connection._stdin, "a")
            self.assertEqual(ssh_connection._stdout, "b")
            self.assertEqual(ssh_connection._stderr, "c")
            ssh_connection.disconnect()

    def test_connect_unknown_host(self):
        ssh_connection = SSHConnection(
            hostname="0.0.0.1",
            known_hosts_file=self.known_hosts_file,
            timeout=1.0,
        )
        with self.assertRaises(
            GvmError,
            msg=(
                "Could'nt establish a connection to fetch the remote "
                "server key: [Errno 65] No route to host"
            ),
        ):
            ssh_connection.connect()

    def test_connect_denied_known_hosts_file(self):
        self.known_hosts_file.chmod(0000)

        ssh_connection = SSHConnection(
            hostname="0.0.0.1", known_hosts_file=self.known_hosts_file
        )
        with self.assertRaises(
            GvmError,
            msg=(
                "Could'nt establish a connection to fetch the remote "
                "server key: [Errno 65] No route to host"
            ),
        ):
            ssh_connection.connect()

    def test_connect_no_known_hosts_file(self):
        self.known_hosts_file.unlink(missing_ok=True)

        ssh_connection = SSHConnection(
            hostname="0.0.0.1",
            known_hosts_file=self.known_hosts_file,
            timeout=1.0,
        )
        with self.assertRaises(
            GvmError,
            msg=(
                "Could'nt establish a connection to fetch the remote "
                "server key: [Errno 65] No route to host"
            ),
        ):
            ssh_connection.connect()

    @patch("builtins.print")
    def test_connect_adding_and_save_hostkey(self, _print_mock):
        input_mock = MagicMock(spec=input)
        key_io = StringIO(
            """-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACB69SvZKJh/9VgSL0G27b5xVYa8nethH3IERbi0YqJDXwAAAKhjwAdrY8AH
awAAAAtzc2gtZWQyNTUxOQAAACB69SvZKJh/9VgSL0G27b5xVYa8nethH3IERbi0YqJDXw
AAAEA9tGQi2IrprbOSbDCF+RmAHd6meNSXBUQ2ekKXm4/8xnr1K9komH/1WBIvQbbtvnFV
hryd62EfcgRFuLRiokNfAAAAI2FsZXhfZ2F5bm9yQEFsZXhzLU1hY0Jvb2stQWlyLmxvY2
FsAQI=
            -----END OPENSSH PRIVATE KEY-----"""
        )
        key = paramiko.Ed25519Key.from_private_key(key_io)
        key_type = key.get_name().replace("ssh-", "").upper()
        hostname = "0.0.0.0"
        input_mock.side_effect = ["yes", "yes"]
        ssh_connection = SSHConnection(
            hostname=hostname,
            known_hosts_file=self.known_hosts_file,
            input=input_mock,
        )
        keys = self.known_hosts_file.read_text(encoding="utf-8")
        self.assertEqual(
            keys,
            "127.0.0.1 ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBOZWi"
            "fs+DoMqIa5Nr0wiVrzQNpMbUwaLzuSTN6rNrYA\n",
        )

        with self.assertLogs("gvm.connections", level="INFO") as cm:
            hostkeys = paramiko.HostKeys(filename=str(self.known_hosts_file))
            ssh_connection._ssh_authentication_input_loop(
                hostkeys=hostkeys, key=key
            )
            keys = self.known_hosts_file.read_text(encoding="utf-8")

            self.assertEqual(
                cm.output,
                [
                    "INFO:gvm.connections.ssh:Warning: "
                    f"Permanently added '{hostname}' ({key_type}) to "
                    "the list of known hosts."
                ],
            )
            self.assertEqual(
                keys,
                "127.0.0.1 ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBOZWi"
                "fs+DoMqIa5Nr0wiVrzQNpMbUwaLzuSTN6rNrYA\n"
                f"0.0.0.0 {key.get_name()} {key.get_base64()}\n",
            )

    @patch("builtins.print")
    def test_connect_adding_and_dont_save_hostkey(self, _print_mock):
        input_mock = MagicMock(spec=input)
        key_io = StringIO(
            """-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACB69SvZKJh/9VgSL0G27b5xVYa8nethH3IERbi0YqJDXwAAAKhjwAdrY8AH
awAAAAtzc2gtZWQyNTUxOQAAACB69SvZKJh/9VgSL0G27b5xVYa8nethH3IERbi0YqJDXw
AAAEA9tGQi2IrprbOSbDCF+RmAHd6meNSXBUQ2ekKXm4/8xnr1K9komH/1WBIvQbbtvnFV
hryd62EfcgRFuLRiokNfAAAAI2FsZXhfZ2F5bm9yQEFsZXhzLU1hY0Jvb2stQWlyLmxvY2
FsAQI=
            -----END OPENSSH PRIVATE KEY-----"""
        )
        key = paramiko.Ed25519Key.from_private_key(key_io)
        key_type = key.get_name().replace("ssh-", "").upper()
        hostname = "0.0.0.0"
        input_mock.side_effect = ["yes", "no"]

        ssh_connection = SSHConnection(
            hostname=hostname,
            known_hosts_file=self.known_hosts_file,
            input=input_mock,
        )
        keys = self.known_hosts_file.read_text(encoding="utf-8")
        self.assertEqual(
            keys,
            "127.0.0.1 ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBOZWi"
            "fs+DoMqIa5Nr0wiVrzQNpMbUwaLzuSTN6rNrYA\n",
        )

        with self.assertLogs("gvm.connections", level="INFO") as cm:
            hostkeys = paramiko.HostKeys(filename=str(self.known_hosts_file))
            ssh_connection._ssh_authentication_input_loop(
                hostkeys=hostkeys, key=key
            )
            keys = self.known_hosts_file.read_text(encoding="utf-8")

            self.assertEqual(
                cm.output,
                [
                    "INFO:gvm.connections.ssh:Warning: "
                    f"Host '{hostname}' ({key_type}) not added to "
                    "the list of known hosts."
                ],
            )

            self.assertEqual(
                keys,
                "127.0.0.1 ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBOZWi"
                "fs+DoMqIa5Nr0wiVrzQNpMbUwaLzuSTN6rNrYA\n",
            )

    def test_connect_wrong_input(self):
        input_mock = MagicMock(spec=input)
        stdout_mock = StringIO()
        key_io = StringIO(
            """-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACB69SvZKJh/9VgSL0G27b5xVYa8nethH3IERbi0YqJDXwAAAKhjwAdrY8AH
awAAAAtzc2gtZWQyNTUxOQAAACB69SvZKJh/9VgSL0G27b5xVYa8nethH3IERbi0YqJDXw
AAAEA9tGQi2IrprbOSbDCF+RmAHd6meNSXBUQ2ekKXm4/8xnr1K9komH/1WBIvQbbtvnFV
hryd62EfcgRFuLRiokNfAAAAI2FsZXhfZ2F5bm9yQEFsZXhzLU1hY0Jvb2stQWlyLmxvY2
FsAQI=
            -----END OPENSSH PRIVATE KEY-----"""
        )
        key = paramiko.Ed25519Key.from_private_key(key_io)
        hostname = "0.0.0.0"
        key_type = key.get_name().replace("ssh-", "").upper()
        inputs = ["asd", "yes", "yoo", "no"]
        input_mock.side_effect = inputs
        ssh_connection = SSHConnection(
            hostname=hostname,
            known_hosts_file=self.known_hosts_file,
            input=input_mock,
            file=stdout_mock,
        )
        with self.assertLogs("gvm.connections", level="INFO") as cm:
            hostkeys = paramiko.HostKeys(filename=str(self.known_hosts_file))
            ssh_connection._ssh_authentication_input_loop(
                hostkeys=hostkeys, key=key
            )
            ret = stdout_mock.getvalue()

            self.assertEqual(
                cm.output,
                [
                    "INFO:gvm.connections.ssh:Warning: "
                    f"Host '{hostname}' ({key_type}) not added to "
                    "the list of known hosts."
                ],
            )

            self.assertEqual(
                ret,
                f"The authenticity of host '{hostname}' can't be established.\n"
                f"{key_type} key fingerprint is "
                "J6VESFdD3xSChn8y9PzWzeF+1tl892mOy2TqkMLO4ow.\n"
                "Are you sure you want to continue connecting (yes/no)? "
                "Please type 'yes' or 'no': "
                "Do you want to add 0.0.0.0 to known_hosts (yes/no)? "
                "Please type 'yes' or 'no': ",
            )

    def test_user_denies_auth(self):
        input_mock = MagicMock(spec=input)
        stdout_mock = StringIO()
        exit_mock = MagicMock(side_effect=AbortException("Exit called"))
        key_io = StringIO(
            """-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACB69SvZKJh/9VgSL0G27b5xVYa8nethH3IERbi0YqJDXwAAAKhjwAdrY8AH
awAAAAtzc2gtZWQyNTUxOQAAACB69SvZKJh/9VgSL0G27b5xVYa8nethH3IERbi0YqJDXw
AAAEA9tGQi2IrprbOSbDCF+RmAHd6meNSXBUQ2ekKXm4/8xnr1K9komH/1WBIvQbbtvnFV
hryd62EfcgRFuLRiokNfAAAAI2FsZXhfZ2F5bm9yQEFsZXhzLU1hY0Jvb2stQWlyLmxvY2
FsAQI=
            -----END OPENSSH PRIVATE KEY-----"""
        )
        key = paramiko.Ed25519Key.from_private_key(key_io)
        hostname = "0.0.0.0"
        input_mock.return_value = "no"
        ssh_connection = SSHConnection(
            hostname=hostname,
            known_hosts_file=self.known_hosts_file,
            input=input_mock,
            exit=exit_mock,
            file=stdout_mock,
        )
        hostkeys = paramiko.HostKeys(filename=str(self.known_hosts_file))
        with self.assertRaisesRegex(AbortException, "^Exit called"):
            ssh_connection._ssh_authentication_input_loop(
                hostkeys=hostkeys,
                key=key,
            )

        exit_mock.assert_called_once_with(
            "User denied key. Host key verification failed."
        )

    def test_disconnect(self):
        with patch("paramiko.SSHClient") as SSHClientMock:
            client_mock = SSHClientMock.return_value
            client_mock.exec_command.return_value = ["a", "b", "c"]
            ssh_connection = SSHConnection(
                known_hosts_file=self.known_hosts_file
            )

            ssh_connection.connect()
            self.assertEqual(ssh_connection._stdin, "a")
            self.assertEqual(ssh_connection._stdout, "b")
            self.assertEqual(ssh_connection._stderr, "c")

            ssh_connection.disconnect()
            # make sure the attributes have been deleted
            with self.assertRaises(AttributeError):
                type(ssh_connection._stdin)
            with self.assertRaises(AttributeError):
                type(ssh_connection._stdout)
            with self.assertRaises(AttributeError):
                type(ssh_connection._stderr)

    def test_disconnect_os_error(self):
        with patch("paramiko.SSHClient") as SSHClientMock:
            client_mock = SSHClientMock.return_value
            client_mock.exec_command.return_value = ["a", "b", "c"]
            client_mock.close.side_effect = OSError

            ssh_connection = SSHConnection(
                known_hosts_file=self.known_hosts_file
            )
            ssh_connection.connect()

            with self.assertRaises(OSError):
                with self.assertLogs("gvm.connections", level="INFO") as cm:
                    ssh_connection.disconnect()
                    self.assertEqual(cm.output, ["Connection closing error: "])

    def test_trigger_paramiko_ssh_except_in_get_remote_key(self):
        with patch("paramiko.transport.Transport") as TransportMock:
            client_mock = TransportMock.return_value
            client_mock.start_client.side_effect = paramiko.SSHException("foo")

            ssh_connection = SSHConnection(
                hostname="0.0.0.0",
            )

            with self.assertRaises(
                GvmError,
                msg="Couldn't fetch the remote server key: foo",
            ):
                ssh_connection._get_remote_host_key()

    def test_trigger_oserror_in_get_remote_key_connect(self):
        with patch("socket.socket") as SocketMock:
            client_mock = SocketMock.return_value
            client_mock.connect.side_effect = OSError("foo")

            ssh_connection = SSHConnection(
                hostname="0.0.0.0",
            )

            with self.assertRaises(
                GvmError,
                msg="Couldn't establish a connection to fetch the"
                "remote server key: foo",
            ):
                ssh_connection._get_remote_host_key()

    def test_trigger_oserror_in_get_remote_key_disconnect(self):
        with patch("paramiko.transport.Transport") as TransportMock:
            client_mock = TransportMock.return_value
            client_mock.close.side_effect = paramiko.SSHException("foo")

            ssh_connection = SSHConnection(
                hostname="0.0.0.0",
            )

            with self.assertRaises(
                GvmError,
                msg="Couldn't close the connection to the"
                "remote server key: foo",
            ):
                ssh_connection._get_remote_host_key()

    def test_send(self):
        with patch("paramiko.SSHClient") as SSHClientMock:
            client_mock = SSHClientMock.return_value
            stdin = Mock()
            stdin.channel.send.return_value = 4
            client_mock.exec_command.return_value = [stdin, None, None]
            ssh_connection = SSHConnection(
                known_hosts_file=self.known_hosts_file
            )

            ssh_connection.connect()
            ssh_connection.send("blah")
            ssh_connection.disconnect()

    def test_send_error(self):
        with patch("paramiko.SSHClient") as SSHClientMock:
            client_mock = SSHClientMock.return_value
            stdin = Mock()
            stdin.channel.send.return_value = None
            client_mock.exec_command.return_value = [stdin, None, None]
            ssh_connection = SSHConnection(
                known_hosts_file=self.known_hosts_file
            )

            ssh_connection.connect()
            with self.assertRaises(
                GvmError, msg="Remote closed the connection"
            ):
                ssh_connection.send("blah")
            ssh_connection.disconnect()

    def test_send_and_slice(self):
        with patch("paramiko.SSHClient") as SSHClientMock:
            client_mock = SSHClientMock.return_value
            stdin = Mock()
            stdin.channel.send.side_effect = [2, 2]
            client_mock.exec_command.return_value = [stdin, None, None]
            ssh_connection = SSHConnection(
                known_hosts_file=self.known_hosts_file
            )

            ssh_connection.connect()
            ssh_connection.send("blah")

            stdin.channel.send.assert_called()
            with self.assertRaises(AssertionError):
                stdin.channel.send.assert_called_once()
            ssh_connection.disconnect()

    def test_read(self):
        with patch("paramiko.SSHClient") as SSHClientMock:
            client_mock = SSHClientMock.return_value
            stdout = Mock()
            stdout.channel.recv.return_value = b"foo bar baz"
            client_mock.exec_command.return_value = [None, stdout, None]
            ssh_connection = SSHConnection(
                known_hosts_file=self.known_hosts_file
            )

            ssh_connection.connect()
            recved = ssh_connection._read()
            self.assertEqual(recved, b"foo bar baz")
            ssh_connection.disconnect()

    def test_is_gvm_connection(self):
        ssh_connection = SSHConnection(known_hosts_file=self.known_hosts_file)
        self.assertTrue(isinstance(ssh_connection, GvmConnection))
