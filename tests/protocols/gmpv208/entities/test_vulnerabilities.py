# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .vulnerabilities import (
    GmpGetVulnerabilitiesTestMixin,
    GmpGetVulnerabilityTestMixin,
)


class Gmpv208GetVulnerabilityTestCase(
    GmpGetVulnerabilityTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208GetVulnerabilitiesTestCase(
    GmpGetVulnerabilitiesTestMixin, Gmpv208TestCase
):
    pass
