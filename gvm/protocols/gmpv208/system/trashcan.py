# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from typing import Any

from gvm.errors import RequiredArgument
from gvm.xml import XmlCommand


class TrashcanMixin:
    def empty_trashcan(self) -> Any:
        """Empty the trashcan

        Remove all entities from the trashcan. **Attention:** this command can
        not be reverted

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("empty_trashcan"))

    def restore_from_trashcan(self, entity_id: str) -> Any:
        """Restore an entity from the trashcan

        Arguments:
            entity_id: ID of the entity to be restored from the trashcan

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not entity_id:
            raise RequiredArgument(
                function=self.restore_from_trashcan.__name__,
                argument="entity_id",
            )

        cmd = XmlCommand("restore")
        cmd.set_attribute("id", entity_id)

        return self._send_xml_command(cmd)
