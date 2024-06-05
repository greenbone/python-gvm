# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument, InvalidArgumentType, RequiredArgument
from gvm.protocols.gmp.requests.v224 import (
    AggregateStatistic,
    EntityType,
    SortOrder,
)


class GmpGetAggregatesTestMixin:
    def test_get_aggregates(self):
        """
        Test basic get_aggregates calls with only resource_type except special
        cases for audit, policy, scan_config and task.
        """
        self.gmp.get_aggregates(EntityType.ALERT)

        self.connection.send.has_been_called_with(
            b'<get_aggregates type="alert"/>'
        )

        self.gmp.get_aggregates(resource_type=EntityType.CERT_BUND_ADV)

        self.connection.send.has_been_called_with(
            b'<get_aggregates type="cert_bund_adv"/>'
        )

        self.gmp.get_aggregates(EntityType.CPE)

        self.connection.send.has_been_called_with(
            b'<get_aggregates type="cpe"/>'
        )

        self.gmp.get_aggregates(EntityType.CVE)

        self.connection.send.has_been_called_with(
            b'<get_aggregates type="cve"/>'
        )

        self.gmp.get_aggregates(EntityType.DFN_CERT_ADV)

        self.connection.send.has_been_called_with(
            b'<get_aggregates type="dfn_cert_adv"/>'
        )

        self.gmp.get_aggregates(EntityType.HOST)

        self.connection.send.has_been_called_with(
            b'<get_aggregates type="host"/>'
        )

        self.gmp.get_aggregates(EntityType.NOTE)

        self.connection.send.has_been_called_with(
            b'<get_aggregates type="note"/>'
        )

        self.gmp.get_aggregates(EntityType.NVT)

        self.connection.send.has_been_called_with(
            b'<get_aggregates type="nvt"/>'
        )

        self.gmp.get_aggregates(EntityType.OPERATING_SYSTEM)

        self.connection.send.has_been_called_with(
            b'<get_aggregates type="os"/>'
        )

        self.gmp.get_aggregates(EntityType.OVALDEF)

        self.connection.send.has_been_called_with(
            b'<get_aggregates type="ovaldef"/>'
        )

        self.gmp.get_aggregates(EntityType.OVERRIDE)

        self.connection.send.has_been_called_with(
            b'<get_aggregates type="override"/>'
        )

        self.gmp.get_aggregates(EntityType.REPORT)

        self.connection.send.has_been_called_with(
            b'<get_aggregates type="report"/>'
        )

        self.gmp.get_aggregates(EntityType.RESULT)

        self.connection.send.has_been_called_with(
            b'<get_aggregates type="result"/>'
        )

    def test_get_aggregates_resource_types_with_usage_type(self):
        """
        Test special cases of resource_type in get_aggregates calls that
        should add a usage_type parameter: audit, policy, scan_config and task.
        """
        self.gmp.get_aggregates(EntityType.AUDIT)

        self.connection.send.has_been_called_with(
            b'<get_aggregates usage_type="audit" type="task"/>'
        )

        self.gmp.get_aggregates(EntityType.POLICY)

        self.connection.send.has_been_called_with(
            b'<get_aggregates usage_type="policy" type="config"/>'
        )

        self.gmp.get_aggregates(EntityType.SCAN_CONFIG)

        self.connection.send.has_been_called_with(
            b'<get_aggregates usage_type="scan" type="config"/>'
        )

        self.gmp.get_aggregates(EntityType.TASK)

        self.connection.send.has_been_called_with(
            b'<get_aggregates usage_type="scan" type="task"/>'
        )

    def test_get_aggregates_missing_resource_type(self):
        """
        Test get_aggregates calls with missing resource_type
        """
        with self.assertRaises(RequiredArgument):
            self.gmp.get_aggregates(resource_type=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_aggregates(resource_type="")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_aggregates("")

    def test_get_aggregates_invalid_resource_type(self):
        """
        Test get_aggregates calls with invalid resource_type
        """
        with self.assertRaises(InvalidArgument):
            self.gmp.get_aggregates(resource_type="foo")

    def test_get_aggregates_sort_criteria(self):
        """
        Test get_aggregates calls with sort_criteria given as strings
        """
        self.gmp.get_aggregates(
            EntityType.NVT,
            group_column="family",
            sort_criteria=[
                {"field": "severity", "stat": "mean", "order": "descending"},
                {"stat": "count", "order": "descending"},
                {"field": "family", "order": "ascending"},
            ],
            data_columns=["severity"],
        )

        self.connection.send.has_been_called_with(
            b'<get_aggregates type="nvt" group_column="family">'
            b'<sort field="severity" stat="mean" order="descending"/>'
            b'<sort stat="count" order="descending"/>'
            b'<sort field="family" order="ascending"/>'
            b"<data_column>severity</data_column>"
            b"</get_aggregates>"
        )

    def test_get_aggregates_sort_criteria_enum(self):
        """
        Test get_aggregates calls with sort_criteria given as enums
        """
        self.gmp.get_aggregates(
            EntityType.NVT,
            group_column="family",
            sort_criteria=[
                {
                    "field": "severity",
                    "stat": AggregateStatistic.MEAN,
                    "order": SortOrder.DESCENDING,
                }
            ],
            data_columns=["severity"],
        )

        self.connection.send.has_been_called_with(
            b'<get_aggregates type="nvt" group_column="family">'
            b'<sort field="severity" stat="mean" order="descending"/>'
            b"<data_column>severity</data_column>"
            b"</get_aggregates>"
        )

    def test_get_aggregates_invalid_sort_criteria(self):
        """
        Test get_aggregates calls with invalid sort_criteria
        """
        with self.assertRaises(InvalidArgumentType):
            self.gmp.get_aggregates(
                resource_type=EntityType.ALERT, sort_criteria="INVALID"
            )

        with self.assertRaises(InvalidArgumentType):
            self.gmp.get_aggregates(
                resource_type=EntityType.ALERT, sort_criteria=["INVALID"]
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.get_aggregates(
                resource_type=EntityType.ALERT,
                sort_criteria=[{"stat": "INVALID"}],
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.get_aggregates(
                resource_type=EntityType.ALERT,
                sort_criteria=[{"order": "INVALID"}],
            )

    def test_get_aggregates_group_limits(self):
        """
        Test get_aggregates calls with group limits (first_group, max_groups)
        """
        self.gmp.get_aggregates(EntityType.CPE, first_group=20, max_groups=25)

        self.connection.send.has_been_called_with(
            b'<get_aggregates type="cpe" first_group="20" max_groups="25"/>'
        )

    def test_get_aggregates_invalid_group_limits(self):
        """
        Test get_aggregates calls with invalid group limits
        """
        with self.assertRaises(InvalidArgumentType):
            self.gmp.get_aggregates(
                EntityType.CPE, first_group="INVALID", max_groups=25
            )

        with self.assertRaises(InvalidArgumentType):
            self.gmp.get_aggregates(
                EntityType.CPE, first_group=1, max_groups="INVALID"
            )

    def test_get_aggregates_data_columns(self):
        """
        Test get_aggregates calls with data_columns
        """
        self.gmp.get_aggregates(
            EntityType.CPE, data_columns=["severity", "cves"]
        )

        self.connection.send.has_been_called_with(
            b'<get_aggregates type="cpe">'
            b"<data_column>severity</data_column>"
            b"<data_column>cves</data_column>"
            b"</get_aggregates>"
        )

        self.gmp.get_aggregates(
            resource_type=EntityType.ALERT, data_columns="severity"
        )

        self.connection.send.has_been_called_with(
            b'<get_aggregates type="alert">'
            b"<data_column>severity</data_column>"
            b"</get_aggregates>"
        )

    def test_get_aggregates_group_column(self):
        """
        Test get_aggregates calls with group_column
        """
        self.gmp.get_aggregates(EntityType.NVT, group_column="family")

        self.connection.send.has_been_called_with(
            b'<get_aggregates type="nvt" group_column="family"/>'
        )

    def test_get_aggregates_subgroup_column(self):
        """
        Test get_aggregates calls with subgroup_column
        """
        self.gmp.get_aggregates(
            EntityType.NVT,
            group_column="family",
            subgroup_column="solution_type",
        )

        self.connection.send.has_been_called_with(
            b'<get_aggregates type="nvt" group_column="family"'
            b' subgroup_column="solution_type"/>'
        )

    def test_get_aggregates_missing_group_column(self):
        """
        Test get_aggregates calls with group_column missing
        if subgroup_column was given.
        """
        with self.assertRaises(RequiredArgument):
            self.gmp.get_aggregates(
                resource_type=EntityType.NVT, subgroup_column="solution_type"
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.get_aggregates(
                resource_type=EntityType.NVT,
                group_column="",
                subgroup_column="solution_type",
            )

    def test_get_aggregates_text_columns(self):
        """
        Test get_aggregates calls with text_columns
        """
        self.gmp.get_aggregates(
            EntityType.SCAN_CONFIG,
            group_column="uuid",
            text_columns=["name", "comment"],
        )

        self.connection.send.has_been_called_with(
            b'<get_aggregates usage_type="scan" type="config"'
            b' group_column="uuid">'
            b"<text_column>name</text_column>"
            b"<text_column>comment</text_column>"
            b"</get_aggregates>"
        )

        self.gmp.get_aggregates(
            EntityType.SCAN_CONFIG,
            group_column="uuid",
            text_columns="name",
        )

        self.connection.send.has_been_called_with(
            b'<get_aggregates usage_type="scan" type="config"'
            b' group_column="uuid">'
            b"<text_column>name</text_column>"
            b"</get_aggregates>"
        )

    def test_get_aggregates_mode(self):
        """
        Test get_aggregates calls with mode
        """
        self.gmp.get_aggregates(
            EntityType.NVT, group_column="name", mode="word_counts"
        )

        self.connection.send.has_been_called_with(
            b'<get_aggregates type="nvt" group_column="name"'
            b' mode="word_counts"/>'
        )
