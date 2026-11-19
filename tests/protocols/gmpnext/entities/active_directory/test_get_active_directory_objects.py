# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from uuid import UUID

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.next import (
    ActiveDirectoryObjectType,
    ActiveDirectorySearchScope,
)


class GmpGetActiveDirectoryObjectsTestMixin:
    def test_get_active_directory_objects_with_duplicate_object_types(self):
        self.gmp.get_active_directory_objects(
            "credential-id", object_types=["computer", "computer"]
        )

        self.connection.send.has_been_called_with(
            b'<get_active_directory_objects credential_id="credential-id">'
            b"<object_types>"
            b"<object_type>computer</object_type>"
            b"</object_types>"
            b"</get_active_directory_objects>"
        )

        self.gmp.get_active_directory_objects(
            "credential-id",
            object_types=[
                "computer",
                "group",
                ActiveDirectoryObjectType.COMPUTER,
                "COMPUTER",
                ActiveDirectoryObjectType.GROUP,
            ],
        )

        self.connection.send.has_been_called_with(
            b'<get_active_directory_objects credential_id="credential-id">'
            b"<object_types>"
            b"<object_type>computer</object_type>"
            b"<object_type>group</object_type>"
            b"</object_types>"
            b"</get_active_directory_objects>"
        )

    def test_get_active_directory_objects_with_mixed_object_types(self):
        self.gmp.get_active_directory_objects(
            "credential-id",
            scope=ActiveDirectorySearchScope.SUBTREE,
            object_types=[ActiveDirectoryObjectType.COMPUTER, "group"],
        )

        self.connection.send.has_been_called_with(
            b'<get_active_directory_objects credential_id="credential-id" '
            b'scope="subtree"><object_types>'
            b"<object_type>computer</object_type>"
            b"<object_type>group</object_type>"
            b"</object_types></get_active_directory_objects>"
        )

    def test_get_active_directory_objects_with_enums(self):
        self.gmp.get_active_directory_objects(
            "credential-id",
            scope=ActiveDirectorySearchScope.ONELEVEL,
            object_types=[
                ActiveDirectoryObjectType.OU,
                ActiveDirectoryObjectType.CONTAINER,
                ActiveDirectoryObjectType.COMPUTER,
                ActiveDirectoryObjectType.GROUP,
            ],
        )

        self.connection.send.has_been_called_with(
            b'<get_active_directory_objects credential_id="credential-id" '
            b'scope="onelevel"><object_types>'
            b"<object_type>ou</object_type>"
            b"<object_type>container</object_type>"
            b"<object_type>computer</object_type>"
            b"<object_type>group</object_type>"
            b"</object_types></get_active_directory_objects>"
        )

    def test_get_active_directory_objects_with_positional_credential_id(self):
        self.gmp.get_active_directory_objects("credential-id")

        self.connection.send.has_been_called_with(
            b'<get_active_directory_objects credential_id="credential-id"/>'
        )

    def test_get_active_directory_objects(self):
        self.gmp.get_active_directory_objects(credential_id="credential-id")

        self.connection.send.has_been_called_with(
            b'<get_active_directory_objects credential_id="credential-id"/>'
        )

    def test_get_active_directory_objects_with_uuid(self):
        self.gmp.get_active_directory_objects(
            credential_id=UUID("12345678-1234-1234-1234-123456789abc")
        )

        self.connection.send.has_been_called_with(
            b"<get_active_directory_objects "
            b'credential_id="12345678-1234-1234-1234-123456789abc"/>'
        )

    def test_get_active_directory_objects_with_all_options(self):
        self.gmp.get_active_directory_objects(
            credential_id="credential-id",
            base_dn="OU=Machines,DC=example,DC=org",
            group_dn="CN=Scan,DC=example,DC=org",
            scope="subtree",
            object_types=["ou", "container", "computer", "group"],
            max_results=1000,
            include_disabled_computers=True,
            targets=True,
            tasks=True,
            details=True,
        )

        self.connection.send.has_been_called_with(
            b'<get_active_directory_objects credential_id="credential-id" '
            b'scope="subtree" max_results="1000" '
            b'include_disabled_computers="1" targets="1" tasks="1" details="1">'
            b"<base_dn>OU=Machines,DC=example,DC=org</base_dn>"
            b"<group_dn>CN=Scan,DC=example,DC=org</group_dn>"
            b"<object_types><object_type>ou</object_type>"
            b"<object_type>container</object_type>"
            b"<object_type>computer</object_type>"
            b"<object_type>group</object_type></object_types>"
            b"</get_active_directory_objects>"
        )

    def test_get_active_directory_objects_with_false_flags(self):
        self.gmp.get_active_directory_objects(
            credential_id="credential-id",
            include_disabled_computers=False,
            targets=False,
            tasks=False,
            details=False,
        )

        self.connection.send.has_been_called_with(
            b'<get_active_directory_objects credential_id="credential-id" '
            b'include_disabled_computers="0" targets="0" tasks="0" details="0"/>'
        )

    def test_get_active_directory_objects_with_special_characters(self):
        self.gmp.get_active_directory_objects(
            credential_id="credential<&",
            base_dn="OU=Machines<&,DC=example,DC=org",
            group_dn="CN=Scan<&,DC=example,DC=org",
        )

        self.connection.send.has_been_called_with(
            b'<get_active_directory_objects credential_id="credential&lt;&amp;">'
            b"<base_dn>OU=Machines&lt;&amp;,DC=example,DC=org</base_dn>"
            b"<group_dn>CN=Scan&lt;&amp;,DC=example,DC=org</group_dn>"
            b"</get_active_directory_objects>"
        )

    def test_get_active_directory_objects_with_scope(self):
        self.gmp.get_active_directory_objects(
            credential_id="credential-id", scope="base"
        )

        self.connection.send.has_been_called_with(
            b'<get_active_directory_objects credential_id="credential-id" '
            b'scope="base"/>'
        )

        self.gmp.get_active_directory_objects(
            credential_id="credential-id", scope="onelevel"
        )

        self.connection.send.has_been_called_with(
            b'<get_active_directory_objects credential_id="credential-id" '
            b'scope="onelevel"/>'
        )

        self.gmp.get_active_directory_objects(
            credential_id="credential-id", scope="subtree"
        )

        self.connection.send.has_been_called_with(
            b'<get_active_directory_objects credential_id="credential-id" '
            b'scope="subtree"/>'
        )

    def test_get_active_directory_objects_with_max_results(self):
        self.gmp.get_active_directory_objects(
            credential_id="credential-id", max_results=1
        )

        self.connection.send.has_been_called_with(
            b'<get_active_directory_objects credential_id="credential-id" '
            b'max_results="1"/>'
        )

        self.gmp.get_active_directory_objects(
            credential_id="credential-id", max_results=1000
        )

        self.connection.send.has_been_called_with(
            b'<get_active_directory_objects credential_id="credential-id" '
            b'max_results="1000"/>'
        )

    def test_get_active_directory_objects_without_credential_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_active_directory_objects(credential_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_active_directory_objects(credential_id="")

        self.connection.send.has_not_been_called()

    def test_get_active_directory_objects_with_empty_dn(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_active_directory_objects(
                credential_id="credential-id", base_dn=""
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.get_active_directory_objects(
                credential_id="credential-id", group_dn=""
            )

        self.connection.send.has_not_been_called()

    def test_get_active_directory_objects_with_empty_scope(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_active_directory_objects(
                credential_id="credential-id", scope=""
            )

        self.connection.send.has_not_been_called()

    def test_get_active_directory_objects_with_invalid_scope(self):
        with self.assertRaises(InvalidArgument) as context:
            self.gmp.get_active_directory_objects(
                credential_id="credential-id", scope="invalid"
            )

        self.assertEqual(context.exception.argument, "scope")
        self.assertEqual(
            context.exception.function, "get_active_directory_objects"
        )
        self.connection.send.has_not_been_called()

    def test_get_active_directory_objects_with_invalid_object_types(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.get_active_directory_objects(
                credential_id="credential-id", object_types=[]
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.get_active_directory_objects(
                credential_id="credential-id", object_types="computer"
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.get_active_directory_objects(
                credential_id="credential-id", object_types=[""]
            )

        with self.assertRaises(InvalidArgument) as context:
            self.gmp.get_active_directory_objects(
                credential_id="credential-id",
                object_types=["computer", "invalid"],
            )

        self.assertEqual(context.exception.argument, "object_types")
        self.assertEqual(
            context.exception.function, "get_active_directory_objects"
        )
        self.connection.send.has_not_been_called()

    def test_get_active_directory_objects_with_invalid_max_results(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.get_active_directory_objects(
                credential_id="credential-id", max_results=-1
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.get_active_directory_objects(
                credential_id="credential-id", max_results=0
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.get_active_directory_objects(
                credential_id="credential-id", max_results=1001
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.get_active_directory_objects(
                credential_id="credential-id", max_results="10"
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.get_active_directory_objects(
                credential_id="credential-id", max_results=1.5
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.get_active_directory_objects(
                credential_id="credential-id", max_results=True
            )

        self.connection.send.has_not_been_called()

    def test_get_active_directory_objects_with_tasks_without_targets(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.get_active_directory_objects(
                credential_id="credential-id",
                tasks=True,
                targets=None,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.get_active_directory_objects(
                credential_id="credential-id",
                tasks=True,
                targets=False,
            )

        self.connection.send.has_not_been_called()
