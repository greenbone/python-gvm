# -*- coding: utf-8 -*-
# Copyright (C) 2021-2022 Greenbone AG
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
