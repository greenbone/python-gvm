# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.vulnerabilities import (
    GmpGetVulnerabilitiesTestMixin,
    GmpGetVulnerabilityTestMixin,
)
from ...gmpv214 import Gmpv214TestCase


class Gmpv214GetVulnerabilityTestCase(
    GmpGetVulnerabilityTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214GetVulnerabilitiesTestCase(
    GmpGetVulnerabilitiesTestMixin, Gmpv214TestCase
):
    pass
