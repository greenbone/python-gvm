# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224 import Gmpv224TestCase
from .vulnerabilities import (
    GmpGetVulnerabilitiesTestMixin,
    GmpGetVulnerabilityTestMixin,
)


class Gmpv224GetVulnerabilityTestCase(
    GmpGetVulnerabilityTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224GetVulnerabilitiesTestCase(
    GmpGetVulnerabilitiesTestMixin, Gmpv224TestCase
):
    pass
