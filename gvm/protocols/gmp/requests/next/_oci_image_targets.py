#  SPDX-FileCopyrightText: 2025 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

from typing import Optional

from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.protocols.gmp.requests._entity_id import EntityID
from gvm.utils import to_bool, to_comma_list
from gvm.xml import XmlCommand


class OCIImageTargets:
    @classmethod
    def create_oci_image_target(
        cls,
        name: str,
        image_references: list[str],
        *,
        comment: Optional[str] = None,
        credential_id: Optional[EntityID] = None,
    ) -> Request:
        """Create a new OCI image target

        Args:
            name: Name of the target
            image_references: List of OCI image URLs to scan
            comment: Comment for the target
            credential_id: UUID of a credential to use on target
        """
        if not name:
            raise RequiredArgument(
                function=cls.create_oci_image_target.__name__, argument="name"
            )

        if not image_references:
            raise RequiredArgument(
                function=cls.create_oci_image_target.__name__,
                argument="image_references",
            )

        cmd = XmlCommand("create_oci_image_target")
        cmd.add_element("name", name)
        cmd.add_element("image_references", to_comma_list(image_references))

        if comment:
            cmd.add_element("comment", comment)

        if credential_id:
            cmd.add_element("credential", attrs={"id": str(credential_id)})

        return cmd

    @classmethod
    def modify_oci_image_target(
        cls,
        oci_image_target_id: EntityID,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        image_references: Optional[list[str]] = None,
        credential_id: Optional[EntityID] = None,
    ) -> Request:
        """Modify an existing target.

        Args:
            oci_image_target_id: UUID of target to modify.
            comment: Comment on target.
            name: Name of target.
            image_references: List of OCI image URLs.
            credential_id: UUID of credential to use on target.
        """
        if not oci_image_target_id:
            raise RequiredArgument(
                function=cls.modify_oci_image_target.__name__,
                argument="oci_image_target_id",
            )

        cmd = XmlCommand("modify_oci_image_target")
        cmd.set_attribute("oci_image_target_id", str(oci_image_target_id))

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if image_references:
            cmd.add_element("image_references", to_comma_list(image_references))

        if credential_id:
            cmd.add_element("credential", attrs={"id": str(credential_id)})

        return cmd

    @classmethod
    def clone_oci_image_target(cls, oci_image_target_id: EntityID) -> Request:
        """Clone an existing OCI image target.

        Args:
            oci_image_target_id: UUID of an existing target to clone.
        """
        if not oci_image_target_id:
            raise RequiredArgument(
                function=cls.clone_oci_image_target.__name__,
                argument="oci_image_target_id",
            )

        cmd = XmlCommand("create_oci_image_target")
        cmd.add_element("copy", str(oci_image_target_id))
        return cmd

    @classmethod
    def delete_oci_image_target(
        cls, oci_image_target_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> Request:
        """Delete an existing OCI image target.

        Args:
            oci_image_target_id: UUID of an existing target to delete.
            ultimate: Whether to remove entirely or to the trashcan.
        """
        if not oci_image_target_id:
            raise RequiredArgument(
                function=cls.delete_oci_image_target.__name__,
                argument="oci_image_target_id",
            )

        cmd = XmlCommand("delete_oci_image_target")
        cmd.set_attribute("oci_image_target_id", str(oci_image_target_id))
        cmd.set_attribute("ultimate", to_bool(ultimate))
        return cmd

    @classmethod
    def get_oci_image_target(
        cls, oci_image_target_id: EntityID, *, tasks: Optional[bool] = None
    ) -> Request:
        """Request a single OCI Image target.

        Args:
            oci_image_target_id: UUID of the target to request.
            tasks: Whether to include list of tasks that use the target
        """
        if not oci_image_target_id:
            raise RequiredArgument(
                function=cls.get_oci_image_target.__name__,
                argument="oci_image_target_id",
            )

        cmd = XmlCommand("get_oci_image_targets")
        cmd.set_attribute("oci_image_target_id", str(oci_image_target_id))

        if tasks is not None:
            cmd.set_attribute("tasks", to_bool(tasks))

        return cmd

    @classmethod
    def get_oci_image_targets(
        cls,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
        tasks: Optional[bool] = None,
    ) -> Request:
        """Request a list of OCI image targets.

        Args:
            filter_string: Filter term to use for the query.
            filter_id: UUID of an existing filter to use for the query.
            trash: Whether to include targets in the trashcan.
            tasks: Whether to include list of tasks that use the target.
        """
        cmd = XmlCommand("get_oci_image_targets")
        cmd.add_filter(filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if tasks is not None:
            cmd.set_attribute("tasks", to_bool(tasks))

        return cmd
