# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Iterable, Optional, Union

from gvm._enum import Enum
from gvm.errors import InvalidArgumentType, RequiredArgument
from gvm.protocols.core import Request
from gvm.xml import XmlCommand

from .._entity_id import EntityID
from ._entity_type import EntityType


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


class SortOrder(Enum):
    """Enum for sort order"""

    ASCENDING = "ascending"
    DESCENDING = "descending"


class Aggregates:
    @classmethod
    def get_aggregates(
        cls,
        resource_type: Union[EntityType, str],
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        sort_criteria: Optional[
            Iterable[dict[str, Union[str, SortOrder, AggregateStatistic]]]
        ] = None,
        data_columns: Optional[Union[Iterable[str], str]] = None,
        group_column: Optional[str] = None,
        subgroup_column: Optional[str] = None,
        text_columns: Optional[Union[Iterable[str], str]] = None,
        first_group: Optional[int] = None,
        max_groups: Optional[int] = None,
        mode: Optional[int] = None,
        **kwargs,
    ) -> Request:
        """Request aggregated information on a resource / entity type

        Additional arguments can be set via the kwargs parameter for backward
        compatibility with older versions of python-gvm, but are not validated.

        Args:
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
        """
        if not resource_type:
            raise RequiredArgument(
                function=cls.get_aggregates.__name__, argument="resource_type"
            )

        if not isinstance(resource_type, EntityType):
            resource_type = EntityType(resource_type)

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

        cmd.add_filter(filter_string, filter_id)

        if first_group is not None:
            try:
                cmd.set_attribute("first_group", str(int(first_group)))
            except ValueError:
                raise InvalidArgumentType(
                    argument="first_group",
                    function=cls.get_aggregates.__name__,
                ) from None

        if max_groups is not None:
            try:
                cmd.set_attribute("max_groups", str(int(max_groups)))
            except ValueError:
                raise InvalidArgumentType(
                    argument="first_group",
                    function=cls.get_aggregates.__name__,
                )

        if sort_criteria is not None:
            if not isinstance(sort_criteria, Iterable) or isinstance(
                sort_criteria, str
            ):
                raise InvalidArgumentType(
                    argument="sort_criteria",
                    function=cls.get_aggregates.__name__,
                    arg_type=getattr(Iterable, "__name__", "Iterable"),
                )
            for sort in sort_criteria:
                if not isinstance(sort, dict):
                    raise InvalidArgumentType(
                        argument="sort_criteria",
                        function=cls.get_aggregates.__name__,
                    )

                sort_elem = cmd.add_element("sort")
                if sort.get("field"):
                    sort_elem.set_attribute("field", sort.get("field"))  # type: ignore

                if sort.get("stat"):
                    if isinstance(sort["stat"], AggregateStatistic):
                        sort_elem.set_attribute("stat", sort["stat"].value)
                    else:
                        stat = AggregateStatistic(sort["stat"])
                        sort_elem.set_attribute("stat", stat.value)

                if sort.get("order"):
                    if isinstance(sort["order"], SortOrder):
                        sort_elem.set_attribute("order", sort["order"].value)
                    else:
                        so = SortOrder(sort["order"])
                        sort_elem.set_attribute("order", so.value)

        if data_columns is not None:
            if isinstance(data_columns, str):
                data_columns = [data_columns]
            elif not isinstance(data_columns, Iterable):
                raise InvalidArgumentType(
                    function=cls.get_aggregates.__name__,
                    argument="data_columns",
                    arg_type=getattr(Iterable, "__name__", "Iterable"),
                )
            for column in data_columns:
                cmd.add_element("data_column", column)

        if group_column is not None:
            cmd.set_attribute("group_column", group_column)

        if subgroup_column is not None:
            if not group_column:
                raise RequiredArgument(
                    f"{cls.get_aggregates.__name__} requires a group_column"
                    " argument if subgroup_column is given",
                    function=cls.get_aggregates.__name__,
                    argument="subgroup_column",
                )
            cmd.set_attribute("subgroup_column", subgroup_column)

        if text_columns is not None:
            if isinstance(text_columns, str):
                text_columns = [text_columns]
            elif not isinstance(text_columns, Iterable):
                raise InvalidArgumentType(
                    function=cls.get_aggregates.__name__,
                    argument="text_columns",
                    arg_type=getattr(Iterable, "__name__", "Iterable"),
                )
            for column in text_columns:
                cmd.add_element("text_column", column)

        if mode is not None:
            cmd.set_attribute("mode", str(mode))

        # Add additional keyword args as attributes for backward compatibility.
        cmd.set_attributes(kwargs)

        return cmd
