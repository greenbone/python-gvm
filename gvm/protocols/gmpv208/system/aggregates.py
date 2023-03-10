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

from enum import Enum
from typing import Any, Optional

from gvm.errors import InvalidArgument, InvalidArgumentType, RequiredArgument

# if I use latest, I get circular import :/
from gvm.protocols.gmpv208.entities.entities import EntityType
from gvm.utils import add_filter
from gvm.xml import XmlCommand


class AggregateStatistic(Enum):
    """Enum for aggregate statistic types"""

    COUNT = "count"  # Number of items
    C_COUNT = "c_count"  # Cumulative number of items
    C_SUM = "c_sum"  # Cumulative sum of values
    MAX = "max"  # Maximum value
    MEAN = "mean"  # Arithmetic mean of values
    MIN = "min"  # Minimum value
    SUM = "sum"  # Sum of values
    TEXT = "text"  # Text column value
    VALUE = "value"  # Group or subgroup column value

    @classmethod
    def from_string(
        cls,
        aggregate_statistic: Optional[str],
    ) -> Optional["AggregateStatistic"]:
        """
        Convert a aggregate statistic string to an actual AggregateStatistic
        instance.

        Arguments:
            aggregate_statistic: Aggregate statistic string to convert to a
                AggregateStatistic
        """
        if not aggregate_statistic:
            return None

        try:
            return cls[aggregate_statistic.upper()]
        except KeyError:
            raise InvalidArgument(
                argument="aggregate_statistic",
                function=cls.from_string.__name__,
            ) from None


class SortOrder(Enum):
    """Enum for sort order"""

    ASCENDING = "ascending"
    DESCENDING = "descending"

    @classmethod
    def from_string(
        cls,
        sort_order: Optional[str],
    ) -> Optional["SortOrder"]:
        """
        Convert a sort order string to an actual SortOrder instance.

        Arguments:
            sort_order: Sort order string to convert to a SortOrder
        """
        if not sort_order:
            return None

        try:
            return cls[sort_order.upper()]
        except KeyError:
            raise InvalidArgument(
                argument="sort_order", function=cls.from_string.__name__
            ) from None


class AggregatesMixin:
    def get_aggregates(
        self,
        resource_type: EntityType,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        sort_criteria: Optional[list] = None,
        data_columns: Optional[list] = None,
        group_column: Optional[str] = None,
        subgroup_column: Optional[str] = None,
        text_columns: Optional[list] = None,
        first_group: Optional[int] = None,
        max_groups: Optional[int] = None,
        mode: Optional[int] = None,
        **kwargs,
    ) -> Any:
        """Request aggregated information on a resource / entity type

        Additional arguments can be set via the kwargs parameter for backward
        compatibility with older versions of python-gvm, but are not validated.

        Arguments:
            resource_type: The entity type to gather data from
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            sort_criteria: List of sort criteria (dicts that can contain
                a field, stat and order)
            data_columns: List of fields to aggregate data from
            group_column: The field to group the entities by
            subgroup_column: The field to further group the entities
                inside groups by
            text_columns: List of simple text columns which no statistics
                are calculated for
            first_group: The index of the first aggregate group to return
            max_groups: The maximum number of aggregate groups to return,
                -1 for all
            mode: Special mode for aggregation

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not resource_type:
            raise RequiredArgument(
                function=self.get_aggregates.__name__, argument="resource_type"
            )

        if not isinstance(resource_type, EntityType):
            raise InvalidArgumentType(
                function=self.get_aggregates.__name__,
                argument="resource_type",
                arg_type=EntityType.__name__,
            )

        cmd = XmlCommand("get_aggregates")

        _actual_resource_type = resource_type
        if resource_type.value == EntityType.AUDIT.value:
            _actual_resource_type = EntityType.TASK
            cmd.set_attribute("usage_type", "audit")
        elif resource_type.value == EntityType.POLICY.value:
            _actual_resource_type = EntityType.SCAN_CONFIG
            cmd.set_attribute("usage_type", "policy")
        elif resource_type.value == EntityType.SCAN_CONFIG.value:
            cmd.set_attribute("usage_type", "scan")
        elif resource_type.value == EntityType.TASK.value:
            cmd.set_attribute("usage_type", "scan")
        cmd.set_attribute("type", _actual_resource_type.value)

        add_filter(cmd, filter_string, filter_id)

        if first_group is not None:
            if not isinstance(first_group, int):
                raise InvalidArgumentType(
                    function=self.get_aggregates.__name__,
                    argument="first_group",
                    arg_type=int.__name__,
                )
            cmd.set_attribute("first_group", str(first_group))

        if max_groups is not None:
            if not isinstance(max_groups, int):
                raise InvalidArgumentType(
                    function=self.get_aggregates.__name__,
                    argument="max_groups",
                    arg_type=int.__name__,
                )
            cmd.set_attribute("max_groups", str(max_groups))

        if sort_criteria is not None:
            if not isinstance(sort_criteria, list):
                raise InvalidArgumentType(
                    function=self.get_aggregates.__name__,
                    argument="sort_criteria",
                    arg_type=list.__name__,
                )
            for sort in sort_criteria:
                if not isinstance(sort, dict):
                    raise InvalidArgumentType(
                        function=self.get_aggregates.__name__,
                        argument="sort_criteria",
                    )

                sort_elem = cmd.add_element("sort")
                if sort.get("field"):
                    sort_elem.set_attribute("field", sort.get("field"))

                if sort.get("stat"):
                    if isinstance(sort["stat"], AggregateStatistic):
                        sort_elem.set_attribute("stat", sort["stat"].value)
                    else:
                        stat = AggregateStatistic.from_string(sort["stat"])
                        sort_elem.set_attribute("stat", stat.value)

                if sort.get("order"):
                    if isinstance(sort["order"], SortOrder):
                        sort_elem.set_attribute("order", sort["order"].value)
                    else:
                        so = SortOrder.from_string(sort["order"])
                        sort_elem.set_attribute("order", so.value)

        if data_columns is not None:
            if not isinstance(data_columns, list):
                raise InvalidArgumentType(
                    function=self.get_aggregates.__name__,
                    argument="data_columns",
                    arg_type=list.__name__,
                )
            for column in data_columns:
                cmd.add_element("data_column", column)

        if group_column is not None:
            cmd.set_attribute("group_column", group_column)

        if subgroup_column is not None:
            if not group_column:
                raise RequiredArgument(
                    f"{self.get_aggregates.__name__} requires a group_column"
                    " argument if subgroup_column is given",
                    function=self.get_aggregates.__name__,
                    argument="subgroup_column",
                )
            cmd.set_attribute("subgroup_column", subgroup_column)

        if text_columns is not None:
            if not isinstance(text_columns, list):
                raise InvalidArgumentType(
                    function=self.get_aggregates.__name__,
                    argument="text_columns",
                    arg_type=list.__name__,
                )
            for column in text_columns:
                cmd.add_element("text_column", column)

        if mode is not None:
            cmd.set_attribute("mode", mode)

        # Add additional keyword args as attributes for backward compatibility.
        cmd.set_attributes(kwargs)

        return self._send_xml_command(cmd)
