# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.vulnerabilities import (
    GmpGetVulnerabilitiesTestMixin,
    GmpGetVulnerabilityTestMixin,
)
from ...gmpv224 import Gmpv224TestCase


class Gmpv224GetVulnerabilityTestCase(
    GmpGetVulnerabilityTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224GetVulnerabilitiesTestCase(
    GmpGetVulnerabilitiesTestMixin, Gmpv224TestCase
):
    pass
