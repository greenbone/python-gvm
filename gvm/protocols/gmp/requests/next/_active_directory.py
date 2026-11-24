# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Sequence

from gvm._enum import Enum
from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool
from gvm.xml import XmlCommand

from .._entity_id import EntityID


class ActiveDirectorySearchScope(Enum):
    """Enum for Active Directory search scopes"""

    BASE = "base"
    ONELEVEL = "onelevel"
    SUBTREE = "subtree"


class ActiveDirectoryObjectType(Enum):
    """Enum for Active Directory object types"""

    OU = "ou"
    CONTAINER = "container"
    COMPUTER = "computer"
    GROUP = "group"


class ActiveDirectory:
    @classmethod
    def get_active_directory_objects(
        cls,
        credential_id: EntityID,
        *,
        base_dn: str | None = None,
        group_dn: str | None = None,
        scope: ActiveDirectorySearchScope | str | None = None,
        object_types: Sequence[ActiveDirectoryObjectType | str] | None = None,
        max_results: int | None = None,
        include_disabled_computers: bool | None = None,
        targets: bool | None = None,
        tasks: bool | None = None,
        details: bool | None = None,
    ) -> Request:
        """Search Active Directory using a saved AD credential.

        Requires AD integration to be enabled in gvmd and a saved AD
        credential. Options set to None are omitted from the request so that
        gvmd applies its defaults.

        Args:
            credential_id: UUID of a saved AD credential.
            base_dn: Nonempty search base within the credential's base DN.
                Defaults to the credential's base DN.
            group_dn: Nonempty DN selecting explicit direct group members
                within the search base and scope. Must be within the
                credential's base DN.
            scope: Search scope, either "base", "onelevel", or "subtree".
                Defaults to "onelevel", searching immediately below base_dn. Use
                "subtree" to search at all directory depths.
            object_types: Nonempty selection of "ou", "container", "computer",
                or "group". Defaults to "ou", "computer", and "group".
                Duplicates are ignored, preserving first-occurrence order.
            max_results: Maximum number of objects to fetch after LDAP
                filtering. Must be a positive integer within the server's
                configured limit. Omit to use that limit.
            include_disabled_computers: Include disabled computers. Defaults
                to True.
            targets: Include matching targets for computers. Defaults to False.
            tasks: Include tasks and readable configurations for matching
                targets. Requires targets=True. Defaults to False.
            details: Include computer OS version and service principal names.
                Defaults to False.
        """
        if not credential_id:
            raise RequiredArgument(
                function=cls.get_active_directory_objects.__name__,
                argument="credential_id",
            )
        if base_dn is not None and not base_dn:
            raise RequiredArgument(
                function=cls.get_active_directory_objects.__name__,
                argument="base_dn",
            )
        if group_dn is not None and not group_dn:
            raise RequiredArgument(
                function=cls.get_active_directory_objects.__name__,
                argument="group_dn",
            )
        if scope is not None and not scope:
            raise RequiredArgument(
                function=cls.get_active_directory_objects.__name__,
                argument="scope",
            )
        if scope is not None and not isinstance(
            scope, ActiveDirectorySearchScope
        ):
            try:
                scope = ActiveDirectorySearchScope(scope)
            except InvalidArgument as error:
                raise InvalidArgument(
                    str(error),
                    function=cls.get_active_directory_objects.__name__,
                    argument="scope",
                ) from None
        if object_types is not None and (
            isinstance(object_types, str)
            or not object_types
            or any(not object_type for object_type in object_types)
        ):
            raise InvalidArgument(
                function=cls.get_active_directory_objects.__name__,
                argument="object_types",
            )
        try:
            normalized_object_types = (
                list(
                    dict.fromkeys(
                        ActiveDirectoryObjectType(t) for t in object_types
                    )
                )
                if object_types is not None
                else None
            )
        except InvalidArgument as error:
            raise InvalidArgument(
                str(error),
                function=cls.get_active_directory_objects.__name__,
                argument="object_types",
            ) from None
        if max_results is not None and (
            isinstance(max_results, bool)
            or not isinstance(max_results, int)
            or max_results < 1
        ):
            raise InvalidArgument(
                function=cls.get_active_directory_objects.__name__,
                argument="max_results",
            )
        if tasks and not targets:
            raise InvalidArgument(
                function=cls.get_active_directory_objects.__name__,
                argument="tasks",
            )

        cmd = XmlCommand("get_active_directory_objects")
        cmd.set_attribute("credential_id", str(credential_id))
        if scope is not None:
            cmd.set_attribute("scope", scope.value)
        if max_results is not None:
            cmd.set_attribute("max_results", str(max_results))
        if include_disabled_computers is not None:
            cmd.set_attribute(
                "include_disabled_computers",
                to_bool(include_disabled_computers),
            )
        if targets is not None:
            cmd.set_attribute("targets", to_bool(targets))
        if tasks is not None:
            cmd.set_attribute("tasks", to_bool(tasks))
        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        if base_dn is not None:
            cmd.add_element("base_dn", base_dn)
        if group_dn is not None:
            cmd.add_element("group_dn", group_dn)
        if normalized_object_types is not None:
            types_element = cmd.add_element("object_types")
            for object_type in normalized_object_types:
                types_element.add_element("object_type", object_type.value)

        return cmd
