#  SPDX-FileCopyrightText: 2026 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.protocols.gmp.requests._entity_id import EntityID
from gvm.utils import to_bool, to_comma_list
from gvm.xml import XmlCommand


class WebApplicationTargets:
    @classmethod
    def create_web_application_target(
        cls,
        name: str,
        urls: list[str],
        *,
        comment: str | None = None,
        exclude_urls: list[str] | None = None,
        credential_id: EntityID | None = None,
    ) -> Request:
        """Create a new web application target.

        Args:
            name: Name of the target.
            urls: List of URLs to scan.
            comment: Comment for the target.
            exclude_urls: List of URLs to exclude from the scan.
            credential_id: UUID of a credential to use on target.
        """
        if not name:
            raise RequiredArgument(
                function=cls.create_web_application_target.__name__,
                argument="name",
            )

        if not urls:
            raise RequiredArgument(
                function=cls.create_web_application_target.__name__,
                argument="urls",
            )

        cmd = XmlCommand("create_web_application_target")
        cmd.add_element("name", name)
        cmd.add_element("urls", to_comma_list(urls))

        if comment:
            cmd.add_element("comment", comment)

        if exclude_urls:
            cmd.add_element("exclude_urls", to_comma_list(exclude_urls))

        if credential_id:
            cmd.add_element("credential", attrs={"id": str(credential_id)})

        return cmd

    @classmethod
    def modify_web_application_target(
        cls,
        web_application_target_id: EntityID,
        *,
        name: str | None = None,
        comment: str | None = None,
        urls: list[str] | None = None,
        exclude_urls: list[str] | None = None,
        credential_id: EntityID | None = None,
    ) -> Request:
        """Modify an existing web application target.

        Args:
            web_application_target_id: UUID of target to modify.
            name: Name of target.
            comment: Comment on target.
            urls: List of URLs to scan.
            exclude_urls: List of URLs to exclude from the scan.
            credential_id: UUID of credential to use on target.
        """
        if not web_application_target_id:
            raise RequiredArgument(
                function=cls.modify_web_application_target.__name__,
                argument="web_application_target_id",
            )

        cmd = XmlCommand("modify_web_application_target")
        cmd.set_attribute(
            "web_application_target_id", str(web_application_target_id)
        )

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if urls:
            cmd.add_element("urls", to_comma_list(urls))

        if exclude_urls:
            cmd.add_element("exclude_urls", to_comma_list(exclude_urls))

        if credential_id:
            cmd.add_element("credential", attrs={"id": str(credential_id)})

        return cmd

    @classmethod
    def clone_web_application_target(
        cls, web_application_target_id: EntityID
    ) -> Request:
        """Clone an existing web application target.

        Args:
            web_application_target_id: UUID of an existing target to clone.
        """
        if not web_application_target_id:
            raise RequiredArgument(
                function=cls.clone_web_application_target.__name__,
                argument="web_application_target_id",
            )

        cmd = XmlCommand("create_web_application_target")
        cmd.add_element("copy", str(web_application_target_id))
        return cmd

    @classmethod
    def delete_web_application_target(
        cls,
        web_application_target_id: EntityID,
        *,
        ultimate: bool | None = False,
    ) -> Request:
        """Delete an existing web application target.

        Args:
            web_application_target_id: UUID of an existing target to delete.
            ultimate: Whether to remove entirely or move to the trashcan.
        """
        if not web_application_target_id:
            raise RequiredArgument(
                function=cls.delete_web_application_target.__name__,
                argument="web_application_target_id",
            )

        cmd = XmlCommand("delete_web_application_target")
        cmd.set_attribute(
            "web_application_target_id", str(web_application_target_id)
        )
        cmd.set_attribute("ultimate", to_bool(ultimate))
        return cmd

    @classmethod
    def get_web_application_target(
        cls,
        web_application_target_id: EntityID,
        *,
        tasks: bool | None = None,
    ) -> Request:
        """Request a single web application target.

        Args:
            web_application_target_id: UUID of the target to request.
            tasks: Whether to include list of tasks that use the target.
        """
        if not web_application_target_id:
            raise RequiredArgument(
                function=cls.get_web_application_target.__name__,
                argument="web_application_target_id",
            )

        cmd = XmlCommand("get_web_application_targets")
        cmd.set_attribute(
            "web_application_target_id", str(web_application_target_id)
        )

        if tasks is not None:
            cmd.set_attribute("tasks", to_bool(tasks))

        return cmd

    @classmethod
    def get_web_application_targets(
        cls,
        *,
        filter_string: str | None = None,
        filter_id: EntityID | None = None,
        trash: bool | None = None,
        tasks: bool | None = None,
    ) -> Request:
        """Request a list of web application targets.

        Args:
            filter_string: Filter term to use for the query.
            filter_id: UUID of an existing filter to use for the query.
            trash: Whether to include targets in the trashcan.
            tasks: Whether to include list of tasks that use the target.
        """
        cmd = XmlCommand("get_web_application_targets")
        cmd.add_filter(filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if tasks is not None:
            cmd.set_attribute("tasks", to_bool(tasks))

        return cmd
